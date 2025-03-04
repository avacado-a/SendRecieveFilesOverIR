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

/*int lastReloadVal = 1;                      // reload button, debounce 
unsigned long lastRDebounceTime = 0;        // reload button debounce time 
int reloadState;                            // reload button debounce result

bool isReloading = false;                   // allows reloading sequence 
unsigned long reloadTimer;                  // time to add shots to ammo bar
int ammo = maxAmmo;                         // current ammo bootup at max
*/

// Initialize game timeout variable
unsigned long timeoutStartTime = - HIT_TIMEOUT - 1000;
int connect = 0;
int loss = 0;
// IR pulse, tracks team distinction
uint16_t sCommand;                            // IR command being sent
bool expectedEight = true;
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SETUP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
void setup() {

  Serial.begin(115200);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);

}


// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOOP <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
void loop() {

  handleIRReception();

}

// Read incoming message ----------
void handleIRReception() {
  if (IrReceiver.decode()) {
    checkPlayerHit();
    IrReceiver.resume(); // Ensure IR receiver is reset
  }
}

// Check if message is a "shot" from an enemy team ----------
void checkPlayerHit() {
  if (connect != IrReceiver.decodedIRData.address) {
    connect++;
    if (connect > 255) {
      connect = 1;
    }
    if (connect != IrReceiver.decodedIRData.address) {
      // TODO: Deal with gap in records
      if (IrReceiver.decodedIRData.address!=0) {
        while (connect != IrReceiver.decodedIRData.address) {
        Serial.print(connect);
        Serial.print(",");
        Serial.println(0);
        connect++;
        if (connect > 255) {
          connect = 1;
        }
        //delay(1000);
      }
      Serial.print(IrReceiver.decodedIRData.address);  
      Serial.print(",");  
      Serial.println(IrReceiver.decodedIRData.command);
      }
    } else {
      Serial.print(IrReceiver.decodedIRData.address);  
      Serial.print(",");  
      Serial.println(IrReceiver.decodedIRData.command);
    }
  }
  
}