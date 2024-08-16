#ifndef LEG_H
#define LEG_H

#include "servo.h"

class Math;
class Leg{
public:
  Leg(Math* calculator, MyServo* driver);
  int length_thigh;
  int length_calf;
private:
  Math* calculator;
  MyServo* driver;

  float speed;

  unsigned short index_thigh1;
  unsigned short index_thigh2;
  unsigned short index_knee;

  double angle_thigh1;
  double angle_thigh2;
  double angle_knee;

  double prev_angle_thigh1;
  double prev_angle_thigh2;
  double prev_angle_knee;

  unsigned long time_elapsed;

private:

public:
  void Update(unsigned long time);
  float GetSpeed();
  void SetAngles(double thigh1,double thigh2,double knee);
  void Reset();

};

#endif