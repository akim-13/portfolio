#include <Wire.h>

const int irEnterPin = 3; 
const int irExitPin = 2;  

volatile int peopleInRoom = 0; 

void setup() {
  pinMode(irEnterPin, INPUT);
  pinMode(irExitPin, INPUT);
  Wire.begin(4); 
  
  attachInterrupt(digitalPinToInterrupt(irEnterPin), personEntered, FALLING);
  attachInterrupt(digitalPinToInterrupt(irExitPin), personExited, FALLING);
  
  Wire.onRequest(requestEvent); 
}

void personEntered() {
  if (digitalRead(irEnterPin) == LOW) { 
    peopleInRoom++; // Increment when someone enters
  }
}

void personExited() {
  if (digitalRead(irExitPin) == LOW && peopleInRoom > 0) { 
    peopleInRoom--; 
  }
}

void requestEvent() {
  Wire.write(peopleInRoom);
}
