#include <Wire.h>

const int enterLed = 4; 
const int exitLed = 5;  

int lastPeopleCInRoom = 0; 

void setup() {
  pinMode(enterLed, OUTPUT);
  pinMode(exitLed, OUTPUT);
  Wire.begin(); 
  Serial.begin(9600);
}

void loop() {
  Wire.requestFrom(4, 1); //request 1 byte from slave device with address 4
  
  if (Wire.available()) {
    int peopleInRoom = Wire.read(); //read the count from the slave
    if (peopleInRoom > lastPeopleCount) {
      digitalWrite(enterLed, HIGH);
      delay(500);
      digitalWrite(enterLed, LOW);
    } else if (peopleInRoom < lastPeopleCount) {
      digitalWrite(exitLed, HIGH);
      delay(500);
      digitalWrite(exitLed, LOW);
    }
    lastPeopleInRoom = peopleInRoom; 
  }

  delay(1000); 
}
