// libraries
#include <Wire.h>
#include <Thread.h>
#include <ThreadController.h>
#include <LiquidCrystal.h> // Library to allow usage of the LCD
#include <math.h> // Math library to allow usage of mathmatical functions

// assigning pins to components
const int micPin = A0; // MAX4466 (Microphone)

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2; // Assigning LCD pins
LiquidCrystal lcd(rs,en,d4,d5,d6,d7); // Initialising LCD object

// initialising constants
const int pickupWindow = 2000; 

// initialising variables
unsigned int voltage;
byte eventValue;
unsigned int vol;

// assigning LED pins
int ledPins[] = {10,9,8,7};

// Initialising threading globals
// Thread completed flag which states whether the thread loop has been completed allowing
bool threadCompleted = true;
// Creating the thread with the getVolumeThread function
const Thread volumeCheckThread(getVolume);

void setup() {
  for (int i=0;i < 4;i++) {
    pinMode(ledPins[i], OUTPUT); // Setting pin mode of the LED pins to output
  }
  
  Serial.begin(9600);           // initialise serial output
  Wire.begin(1);                // initialises I2C communication (slave address 1)
  Wire.onRequest(sendData);     // initialises the request function  

  lcd.begin(16, 2);                     // Setting LCD size to 16x2
  lcd.println("Now Playing!        ");  // Printing to LCD display, intentional extra spacing to prevent blank squares appearing on the display
  
}

  // main program loop
void loop() {
  volumeCheckThread.run();  // Run the thread that gets the volume level
  updateLCD(); // Update LCD with the volume level obtained from the thread just run
  doLEDs();      // Continue running the LED function
}

// Update the LCD cursor and display the normalised volume level, using ceil function (round upwards)
// Normalising using max value of analogRead() which is 1023
void updateLCD() {
  lcd.setCursor(0,1);
  lcd.println("Volume Lvl: " + String(ceil((( (float) vol ) / 1023.0) * 100.0)) + "     ");
}

// Uses threading to help manage the flow of execution between gathering volume levels and performing LED operations.
void getVolume(Thread* thread) {
    if (threadCompleted) {     // Only runs if no thread is currently active
      threadCompleted = false; // Prevents a thread from being run whilst one is already active. 
      unsigned int maxVoltage = 0; // Assigning values to local variables
      unsigned int minVoltage = 1024;
      unsigned long startTime = millis(); // Gets the current time
      while (millis() - startTime < pickupWindow) { // Runs for a defined time 'pickupWindow' - set to 2s
    
        voltage = analogRead(micPin); // retrieves voltage from microphone
    
        if (voltage < 1024) {           // filtering to any outlier recordings
          if (voltage > maxVoltage) {   // if the voltage is the highest yet, it is recorded
            maxVoltage = voltage;
          }
          else if (voltage < minVoltage) { // if the voltage is the lowest yet, it is recorded
            minVoltage = voltage;
          }
        }
      }
      threadCompleted = true; // Marks the thread process as completed so it can be run again
      // Calculates volume
      vol = maxVoltage - minVoltage;
      // volume is output so it can be seen on the serial plotter
      Serial.println(vol);
    }
}

// Function to permform LED patterns
void doLEDs() {
  long startTime = millis(); // Gets the time at the point of function call
  while ((millis() - startTime) < 5000) { // Will continue for 5s before yielding for 1s to allow for volume level gathering (in main loop)
    sequenceLightEffect();
    alternatingLightEffect();
  }
}

// Using for loops with delays to create lighting patterns
void sequenceLightEffect() {
  for (int x=0; x<4; x++) {
     for (int i=0;i < 4;i++) {
       digitalWrite(ledPins[i], HIGH);
       delay(40);
    }
    delay(200);
    for (int i=0;i < 4;i++) {
        digitalWrite(ledPins[i], LOW);
        delay(40);
    }
  }
}

void alternatingLightEffect() {
  for (int x=0;x<2;x++) {
    for (int i=0;i < 4;i += 2) {
       digitalWrite(ledPins[i], HIGH);
       delay(40);
    }
    delay(200);
    for (int i=0;i < 4;i += 2) {
        digitalWrite(ledPins[i], LOW);
        delay(40);
    }
    for (int i=1;i < 4;i += 2) {
       digitalWrite(ledPins[i], HIGH);
       delay(40);
    }
    delay(200);
    for (int i=1;i < 4;i += 2) {
        digitalWrite(ledPins[i], LOW);
        delay(40);
    }
    delay(100);
  }
}

// data request function
void sendData() {

  // the music will not register louder than 400, so we filter out any values higher than this
  if (vol > 100 and vol < 400) { // if the vol is too high, send a 1 to tell the controller to turn vol down.
    eventValue = 1;         // Sets global variable eventValue to 1
    Wire.write(eventValue); // Sends a 1 to the master to represent volume needs to be lowered
    lcd.setCursor(0,1);
    lcd.println("Lowering Volume!     "); // Updates LCD cursor and displays that the volume is being lowered
  }
  else { // if the vol is fine then send a 0
    eventValue = 0; 
    Wire.write(eventValue); // Master board interprets 0 as no volume adjustment needed
  }
}
