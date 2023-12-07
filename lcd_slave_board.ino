#include <Wire.h>
#include <Thread.h>
#include <ThreadController.h>
#include <LiquidCrystal.h>     // Incorporates the LCD library for display functionality.
#include <math.h>              // Includes the math library for mathematical functions.

// Assigning pins to components
const int micPin = A0; // Pin assignment for MAX4466 (Microphone).

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2; // Pins for the LCD display.
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);                  // Initializing the LCD object.

// Initializing constants
const int pickupWindow = 2000; // Time window for audio pickup in milliseconds.

// Initializing variables
unsigned int voltage;
byte eventValue;
unsigned int vol;

// Assigning LED pins
int ledPins[] = {10, 9, 8, 7};

// Initializing threading variables
bool threadCompleted = true; // Flag to check if the thread loop is completed.
const Thread volumeCheckThread(getVolume); // Creating the volume checking thread.

void setup() 
{
    for (int i = 0; i < 4; i++) 
    {
        pinMode(ledPins[i], OUTPUT);     // Setting the mode of LED pins to output.
    }

    Serial.begin(9600);                  // Initialize serial communication.
    Wire.begin(1);                       // Initialize I2C communication with slave address 1.
    Wire.onRequest(sendData);            // Initialize the request function.

    lcd.begin(16, 2);                    // Set LCD size to 16x2.
    lcd.println("Now Playing!        "); // Display message on LCD.
}

// Main program loop
void loop() 
{
    volumeCheckThread.run(); // Run the volume level checking thread.
    updateLCD();             // Update the LCD with volume level.
    doLEDs();                // Execute LED lighting effects.
}

// Update the LCD to display the normalized volume level.
void updateLCD() 
{
    lcd.setCursor(0, 1);
    lcd.println("Volume Lvl: " + String(ceil(((float)vol) / 1023.0 * 100.0)) + "     ");
}

// Threading function for volume management.
void getVolume(Thread* thread) 
{
    if (threadCompleted) 
    {
        threadCompleted = false;            // Lock thread execution.
        unsigned int maxVoltage = 0;
        unsigned int minVoltage = 1024;
        unsigned long startTime = millis(); // Record start time.

        // Collect data for a specific time window.
        while (millis() - startTime < pickupWindow) 
        {
            voltage = analogRead(micPin); // Read voltage from the microphone.

            // Filter and record voltage fluctuations.
            if (voltage < 1024) 
            {
                if (voltage > maxVoltage) 
                {
                    maxVoltage = voltage;
                }
                else if (voltage < minVoltage) 
                {
                    minVoltage = voltage;
                }
            }
        }
        threadCompleted = true;        // Unlock thread for next execution.
        vol = maxVoltage - minVoltage; // Calculate volume level.
        Serial.println(vol);           // Output volume for debugging.
    }
}

// Function to manage LED lighting effects.
void doLEDs() 
{
    // Record the start time of the function.
    long startTime = millis(); 
    
    // Run LED effects for a specified duration.
    while ((millis() - startTime) < 5000) 
    {
        sequenceLightEffect();
        alternatingLightEffect();
    }
}

// Sequence lighting effect using LEDs.
void sequenceLightEffect() 
{
    for (int x = 0; x < 4; x++) 
    {
        for (int i = 0; i < 4; i++) 
        {
            digitalWrite(ledPins[i], HIGH);
            delay(40);
        }
        delay(200);
        for (int i = 0; i < 4; i++) 
        {
            digitalWrite(ledPins[i], LOW);
            delay(40);
        }
    }
}

// Alternating lighting effect using LEDs.
void alternatingLightEffect() 
{
    for (int x = 0; x < 2; x++) 
    {
        for (int i = 0; i < 4; i += 2) 
        {
            digitalWrite(ledPins[i], HIGH);
            delay(40);
        }
        delay(200);
        for (int i = 0; i < 4; i += 2) 
        {
            digitalWrite(ledPins[i], LOW);
            delay(40);
        }
        for (int i = 1; i < 4; i += 2) 
        {
            digitalWrite(ledPins[i], HIGH);
            delay(40);
        }
        delay(200);
        for (int i = 1; i < 4; i += 2) 
        {
            digitalWrite(ledPins[i], LOW);
            delay(40);
        }
        delay(100);
    }
}

// Function to handle data requests.
void sendData() 
{
    // Filter and manage volume levels.
    if (vol > 100 && vol < 400) 
    {
        eventValue = 1; 
        Wire.write(eventValue);               // Inform the master to lower the volume.
        lcd.setCursor(0, 1);
        lcd.println("Lowering Volume!     "); // Update LCD display.
    }
    else 
    {
        eventValue = 0;
        Wire.write(eventValue); // No adjustment needed.
    }
}

