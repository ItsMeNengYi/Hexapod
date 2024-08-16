#ifndef SERVO_H
#define SERVO_H

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define servoMIN 544
#define servoMAX 2400

class MyServo{
public:
  MyServo();
private:
  Adafruit_PWMServoDriver servoDriver;
  short servoMin = servoMIN;
  short sercoMax = servoMAX;

public:
  void initiate();
  void SetAngle(unsigned short index,double angle);
};

#endif