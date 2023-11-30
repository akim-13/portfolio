#include <Wire.h>

const int enterLED = 4; 
const int exitLED = 5;  

int lastPeopleInRoom = 0; 

void setup() 
{
    pinMode(enterLED, OUTPUT);
    pinMode(exitLED, OUTPUT);
    Wire.begin(); 
    Serial.begin(9600);
}

void flashLED (int pinLED)
{
    digitalWrite(pinLED, HIGH);
    delay(500);
    digitalWrite(pinLED, LOW);
}

void loop() 
{
    // Request 1 byte from the slave board with address 4.
    Wire.requestFrom(4, 1); 
  
    if (Wire.available()) 
    {
        // Read the count from the slave board.
        int peopleInRoom = Wire.read(); 
        if (peopleInRoom > lastPeopleInRoom) 
            flashLED (enterLED);
        else 
            flashLED (exitLED);

        lastPeopleInRoom = peopleInRoom; 
    }

    delay(1000); 
}
