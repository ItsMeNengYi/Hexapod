#include "leg.h"
#include "math.h"

Leg::Leg(Math* calculator,MyServo* driver){
  this->speed = 1;
  this->length_thigh = 110;
  this->length_calf = 170;
  this->prev_angle_thigh1 = 0;
  this->prev_angle_thigh2 = 0;
  this->prev_angle_knee = 0;
  this->index_thigh1= 0;
  this->index_thigh2= 1; 
  this->index_knee= 2; 
  this->calculator = calculator;
  this->driver = driver;
}


void Leg::Update(unsigned long time){
  calculator->CalculateAngle(this,time);
  calculator->GetAngle(this);

  //transform
  angle_thigh1+=135;
  angle_thigh2+=135;
  angle_knee = 270 - angle_knee;

  Serial.print(angle_thigh1);
  Serial.print(" ");
  Serial.print(angle_thigh2);
  Serial.print(" ");
  Serial.println(angle_knee);

  
  driver->SetAngle(index_thigh1,angle_thigh1);
  prev_angle_thigh1 = angle_thigh1;

  driver->SetAngle(index_thigh2,angle_thigh2);
  prev_angle_thigh2 = angle_thigh2;

  driver->SetAngle(index_knee,angle_knee);
  prev_angle_knee = angle_knee;
}

void Leg::SetAngles(double thigh1,double thigh2,double knee){
  angle_thigh1 = thigh1;
  angle_thigh2 = thigh2;
  angle_knee = knee;
}

void Leg::Reset(){
  driver->SetAngle(index_thigh1,135);
  driver->SetAngle(index_thigh2,135);
  driver->SetAngle(index_knee,180);
}

float Leg::GetSpeed(){
  return speed;
}
