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
    delay(1000);
    digitalWrite(pinLED, LOW);
}

void loop() {
    // Request 1 byte from the slave board with address 4.
    Wire.requestFrom(4, 1); 
  
    if (Wire.available()) {
        // Read the count from the slave board.
        int peopleInRoom = Wire.read(); 
        Serial.print("People in Room: ");
        Serial.println(peopleInRoom);
        
        if (peopleInRoom > lastPeopleInRoom) {
            Serial.println("Someone entered");
            flashLED (enterLED);
        } else if (peopleInRoom < lastPeopleInRoom) {
            Serial.println("Someone exited");
            flashLED (exitLED);
        }

        lastPeopleInRoom = peopleInRoom; 
    } else {
        Serial.println("No data available from slave");
    }

    delay(1000); // Wait for a second before making the next request
}

    delay(1000); 
}
