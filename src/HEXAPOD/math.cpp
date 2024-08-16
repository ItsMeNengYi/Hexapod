#include "math.h"

Math::Math(){
  this->sita1 =0;
  this->sita2 =0;
  this->phi =0;
}

void Math::CalculateAngle(Leg* leg,unsigned long time_elapsed){
  this->length1 = leg->length_thigh;
  this->length2 = leg->length_calf;
  double speed = leg->GetSpeed(); 
  // turning_angle = math.pi/8
  unsigned int period = 2000;
  double z_offset=0;
  double x_offset=130;
  double y_offset=-70;
  double DistanceTravel = 50;
  double r_x;
  double r_y;
  double r_z;

  double angle_a;
  double angle_c;
  double a;
  double time = time_elapsed%period;
  double phase_angle = time/(period/2)*M_PI;

  if(time <=period/2){
    // circle
    r_z = DistanceTravel*cos(phase_angle)+z_offset;
    r_y = DistanceTravel*sin(phase_angle)+y_offset;
    r_x = x_offset;
  }else{
    // line
    r_z = DistanceTravel*cos(phase_angle)+z_offset;
    r_y = y_offset;
    r_x = x_offset;
  }
  // Serial.print(-r_x);
  // Serial.print(" ");
  // Serial.print(r_y);
  // Serial.print(" ");
  // Serial.println(r_z);

  // inverse kinematics
  r_x = -r_x;
  sita2 = atan(r_z/r_x);
  a = sqrt(sq(r_x) + sq(r_z));
  phi = acos((sq(r_z)+sq(r_x)+sq(r_y)-sq(length1)-sq(length2))/(length1*length2*2));
      
  angle_a = atan(sin(phi)/(length1/length2 + cos(phi)));
  if (angle_a<0){
    angle_a = M_PI+angle_a;
  }
  angle_c=atan(abs(r_y/a));

  if(r_y<0){
    sita1 = angle_a-angle_c;
  }else{
    sita1 = angle_a+angle_c;
  }

  //?????????????//
  // sita1 -= 0.7;
  //?????????????//


  if(r_x>0){
    phi = -phi;
    sita1=M_PI - sita1;
  }
  
  sita1 = sita1/M_PI*180;
  sita2 = sita2/M_PI*180;
  phi = phi/M_PI*180;
  phi = phi-sita1;
  
  
}
void Math::GetAngle(Leg* leg){
  leg->SetAngles(sita1,sita2,phi);
}