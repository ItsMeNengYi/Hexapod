#ifndef MATH_H
#define MATH_H

#include <Arduino.h>
#include "leg.h"

class Math{
public:
  Math();

private:
  double length1;
  double length2;
  
  double sita1;
  double sita2;
  double phi;

public:
  void CalculateAngle(Leg* leg, unsigned long time_elapsed);
  void GetAngle(Leg* leg);
  unsigned long Get_position();
};

#endif