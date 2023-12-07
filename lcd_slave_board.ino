#include <Wire.h>
#include <math.h>
#include <LiquidCrystal.h>     // LCD library for display functionality.
#include <ThreadController.h>  // Threading.
#include <Thread.h>           

// LCD display pins.
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
const int numOfLEDs = 4;
// LEDs pins.
const int ledPins[numOfLEDs] = {10, 9, 8, 7};
// Pin for MAX4466 (microphone).
const int micPin = A0;

// Initialize the LCD object.
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Time window for audio pickup in milliseconds.
const int pickupWindow = 2000;

// Initialize other variables.
unsigned int voltage;
byte eventValue;
unsigned int vol;

void sendDataToMaster() 
{
    // Filter and manage volume levels.
    if (vol > 100 && vol < 400) 
    {
        eventValue = 1; 
        // Inform the master to lower the volume.
        Wire.write(eventValue);               
        // Positions the cursor at the beginning of the second row on the LCD.
        lcd.setCursor(0, 1);
        // Update LCD display.
        lcd.println("Lowering Volume!     "); 
    }
    else 
    {
        eventValue = 0;
        // Master board interprets 0 as no volume adjustment needed
        Wire.write(eventValue); 
    }
}


// Standard setup function.
void setup() 
{     
    // Set the mode of LED pins to output.
    for (int i = 0; i < numOfLEDs; i++) 
        pinMode(ledPins[i], OUTPUT);

    // Initialize serial communication at 9600 bits per second.
    Serial.begin(9600);

    // Initialize I2C communication (slave address `1`).
    Wire.begin(1);
    // Send data to the master board when requested.
    Wire.onRequest(sendDataToMaster);

    // Set LCD size to 16x2.
    lcd.begin(16, 2);                     
    // Display message on LCD.
    lcd.println("Now Playing!        ");
}


// Turn on (state HIGH) or off (state LOW) specified LEDs.
void changeLEDsState(int state, int startingFromLED, int step)
{
    for (int i = startingFromLED; i < numOfLEDs; i += step) 
    {
        digitalWrite(ledPins[i], state);
        delay(40);
    }
}


// Alternating lighting effect using LEDs.
void alternatingLightEffect() 
{
    for (int x = 0; x < 2; x++) 
    {
        // Turn on LEDs 0 and 2.
        changeLEDsState(HIGH, 0, 2);

        delay(200);

        // Turn off LEDs 0 and 2.
        changeLEDsState(LOW, 0, 2);
        // Turn on LEDs 1 and 3.
        changeLEDsState(HIGH, 1, 2);

        delay(200);

        // Turn off LEDs 1 and 3.
        changeLEDsState(LOW, 1, 2);

        delay(100);
    }
}


// Sequence lighting effect using LEDs.
void sequenceLightEffect() 
{
    for (int x = 0; x < numOfLEDs; x++) 
    {
        // Turn on all LEDs.
        changeLEDsState(HIGH, 0, 1);

        delay(200);

        // Turn off all LEDs.
        changeLEDsState(LOW, 0, 1);
    }
}


// Function to manage LED lighting effects.
void doLEDs() 
{
    // Record the start time of the function.
    unsigned long startTime = millis(); 
    
    // Run LED effects for 5 seconds.
    while ((millis() - startTime) < 5000) 
    {
        sequenceLightEffect();
        alternatingLightEffect();
    }
}


// Update the LCD to display the normalized volume level.
void updateLCD() 
{
    float normalizedVolumeLvl = ceil(((float)vol) / 1023.0 * 100.0)

    // Positions the cursor at the beginning of the second row on the LCD.
    lcd.setCursor(0, 1);
    lcd.print("Volume Lvl: ");
    lcd.print(String(normalizedVolumeLvl));
    lcd.println("%    ");
}


// Threading function for volume management.
void getVolume(Thread* thread) 
{
    if (threadCompleted) 
    {            
        // Lock thread execution.
        threadCompleted = false;
        unsigned int maxVoltage = 0;
        unsigned int minVoltage = 1024;
        // Record start time.
        unsigned long startTime = millis();

        // Collect data for a specific time window.
        while (millis() - startTime < pickupWindow) 
        {
            // Read voltage from the microphone.
            voltage = analogRead(micPin);

            // Filter and record voltage fluctuations.
            if (voltage < 1024) 
            {
                maxVoltage = max(voltage, maxVoltage);
                minVoltage = min(voltage, minVoltage);
            }
        }

        // Unlock thread for next execution.
        threadCompleted = true;        
        // Calculate volume level.
        vol = maxVoltage - minVoltage; 
        // Output volume for debugging.
        Serial.println(vol);           
    }
}

// Threading.
bool threadCompleted = true;                // Flag to check if the thread loop is completed.
const Thread volumeCheckThread(getVolume);  // Create the volume checking thread.

// Standard main loop.
void loop() 
{
    // Run the volume level checking thread.
    volumeCheckThread.run(); 
    // Update the LCD with volume level.
    updateLCD();             
    // Execute LED lighting effects.
    doLEDs();                
}

