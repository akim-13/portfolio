#include <Servo.h>

// LEDs.
const int redLEDs[] = {4, 5, 6};
const int greenLEDs[] = {10, 12, 13};
const int blueRedLED = 8;
const int blueGreenLED = 9;

// Buttons and debouncing.
const int redButton = 2;
const int greenButton = 3;
const int debounceDelay = 200;
volatile unsigned long lastRedButtonPressTime = 0;
volatile unsigned long lastGreenButtonPressTime = 0;

// Buzzer.
const int buzzer = A1;
bool buzzerON = false;

// Servo.
Servo servo;
const int servoPin = 11;

// Potentiometer.
const int potentiometer = A0;

// Misc.
int minDelayTime = 500;
int maxDelayTime = 2000;
int blueRedLEDState; 
int blueGreenLEDState; 
volatile int redScore = 0;
volatile int greenScore = 0;

struct Player 
{
    const char* colorName;
    int LEDs[3];
    int blueLED;
    int* score;
    unsigned long* lastPressTime;
};

Player redPlayer   = { "Red",   { redLEDs[0],   redLEDs[1],   redLEDs[2]   }, blueRedLED,   &redScore,   &lastRedButtonPressTime   };
Player greenPlayer = { "Green", { greenLEDs[0], greenLEDs[1], greenLEDs[2] }, blueGreenLED, &greenScore, &lastGreenButtonPressTime } ;

void setup() 
{
    // Set a mode for each pin.
    for (int i=0; i<3; i++)
    {
        pinMode(redLEDs[i], OUTPUT);
        pinMode(greenLEDs[i], OUTPUT);
    }
    pinMode(blueRedLED, OUTPUT);
    pinMode(blueGreenLED, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(redButton, INPUT);
    pinMode(greenButton, INPUT);
    pinMode(potentiometer, INPUT);

    // Reset servo.
    servo.attach(servoPin);
    servo.write(90);

    // Trigger interrupts when a button is pressed (i.e. a pin goes from LOW to HIGH).
    attachInterrupt(0, redButtonPress, RISING); 
    attachInterrupt(1, greenButtonPress, RISING);
}

void activateBuzzerIfMissed()
{
    if (buzzerON)
    {
        tone(buzzer, 300);
        delay(100);
        noTone(buzzer);
        buzzerON = false;
    }
}

void rotateServo()
{
    // Point at red if they are winning.
    if (*redPlayer.score > *greenPlayer.score)
        servo.write(45);
    // Point at green if they are winning.
    else if (*greenPlayer.score > *redPlayer.score)
        servo.write(135);
    // Point in the middle if tied.
    else
        servo.write(90);
}

float calcDifficulty()
{
    float difficulty = analogRead(potentiometer);
    if (difficulty != 0)
        // Divide by max value of the potentiometer to normalize.
        return difficulty / 1023;
    else
        // Default to the easiest difficulty if the potentiometer reads 0.
        return 1;
}

void loop() 
{
    activateBuzzerIfMissed();
    rotateServo();

    float difficulty = calcDifficulty();

    int redRndNum = random(3); 
    int greenRndNum = random(3);
    int redDelay = random(minDelayTime, maxDelayTime) * difficulty;
    int greenDelay = random(minDelayTime, maxDelayTime) * difficulty;
    const int redGreenDelay = 1000;

    // Red ON.
    digitalWrite(redLEDs[redRndNum], HIGH);

    delay(redDelay);

    // Red OFF.
    digitalWrite(redLEDs[redRndNum], LOW);
    // Turn off Blue LED for the Red player if they scored.
    if(digitalRead(blueRedLED) == HIGH)
        digitalWrite(blueRedLED, LOW);

    delay(redGreenDelay);

    // Green ON.
    digitalWrite(greenLEDs[greenRndNum], HIGH);

    delay(greenDelay);

    // Green OFF.
    digitalWrite(greenLEDs[greenRndNum], LOW);
    // Turn off Blue LED for the Green player if they scored.
    if(digitalRead(blueGreenLED) == HIGH)
        digitalWrite(blueGreenLED, LOW);

    delay(redGreenDelay);
}

void buttonPress(Player &player) {
    unsigned long currentTime = millis();
    // Condition for debouncing.
    if (currentTime - *player.lastPressTime > debounceDelay) 
    {
        *player.lastPressTime = currentTime;

        for (int i=0; i<3; i++)
        {
            int LEDState = digitalRead(player.LEDs[i]);
            // If an LED is on, increment the score and turn on Blue LED.
            if (LEDState == HIGH)
            {
                (*player.score)++;
                digitalWrite(player.blueLED, HIGH); 
                break;
            }
            // If none of the LEDs were on, decrement the score and sound the buzzer.
            else if (i == 2)
            {
                (*player.score)--; 
                buzzerON = true;
            }
        }
    }
    
    // Light up all of the winner's LEDs and end the game.
    if (*player.score >= 10)
    {
        while (true)
        {
            for (int i=0; i<3; i++)
                digitalWrite(player.LEDs[i], HIGH);
            digitalWrite(player.blueLED, HIGH);
        }
    }
}

void redButtonPress() 
{
    buttonPress(redPlayer);
}

void greenButtonPress() 
{
    buttonPress(greenPlayer);
}

