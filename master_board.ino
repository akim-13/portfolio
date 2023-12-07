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
bool audioPaused = false;         // Represents whether audio is paused.
int lastPeopleInRoom = 0;         // Number of people in the room.
bool manualPause = false;         // Flag for manual pause state.
unsigned long lastPressTime = 0;  // Timer for button debounce.

// Initialize constants.
const int buttonPin = 2;                 // Pin number for the button.
const int debounceDelay = 200;           // Delay for button debounce in milliseconds.
const int timeBetweenVolChecks = 10000;  // Interval for volume checks in milliseconds.
TMRpcm audio;                            // Instance of TMRpcm for audio playback.

// Standard setup function.
void setup() 
{
    // Initializes I2C communication (master).
    Wire.begin();       
    // Initialize serial communication at 9600 bits per second.
    Serial.begin(9600);
    // Attache interrupt to the button.
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
    else 
    {
        // The user will be prompted in the main `loop`.
        Serial.println("Enter the corresponding number to play a song:");

        audio.speakerPin = 9;

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
}


void loop() 
{              
    // If user input is available.
    if (Serial.available()) 
    {                      
        String songNames[numSongs];

        // Get user's input.
        userInput = Serial.parseInt();               

        // Read and discard any extra characters.
        char c = Serial.read(); 

        // If the input is a valid song number.
        if (userInput > 0 && userInput <= numSongs) 
        {
            // Turn off audio.
            audio.disable();

            // Open the root directory.
            File directory = SD.open("/");
            // Discard the first non-song file because it is there by default.
            File file = directory.openNextFile(); 

            // Add every filename to the array songNames.
            for (unsigned int i = 0; i < numSongs; i++) 
            {
                File file = directory.openNextFile(); 
                // Adds to the array.
                songNames[i] = file.name();                 
                file.close();                               
            }

            directory.close();

            // Stores the name of the song the user selected in "song".
            String song = songNames[userInput - 1];  

            // Converts to a c style string.
            const char* songFileName = song.c_str(); 
            // Music is played and the filename is output.
            audio.play(songFileName);
            Serial.print("Playing: ");               
            Serial.println(songFileName);
        }

        // If the user input is invalid.
        else 
            Serial.println("ERROR: invalid integer entered.");
    }

    // If nothing is playing and the audio hasn't been paused, randomly select a song.
    if (!audio.isPlaying() && not(audioPaused)) 
    {
        // Default volume value is 4
        autoVol = 4;              
        audio.setVolume(autoVol); 

        String songNames[numSongs];

        // Randomly generate a number to pick a random track.
        unsigned int random = rand();
        unsigned int randomTrackNum = random % numSongs;

        // Open the root directory.
        File directory = SD.open("/");
        // Discard the first file because it's there by default
        File file = directory.openNextFile(); 

        // Add every filename to the array songNames.
        for (unsigned int i = 0; i < numSongs; i++) 
        {
            File file = directory.openNextFile();
            songNames[i] = file.name();                 // adds to the array
            file.close();                               // closes the open file
        }

        directory.close();                       // closes the open directory

        String song = songNames[randomTrackNum]; // stores the name of the song
            
        const char* songFileName = song.c_str(); // converts to a c style string

        // music is played and the filename is output
        audio.play(songFileName);
        Serial.print("Playing: ");
        Serial.println(songFileName);

    } 
  else if (millis() - previousTime >= timeBetweenVolChecks) { // if audio is playing and 5 seconds has passed since the volume was last checked
    // if 5 seconds has passed since the volume was last checked
    previousTime = millis();                             // resets the last time the volume was checked

    Wire.requestFrom(1, 1);                                 // requests 1 byte from slave 1

    while (Wire.available()) {                           // whilst the communication channel is open (if a value is recieved)
      int micRec = Wire.read();                          // set a variable to the value given from the slave
      if (micRec == 1 and autoVol != 1) {               //  if a 1 was recieved, it means the volume is too high
        autoVol -= 1;                                   //  will turn down the volume if the volume isn't already at its lowest
        audio.setVolume(autoVol);
      }
    }
  }
  // getting info from slave 2
  Wire.requestFrom(2, 1);                               // requests a byte from slave 2
  delay(5);                                             
  if (Wire.available()) {                               // if the communication channel is open (if a value is recieved)
      int peopleInRoom = Wire.read();                   
      lastPeopleInRoom = peopleInRoom;                  // Read the value given by the slave, states the number of people in the room currently
  }
  else {                                                // If the communciation channel isn't available, output it in the serial monitor
      Serial.println("No data available from slave");     
  }



  if (lastPeopleInRoom == 0 && audioPaused == false) {  // If there are no people in the room and the audio isn't already paused
    autoTurnOff();                                      // Pause the audio
  }
  else if (lastPeopleInRoom > 0 && audioPaused == true) { // If there are any people in the room and the audio is currently paused
    autoTurnOn();                                         // Turn the audio back on
  }
}


void pauseAudio() // Pause audio function (BUTTON PRESS)
{
    // The number of milliseconds passed since the Arduino board began running the current program. 
    unsigned long currentTime = millis();
    // Condition for debouncing.
    if (currentTime - lastPressTime > debounceDelay) 
    {
        lastPressTime = currentTime;

        Serial.print("Toggling Pause...\n");
        audio.pause();                      // Pause the audio (still keeps the song data prior to pause)
        audioPaused = not(audioPaused);     // Negate the audioPaused flag to show the audio is now paused

        if (audioPaused)
            manualPause = true;             // If the audio is now paused, set the manualPause flag to true
        else
            manualPause = false;            // If the audio isn't paused anymore, set the flag to false
    }
}

void autoTurnOff() { // Automatic audio pause function (not triggered by button press, triggered by no one in room) 
  Serial.print("Toggling Pause...\n");
  if (not (audioPaused)) {
    audio.pause();                // If the audio isn't paused, pause it.
  }
  audioPaused = not(audioPaused); // Negate the flag
}

void autoTurnOn() {              
  if (manualPause == true) {      // If the audio is currently paused manually (by button press), don't unpause it as manual pausing takes precendence
    return;
  }
  Serial.print("Toggling Pause...\n");
  if (audioPaused) {                    // Otherwise, if the audio is currently paused, unpause it.
    audio.pause();
  }
  audioPaused = not(audioPaused);       // Negate the current flag value
}
