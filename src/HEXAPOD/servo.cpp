#include "servo.h"

MyServo::MyServo(){
  this->servoDriver = Adafruit_PWMServoDriver();
}

void MyServo::initiate(){
  servoDriver.begin();
  servoDriver.setPWMFreq(333);
}

void MyServo::SetAngle(unsigned short index,double angle){
  if(index >= 0 && index <= 15){
    double pulseWidth = angle / 270 * (2400 - 544) + 544;
    if (pulseWidth < 544) {
      pulseWidth = 544;
    }else if(pulseWidth > 2400) {
      pulseWidth = 2400;
    }
    // Serial.println((int)pulseWidth);
    servoDriver.setPWM(index, 0, (int)pulseWidth);
  }
  return;
}