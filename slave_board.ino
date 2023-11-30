#include <Wire.h>

const int irEnterPin = 3; 
const int irExitPin = 2;  

volatile int peopleInRoom = 0; 

void setup() 
{
    pinMode(irEnterPin, INPUT);
    pinMode(irExitPin, INPUT);
    Wire.begin(4); 

    Serial.begin(9600);
    attachInterrupt(digitalPinToInterrupt(irEnterPin), personEntered, FALLING);
    attachInterrupt(digitalPinToInterrupt(irExitPin), personExited, FALLING);

    Wire.onRequest(requestEvent); 
}

void loop() {}

void personEntered() 
{
    peopleInRoom++;
    // For debugging.
    Serial.print("+: ");
    Serial.println(peopleInRoom);
}

void personExited() 
{
    if (peopleInRoom > 0) 
    { 
        peopleInRoom--; 
        // For debugging.
        Serial.print("-: ");
        Serial.println(peopleInRoom);
    }
}

void requestEvent() 
{
    Wire.write(peopleInRoom);
}
