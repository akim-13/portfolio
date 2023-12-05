// libraries
#include <Wire.h>
#include <Thread.h>
#include <ThreadController.h>
#include <LiquidCrystal.h>
#include <math.h>

// assigning pins to components
const int micPin = A0; // MAX4466 (Microphone)

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

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

// initialise serial monitor
void setup() {
  for (int i=0;i < 4;i++) {
    pinMode(ledPins[i], OUTPUT); // Setting pin mode of the LED pins to output
  }
  
  Serial.begin(9600);           // initialise serial output
  Wire.begin(1);                // initialises I2C communication (slave address 1)
  Wire.onRequest(sendData);     // initialises the request function  

  lcd.begin(16, 2);
  lcd.println("Now Playing!        ");
  
}


  // main program loop
void loop() {
  volumeCheckThread.run();  // Run the thread that gets the volume level
  updateLCD(); // Update LCD with the volume level obtained from the thread just run
  doLEDs();      // Continue running the LED function
}

void updateLCD() {
  lcd.setCursor(0,1);
  lcd.println("Volume Lvl: " + String(ceil((( (float) vol ) / 1023.0) * 100.0)) + "     ");
}

// Uses threading to help manage the flow of execution between gathering volume levels and performing LED operations.
void getVolume(Thread* thread) {
    if (threadCompleted) {     // Only runs if no thread is currently active
      threadCompleted = false; // Prevents a thread from being run whilst one is already active. 
      unsigned int maxVoltage = 0;
      unsigned int minVoltage = 1024;
      unsigned long startTime = millis();
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

void doLEDs() {
  long startTime = millis(); // Gets the time at the point of function call
  while ((millis() - startTime) < 5000) { // Will continue for 5s before yielding for 1s to allow for volume level gathering (in main loop)
    sequenceLightEffect();
    alternatingLightEffect();
  }
}

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
    eventValue = 1;
    Wire.write(eventValue);
    lcd.setCursor(0,1);
    lcd.println("Lowering Volume!     ");
  }
  else { // if the vol is fine then send a 0
    eventValue = 0;
    Wire.write(eventValue);
  }
}
