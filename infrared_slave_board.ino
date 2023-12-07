#include <Wire.h>

// Initiate global variables.
const int IREntrancePin = 3;    // Infrared sensor at the entrance.
const int IRExitPin = 2;        // Infrared sensor at the exit.
volatile int peopleInRoom = 0;  // Number of people in the room. 


void sendDataToMaster() 
{
    // Send the number of people in the room to the master board.
    Wire.write(peopleInRoom);
}


// Standard setup function.
void setup() 
{
    // Set the pins of the IR sensors to behave as input.
    pinMode(IREntrancePin, INPUT);
    pinMode(IRExitPin, INPUT);

    // Initialize I2C communication (slave address `2`).
    Wire.begin(2); 
    // Send data to the master board when requested.
    Wire.onRequest(sendDataToMaster); 

    // Initialize serial communication at 9600 bits per second.
    Serial.begin(9600);
}


void handleEnteringPerson() 
{
    // Increment the counter of people.
    peopleInRoom++;
    // For debugging.
    Serial.print("+: ");
    Serial.println(peopleInRoom);
}


void handleExitingPerson() 
{
    // Do not allow the counter to go negative.
    if (peopleInRoom > 0) 
    { 
        // Decrement the counter of people.
        peopleInRoom--; 
        // For debugging.
        Serial.print("-: ");
        Serial.println(peopleInRoom);
    }
}


// Standard main loop.
void loop() 
{
    // Check for a person every half a second.
    delay(500);

    // If the IR sensor at the entrance has activated.
    if (digitalRead(IREntrancePin) == HIGH) 
    {
        handleEnteringPerson();
        // Deactivate the entrance IR sensor.
        digitalWrite(IREntrancePin, LOW);
    }

    // TODO: check whether we need this delay.
    delay(100);

    // If the IR sensor at the exit has activated.
    if (digitalRead(IRExitPin) == HIGH) 
    {
        handleExitingPerson();
        // Deactivate the exit IR sensor.
        digitalWrite(IRExitPin, LOW);
    }
}

