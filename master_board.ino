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
bool audioPaused = false; // creating variable representing pause state
int buttonPin = 2; // assigning variable to button pin number
int lastPeopleInRoom = 0; // setting the number of people in the room to 0
bool manualPause = false; // settings the manual pause state to 0 (prevents conflicts with auto pausing)
// Variables to prevent button debounce
unsigned long lastPressTime = 0;
const int debounceDelay = 200;

// initialise consants
TMRpcm audio; // creates an instance of the TMRpcm object named "audio"
const int timeBetweenVolChecks = 10000; // volume is checked every 5 seconds

void setup() {
  Wire.begin();       // initialises I2C communication (no address because master)
  Serial.begin(9600); // initialises serial output
  Serial.println("Initialising SD card."); // Shows the SD initialisation process has been started

  attachInterrupt(0, pauseAudio, RISING); // Attatches a rising interrupt to the button, allowing it to trigger the toggleAudio function
  pinMode(buttonPin, INPUT_PULLUP); // Setting the button pin to an input

// if the SD card can't be accessed then the program will not execute. no parameter needed for begin() as it's in the default (pin 9)
  if (SD.begin() == false) {
    Serial.println("Initialisation failed."); 
    while (true); // If initialisation fails, an infinite loop starts preventing other parts of the program from running
  }

// if the SD card can be accessed, this branch is executed
  else {
    
    audio.speakerPin = 9; // sets the speakerpin to 9

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

    directory.close();                        // close the open directory

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

      File directoryAgain = SD.open("/");        // stores the root directory, which is an instance of the file object, in "directoryAgain" as a directory instance was previously opened
      File file = directoryAgain.openNextFile(); // discard the first file because it's there by default

      // loop which adds every filename to the array songNames
      for (unsigned int i = 0; i < numSongs; i++) {
        File file = directoryAgain.openNextFile();  // stores the next file in "directory", which is an instance of the file object, in "file"
        songNames[i] = file.name();                 // adds to the array
        file.close();                               
      }

      directoryAgain.close();                       // closes the directory instance

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

  // if nothing is playing and the audio hasn't been paused, randomly select a song
  if (!audio.isPlaying() && not(audioPaused)) {

    autoVol = 4;              // Default volume value is 4
    audio.setVolume(autoVol); // set the volume to 4

    String songNames[numSongs]; // initialises the array songNames which will store the song names

    // randomly generate a number to pick a random track
    unsigned int random = rand();
    unsigned int randomTrackNum = random % numSongs;

    File directoryAgain = SD.open("/"); // stores the root directory, which is an instance of the file object, in "directoryAgain"
    File file = directoryAgain.openNextFile(); // discard the first file because it's there by default

    // loop which adds every filename to the array songNames
    for (unsigned int i = 0; i < numSongs; i++) {
      File file = directoryAgain.openNextFile();  // stores the next file in "directory", which is an instance of the file object, in "file"
      songNames[i] = file.name();                 // adds to the array
      file.close();                               // closes the open file
    }

    directoryAgain.close();                       // closes the open directory

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
