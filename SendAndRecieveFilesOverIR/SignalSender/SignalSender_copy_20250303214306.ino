/*
  ************************************************************************************
  * MIT License
  *
  * Copyright (c) 2025 Crunchlabs LLC (Laser Tag Code)

  * Permission is hereby granted, free of charge, to any person obtaining a copy
  * of this software and associated documentation files (the "Software"), to deal
  * in the Software without restriction, including without limitation the rights
  * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  * copies of the Software, and to permit persons to whom the Software is furnished
  * to do so, subject to the following conditions:
  *
  * The above copyright notice and this permission notice shall be included in all
  * copies or substantial portions of the Software.
  *
  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
  * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  *
  ************************************************************************************
*/
// >>>>>>>>>>>>>>>>>>>>>>>>>>>> PIN DEFINITIONS <<<<<<<<<<<<<<<<<<<<<<<<<<<<
#define IR_SEND_PIN         3
#define IR_RECEIVE_PIN      5 
#define _IR_TIMING_TEST_PIN 7

//#define LED_PIN     6
//#define LED_COUNT   6

//#define RELOAD_PIN      8
#define SERVO_PIN       9
//#define BUZZER_PIN      11 
#define TRIGGER_PIN     12

#define TEAM1_PIN       15      // A1 pin 
#define TEAM2_PIN       16      // A2 pin
#define TEAM3_PIN       17      // A3 pin

// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LIBRARIES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#define DECODE_NEC          // defines RIR Protocol (Apple and Onkyo)

#include <IRremote.hpp>   
//#include <Adafruit_NeoPixel.h>  
#include <Arduino.h>
#include <Servo.h>

//Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
Servo myservo;

// >>>>>>>>>>>>>>>>>>>>>>>>>>> GAME PARAMETERS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#define DEBOUNCE_DELAY 20

#define SERVO_INITIAL_POS 150     // how agressively to undarken goggles 
#define SERVO_READY_POS 120       // reduce aggresiveness near end of action
#define SERVO_HIT_POS 50

#define TRIGGER_COOLDOWN 500      // milliseconds  
#define HIT_TIMEOUT 10000         // milliseconds
//#define RELOAD_TIME_EACH 1000     // milliseconds

/*const bool infiniteAmmo = true;
const int maxAmmo = LED_COUNT;        
const bool deathTakesAmmo = true;*/          

int team = 1;     // default 

// >>>>>>>>>>>>>>>>>>>>>>>>>>> GAME VARIABLES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

int lastTriggerVal = 1;                     // trigger debounce variable
unsigned long lastTDebounceTime = 0;        // trigger button debounce time
int triggerState;                           // trigger debounce result
bool buttonWasReleased = true;              // release check, no "full auto"
unsigned long previousTriggerMillis = 0;    // cooldown timestamp between shots
bool newData = false;
const byte numChars = 32;
char receivedChars[numChars];
bool starting = true; 
int loss = 1;
/*int lastReloadVal = 1;                      // reload button, debounce 
unsigned long lastRDebounceTime = 0;        // reload button debounce time 
int reloadState;                            // reload button debounce result

bool isReloading = false;                   // allows reloading sequence 
unsigned long reloadTimer;                  // time to add shots to ammo bar
int ammo = maxAmmo;                         // current ammo bootup at max
*/

// Initialize game timeout variable
unsigned long timeoutStartTime = - HIT_TIMEOUT - 1000;

// IR pulse, tracks team distinction
uint8_t sCommand;
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SETUP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
void setup() {
  myservo.attach(SERVO_PIN);
  myservo.write(SERVO_INITIAL_POS);
  delay(500);
  myservo.write(SERVO_READY_POS);
  delay(500);
  myservo.detach();

  pinMode(TRIGGER_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(TEAM1_PIN, INPUT_PULLUP);
  pinMode(TEAM2_PIN, INPUT_PULLUP);
  pinMode(TEAM3_PIN, INPUT_PULLUP);

  sCommand = 0x34;

  Serial.begin(115200);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
}


// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOOP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
char* recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
    newData = false;
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;       
        }
    }
    if (newData) {
      return receivedChars;
    } else {
      return nullptr;
    }
}

void waitTillnRecieved(String n) {
  while (n.compareTo(String(receivedChars))!=0) {
    char* receivedChars = recvWithStartEndMarkers();
  }
}

void loop() {
  if (starting) {
    Serial.println("colo");
    waitTillnRecieved("n");
    Serial.println("confirming!");    
    // Add more starting code if needed
    starting = false;
  }
  int test = 0;
  int byte = 0;
  Serial.println("done");

  char* receivedChars = recvWithStartEndMarkers();
  bool don = false;
  // while (!don){
  //   char* receivedChars = recvWithStartEndMarkers();
  //   if (receivedChars != nullptr) {
  //     Serial.println(receivedChars);
  //     test = atoi(receivedChars);
  //     don = true;
  //   }
  // }
  don = false;
  while (!don){
    char* receivedChars = recvWithStartEndMarkers();
    if (receivedChars != nullptr) {
      Serial.println(receivedChars);
      byte = atoi(receivedChars);
      don = true;
    }
  }
  //Serial.println(test);
  Serial.println(byte);
  sendIR_Pulse((uint16_t)byte);
  loss++;
  if (loss > 255) {
    loss = 1;
  }
}

// Fire "Shot" ----------
void sendIR_Pulse(uint16_t sent) {
  //Serial.flush();
  //sendFAST(sent,1,1);
  IrSender.sendNEC(loss, sent, 1);
  delay(10);
  
}
