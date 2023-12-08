#include <SPI.h>      // Enables communication with SPI devices (the SD card module).
#include <SD.h>       // Enables reading from SD card.
#include <stdbool.h>  // Provides boolean data type.
#include <TMRpcm.h>   // Enables processing of .wav files.
#include <stdlib.h>   // Provides the rand() function.
#include <Wire.h>     // Enables I2C communication.

// Initialize variables.
unsigned int numSongs = 0;        // Total number of songs.
int userInput;                    // User input for song selection.
byte receivedValue;               // Stores the byte value received from slaves.
unsigned long previousTime = 0;   // Stores the last time the volume was checked.
int autoVol = 7;                  // Default volume level.
int lastPeopleInRoom = 0;         // Number of people in the room.
unsigned long lastPressTime = 0;  // Timer for button debounce.
bool audioIsPaused = false;         // Represents whether audio is paused.
bool audioIsManuallyPaused = false;         // Flag for manual pause state.
bool roomIsEmpty = true;          // Start with an empty room.
bool volumeIsTooLoud = false;     // Indicates whether the volume has to be lowered.

// Initialize constants.
const int buttonPin = 2;                 // Pin number for the button.
const int debounceDelay = 200;           // Delay for button debounce in milliseconds.
const int timeBetweenVolChecks = 10000;  // Interval for volume checks in milliseconds.
TMRpcm audio;                            // Instance of TMRpcm for audio playback.

// Pause audio function (BUTTON PRESS)
void pauseAudio() 
{
    // The number of milliseconds passed since the Arduino board began running the current program. 
    unsigned long currentTime = millis();
    // Condition for debouncing.
    if (currentTime - lastPressTime > debounceDelay) 
    {
        lastPressTime = currentTime;

        Serial.print("Toggling Pause...\n");
        // Pause the audio (still keeps the song data prior to pause).
        audio.pause();                      
        audioIsPaused = true;

        if (audioIsPaused)
            // If the audio is now paused, set the `audioIsManuallyPaused` flag to true.
            audioIsManuallyPaused = true;             
        else
            // If the audio is not paused anymore, set the flag to false.
            audioIsManuallyPaused = false;            
    }
}


// Handle SD card files.
void listAndCountSongs() 
{
    // Open the root directory.
    File directory = SD.open("/"); 

    while (true) 
    {
        // Get the next file from the directory.
        File file = directory.openNextFile();

        // Break the loop when there are no more files.
        if (!file) 
            break; 
        else
            numSongs++;

        // Displays the filenames with corresponding numbers.
        Serial.print(numSongs);
        Serial.print(". ");
        Serial.println(file.name()); 

        // Closes the file to avoid memory issues.
        file.close(); 
    }

    // Account for one of the read files (not a song), which is in the directory by default.
    numSongs--;

    directory.close();
}


// Standard setup function.
void setup() 
{
    // Initializes I2C communication (master).
    Wire.begin();       
    // Initialize serial communication at 9600 bits per second.
    Serial.begin(9600);

    // Attach interrupt to the button.
    attachInterrupt(0, pauseAudio, RISING); 
    // Set button pin to input with pull-up resistor.
    pinMode(buttonPin, INPUT_PULLUP);       

    Serial.println("Initializing SD card...");

    // Check if the SD card failed to initialize.
    if (!SD.begin()) 
    {
        Serial.println("ERROR: Initialization failed."); 
        // Enter infinite loop to halt further execution on failure.
        while (true); 
    }

    // The user will be prompted in the main `loop()`.
    Serial.println("Enter the corresponding number to play a song:");

    // Assign the speaker pin.
    audio.speakerPin = 9;

    listAndCountSongs();
}


void autoPlayAudio() 
{              
    // If the audio is currently paused manually (by button press), don't unpause it as manual pausing takes precedence.
    if (audioIsManuallyPaused)
        return;

    Serial.println("Toggling Pause...");

    // If the audio is paused, unpause it.
    if (audioIsPaused)
        // The `pause()` function (rather confusingly) toggles the pause.
        audio.pause();

    audioIsPaused = false;
}


// Automatic audio pause function (not triggered by button press, triggered by no one in room) 
void autoPauseAudio() 
{ 
    Serial.println("Toggling Pause...");

    // If the audio isn't paused, pause it.
    if (!audioIsPaused) 
        audio.pause();                

    audioIsPaused = true;
}


// Communicate with the IR slave.
void toggleAudioByOccupancy()
{
    // Requests a byte from slave 2.
    Wire.requestFrom(2, 1);                               

    // TODO: What is this 5ms delay, do we need it?
    delay(5);                                             

    // If the communication channel is open (if a value is received)
    if (Wire.available()) 
        roomIsEmpty = Wire.read();                   
    else 
        Serial.println("No data available from the slave.");     

    // If there are no people in the room and the audio isn't already paused.
    if (roomIsEmpty && !audioIsPaused) 
        // Pause the audio.
        autoPauseAudio();                                      
    // If there are any people in the room and the audio is currently paused.
    else if (!roomIsEmpty && audioIsPaused)
        // Turn the audio back on
        autoPlayAudio();                                         
}


// Communicate with the LCD/microphone slave.
void lowerVolumeIfTooLoud()
{
    // Requests 1 byte from slave 1.
    Wire.requestFrom(1, 1);                                 

    // While the communication channel is open (if a value is received).
    while (Wire.available()) 
    {                           
        // Set a variable to the value given from the slave.
        volumeIsTooLoud = Wire.read();                          
        //  If a 1 was received, it means the volume is too high.
        if (volumeIsTooLoud and autoVol != 1) 
        {               
            // Turn down the volume if the it is not already at its lowest.
            autoVol -= 1;                                   
            audio.setVolume(autoVol);
        }
    }
}


String* getSongsFromRootDir() 
{
    // Open the root directory.
    File directory = SD.open("/");
    // Discard the first file, which is there by default and not a song.
    directory.openNextFile(); 

    // Dynamically allocate an array of Strings.
    String* songNames = new String[numSongs];

    // Add every filename to the array `songNames`.
    for (int i = 0; i < numSongs; i++) 
    {
        File file = directory.openNextFile();
        songNames[i] = file.name();                 
        file.close();
    }

    directory.close();

    return songNames;
}


void playSelectedSong(int songIndex)
{
    // Add songs to `songNames` from the root directory.
    String* songNames[numSongs] = getSongsFromRootDir();
    // Stores the name of the song the user selected in "song".
    String song = songNames[songIndex];  

    // Free the dynamically allocated memory.
    delete[] songNames;

    // Convert to a C style string.
    const char* songFileName = song.c_str(); 
    // Music is played and the filename is output.
    audio.play(songFileName);
    Serial.print("Playing: ");               
    Serial.println(songFileName);
}


void selectRandomSong()
{
    // Default volume value is 4.
    autoVol = 4;              
    audio.setVolume(autoVol); 

    // Randomly generate a number to play a random track.
    unsigned int randomTrackNum = rand() % numSongs;
    playSelectedSong(randomTrackNum);
}


void selectUsersSong()
{
    // Get user's input.
    userInput = Serial.parseInt();               

    // Read and discard any extra characters.
    char c = Serial.read(); 

    // If the input is a valid song number.
    if (userInput > 0 && userInput <= numSongs) 
    {
        // Turn off audio.
        audio.disable();
        playSelectedSong(userInput - 1);
    }
    else 
        Serial.println("ERROR: invalid integer entered.");
}


void loop() 
{              
    // If user input is available.
    if (Serial.available()) 
        selectUsersSong();

    // If nothing is playing and the audio has not been paused, randomly select a song.
    if (!audio.isPlaying() && !audioIsPaused) 
        selectRandomSong();
    // If audio is playing and a number of seconds have passed since the volume was last checked.
    else if (millis() - previousTime >= timeBetweenVolChecks) 
    { 
        // Resets the last time the volume was checked.
        previousTime = millis();                             
        lowerVolumeIfTooLoud();
    }

    toggleAudioByOccupancy();
}

