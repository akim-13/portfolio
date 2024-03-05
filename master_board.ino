// libraries
#include <SPI.h> // enables communication with SPI devices (the SD card module)
#include <SD.h> // enables reading from SD card
#include <stdbool.h> // provides boolean data type
#include <TMRpcm.h> // enables processing of .wav files
#include <stdlib.h> // provides the rand() function
#include <Wire.h> // enables I2C communication

// initialise variables 
unsigned int numSongs = 0;
int userInput;
unsigned long previousTime = 0; // stores the last time the volume was checked
int autoVol = 7;                // allows the arduino to change the volume automatically if it's too high
bool autoPaused = false;        // represents the automatic pause state
bool manualPaused = false;      // represents the manual pause state

// debounce values
unsigned long lastPress = millis();
unsigned long debounceDelay = 500; // button can only be pressed once per half second

// communication flags
byte peopleInRoom; // stores the flag received from the IR slave
byte micValue;     // stores the flag received from the LCD slave

// assigning pins to components
int buttonPin = 2;

// initialise constants
TMRpcm audio;                           // creates an instance of the TMRpcm object named "audio"
const int timeBetweenChecks = 2500; // volume and people are checked every 10 seconds

struct numberedSongs {int key; char* value;};
numberedSongs songsIndex[7]; // One extra size capacity as index 0 isnt used


// function which pauses the audio if the button has been pressed
void manualPauseAudio() {
  // debounce implementation
  if ((millis() - lastPress) > debounceDelay) {
    lastPress = millis(); // resets the last press
    
    // if the audio is already paused do nothing
    // if audio is playing, pause it
    if (autoPaused == false && manualPaused == false) {
      Serial.print("Manually Pausing...\n");
      audio.pause();
      manualPaused = true;
    }
  
    // if the audio has been manually paused, play it
    else if (autoPaused == false && manualPaused == true) {
      Serial.print("Manually Playing...\n");
      audio.pause();
      manualPaused = false;
    }
  }
}

void setup() {
  Wire.begin();       // initialises I2C communication (no address because master)
  Serial.begin(9600); // initialises serial output

  // initialise button interrupt & pinMode
  attachInterrupt(0, manualPauseAudio, RISING);
  pinMode(buttonPin, INPUT_PULLUP);

  // initialising the SD card
  Serial.println("Initialising SD card.");

// if the SD card can't be accessed then the master will not execute
// the SD card is connected via the default pin. So no parameter pin is needed
  if (SD.begin() == false) {
    Serial.println("Initialisation failed."); 
    while (true);
  }

  // if the SD card can be accessed, this branch is executed
  else {
    
    // initialise audio output
    audio.speakerPin = 9; //

    // output the names of the songs
    Serial.println("Enter the corresponding number to play a song: ");
    
    File directory = SD.open("/");                             // stores the root directory, which is an instance of the file object, in "directory"

    int songCount = 1;                                        // Start index at 1 as user will be presented options 1 - 6.
    while (true) {                                            // Loops until no file is reached
      File file = directory.openNextFile(); 
      if (file) {                                             // If the next file exists
        if (isWavFile(file.name())) {                         // Check if the file is a .wav (SYSTEM file doesn't so we need to check to avoid it being added)
          songsIndex[songCount].key = songCount;              // Set the key to the index of the song
          songsIndex[songCount].value = strdup((file.name()));  // Set the value at that index to the files name, allocating memory prior
          Serial.print(songCount);                            // Prints out the options to the user
          Serial.print(". ");
          Serial.println(file.name());
          songCount += 1;                                     // Increments the counter for next loop iteration
          file.close();                                       // Close the file to free resources
        }
      } else {
        break;                                                // If no file is found, break the loop
      }
    }
    directory.close();
  }
}

bool isWavFile(String fileName) 
{
    // Convert to lowercase for case-insensitive comparison.
    fileName.toLowerCase();

    // Check if the file name ends with ".wav"
    return fileName.endsWith(".wav");
}

// Receieves the data from the slave boards and processes it accordingly
void checkSlaveBoards() {

  // checking the LCD slave (address 1)
  Wire.beginTransmission(1);                                 // Opens transmission on wire 1
  byte transmissionOpen1  = Wire.endTransmission();          // Checks the I2C bus was valid, receives 0 if it was valid
  if (transmissionOpen1 == 0) {                              // Request the data from the wire if the transmission line worked
    Wire.requestFrom(1, 1, true);                            // This was implemented as a closed transmission line was halting the rest of the loop
    
    // Reads the data from the LCD slave board
    while (Wire.available()) {
      micValue = Wire.read();
  
      // if the LCD slave has detected that the volume is too high and the audio isn't already at its lowest, lower it by 1
      // Receiving a 1 means volume needs to be lowered, otherwise leave it.
      if (micValue == 1 and autoVol != 1) {
        autoVol--;
        audio.setVolume(autoVol);
      }
    }
  }

  Wire.beginTransmission(2);                                // Opens transmission on wire 2
  byte newDataReceived2 = Wire.endTransmission();           // Checks the I2C bus was valid, receives 0 if it was valid
  if (newDataReceived2  == 0) {
    Wire.requestFrom(2, 1);                                 // requests 1 byte from address 2
  
    // Retrieve data from the IR slave board
    while (Wire.available()) {
      peopleInRoom = Wire.read(); 
  
      // if nobody is in the room and the audio has not been automatically or manually paused, pause it
      if ((peopleInRoom == 0) && (!autoPaused) && (!manualPaused)) {
        Serial.print("Automatically Pausing...\n"); // informs user that the audio is being paused
        audio.pause();                              // pauses the audio
        autoPaused = true;
      }
  
      // if people are in the room and the audio has been automatically paused and not manually paused, play it
      else if ((peopleInRoom == 1) && (autoPaused) && (!manualPaused)) {
        Serial.print("Automatically Playing...\n"); // informs user that the audio is being played
        audio.pause();                              // plays the audio
        autoPaused = false;
      }
    }
  }
}

void loop() {  
  if (Serial.available()) {

    audio.setVolume(4); // resets the volume every time a new song is selected


    userInput = Serial.parseInt(); // retrieve user input
    Serial.read(); // clears the serial buffer
    Serial.print("Reading input...");

    // if the input is a valid song number
    if (1 <= userInput <= 6) {
      // music is played and the filename is output
      audio.play(songsIndex[userInput].value);       // Retrieves the song name at the user provided index
      Serial.print("Manually Playing: ");            
      Serial.println(songsIndex[userInput].value);   // Prints the song name
    }

    // if the user input is invalid 
    else {
      Serial.println("Error: invalid integer entered.");
    }
  }
  delay(100);
  // if nothing is playing, randomly select a song
  if (!audio.isPlaying()) { 
    Serial.println("Nothing playing");
    audio.disable(); // turn the audio off

    // resets the volume at the start of each song
    autoVol = 4;
    audio.setVolume(autoVol);


    // randomly select an audio track
    unsigned int random = rand();
    unsigned int randomTrackNum = random % 6;

    //directory.close(); // ensures the directory has been closed properly
    Serial.println(randomTrackNum+1);
    char* toPlay = songsIndex[randomTrackNum+1].value; // stores the name of the song the user selected in "song"
        
    //const char* songFileName = song.c_str(); // converts the song name to a c style string

    // music is played and the filename is output
    audio.play(toPlay);
    Serial.print("Automatically Playing: ");
    Serial.println(toPlay);
  }
 
  // if audio is playing and 10 seconds has passed since the slave flags were last checked, they are checked again
  else if (millis() - previousTime >= timeBetweenChecks) {
    previousTime = millis();              // resets the last time the volume was checked
    checkSlaveBoards();
  }
}
  
