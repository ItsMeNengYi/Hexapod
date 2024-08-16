#include <Arduino.h>
#include <BLEDevice.h>

#include "hexapod.h"
#include "leg.h"
#include "math.h"
#include "servo.h"

Math calculator;
MyServo driver;
Leg demoleg(&calculator, &driver);

void setup() {
  // Serial.begin(9600);
  driver.initiate();
  demoleg.Reset();
  delay(500);
}

void loop() {
  // demoleg.Reset();
  demoleg.Update(millis());

}
