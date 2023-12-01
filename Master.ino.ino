#include <SPI.h> // enables communication with SPI devices (the SD card module)
#include <SD.h> // enables reading from SD card
#include <stdbool.h> // provides boolean data type
#include <TMRpcm.h> // enables processing of .wav files
#include <stdlib.h> // provides the rand() function
#include <Wire.h> // enables I2C communication

// initialise variables 
unsigned int numSongs = 0;
int userInput;
byte receivedValue; // stores the byte value received from slaves
unsigned long previousTime = 0; // stores the last time the volume was checked
int autoVol = 7; // allows the arduino to change the volume if it's too high
bool audioPaused = false; // Initialise variable representing pause state
int buttonPin = 2;
int lastPeopleInRoom = 0; 

// initialise consants
TMRpcm audio; // creates an instance of the TMRpcm object named "audio"
const int timeBetweenVolChecks = 10000; // volume is checked every 5 seconds

void setup() {
  Wire.begin();       // initialises I2C communication (no address because master)
  Serial.begin(9600); // initialises serial output
  // SETUP SD CARD
  Serial.println("Initialising SD card.");

  // ATTATCH BUTTON INTERRUPT
  attachInterrupt(0, pauseAudio, RISING);
  pinMode(buttonPin, INPUT_PULLUP);

// if the SD card can't be accessed then the program will not execute. no parameter needed fr begin() as it's in the default (pin 9)
  if (SD.begin() == false) {
    Serial.println("Initialisation failed."); 
    while (true);
  }

// if the SD card can be accessed, this branch us executed
  else {
    
    // SETUP AUDIO OUTPUT
    audio.speakerPin = 9; // sets the speakerpin to 9

    // output the names of the songs
    Serial.println("Enter the corresponding number to play a song: ");
    
    File directory = SD.open("/");            // stores the root directory, which is an instance of the file object, in "directory"
    File file = directory.openNextFile();     // discards the first file in the directory because it's there by default
    
    while (true) {                            // repeats until all files have been output
      File file = directory.openNextFile();   // stores the next file in "directory", which is an instance of the file object, in "file"
      if (!file) break;                       // breaks the loop when there are no more files to output
      numSongs += 1;                          // counts the song
      Serial.print(numSongs);
      Serial.print(". ");
      Serial.println(file.name());            // displays the filenames and their corresponding numbers
      file.close();
    }

    directory.close();  

  }
}

void loop() {              

  // if user input available
  if (Serial.available()) {

    String songNames[numSongs];                  // initialises the array songNames which will store the song names
    
    userInput = Serial.parseInt();               // gather user input
    
    char c = Serial.read(); // read and discard any extra characters

    // if the input is a valid song number
    if (userInput <= numSongs) {
      audio.disable();                             // turn audio off

      File directoryAgain = SD.open("/");        // stores the root directory, which is an instance of the file object, in "directoryAgain"
      File file = directoryAgain.openNextFile(); // discard the first file because it's there by default

      // loop which adds every filename to the array songNames
      for (unsigned int i = 0; i < numSongs; i++) {
        File file = directoryAgain.openNextFile();  // stores the next file in "directory", which is an instance of the file object, in "file"
        songNames[i] = file.name();                 // adds to the array
        file.close();                               
      }

      directoryAgain.close();

      String song = songNames[userInput - 1];  // stores the name of the song the user selected in "song"
        
      const char* songFileName = song.c_str(); // converts to a c style string

      // music is played and the filename is output
      audio.play(songFileName);
      Serial.print("Playing: ");               
      Serial.println(songFileName);
    }

    // if the user input is invalid 
    else {
      Serial.println("Error: invalid integer entered.");
    }
  }

  // if nothing is playing, randomly select a song
  if (!audio.isPlaying() && not(audioPaused)) {

    autoVol = 4;
    audio.setVolume(autoVol);

    String songNames[numSongs]; // initialises the array songNames which will store the song names

    // randomly select an audio track
    unsigned int random = rand();
    unsigned int randomTrackNum = random % 6;

    File directoryAgain = SD.open("/"); // stores the root directory, which is an instance of the file object, in "directoryAgain"
    File file = directoryAgain.openNextFile(); // discard the first file because it's there by default

    // loop which adds every filename to the array songNames
    for (unsigned int i = 0; i < numSongs; i++) {
      File file = directoryAgain.openNextFile();  // stores the next file in "directory", which is an instance of the file object, in "file"
      songNames[i] = file.name();                 // adds to the array
      file.close();
    }

    directoryAgain.close();

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

    while (Wire.available()) {                           // if the volume is too loud (a 1 is received), turn it down
      int micRec = Wire.read();
      if (micRec == 1 and autoVol != 1) {
        autoVol -= 1;
        //audio.setVolume(autoVol);
      }
    }
  }
  // getting info from slave 2
  Wire.requestFrom(2, 1); 
  delay(5);
  if (Wire.available()) {
      // Read the count from the slave board.
      int peopleInRoom = Wire.read(); 
      lastPeopleInRoom = peopleInRoom; 
  }
  else {
      Serial.println("No data available from slave");
  }
}

void pauseAudio() {
  Serial.print("Toggling Pause...\n");
  audio.pause();
  audioPaused = not(audioPaused);
}
