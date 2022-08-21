#include <Servo.h>

#define rf 5
#define rr 6
#define pwmr 9
#define pwml 10
#define lf 7
#define lr 8
#define red 2
#define green 4
#define blue 3
#define volt A5 
#define current A4
#define motSwitch 11

void forward();
void backward();
void right();
void left();
void neutral();
void forwardRight();
void forwardLeft();
void backwardRight();
void backwardLeft();
void setPWM();

Servo escl;
Servo escr;
char s[3];
short int level = 1;
short int maxl = 190;
short int maxr = 255;
short int maxl1[2];
short int maxr2[2];
unsigned long debounce = 0;
short int state = 0;
bool last_state = false;

void setup() {
  // put your setup code here = 0, to run once:
  pinMode(lf,OUTPUT);
  pinMode(lr,OUTPUT);
  pinMode(rf,OUTPUT);
  pinMode(rr,OUTPUT);
  pinMode(pwmr,OUTPUT);
  pinMode(pwml,OUTPUT);
  pinMode(red,OUTPUT);
  pinMode(green,OUTPUT);
  pinMode(blue,OUTPUT);
  pinMode(volt,INPUT);
  pinMode(current,INPUT);
  pinMode(motSwitch,INPUT_PULLUP);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  digitalWrite(12,HIGH);
  digitalWrite(13,LOW);
  setPWM();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 char s[5];
 if(millis()-debounce >100)
 {
  if(digitalRead(motSwitch) == LOW and last_state == false)
 {
  debounce = millis();
  last_state = true;
  if(state == 0)
  {
    escl.attach(10);
    escl.attach(9);
    digitalWrite(12,LOW);
    digitalWrite(13,HIGH);
    state = 1;
    }
   else
   {
    escl.detach();
    escr.detach();
    digitalWrite(12,HIGH);
    digitalWrite(13,LOW);
    state = 0;
    }
  }
  if(digitalRead(motSwitch) == HIGH and last_state == true)
  {
    last_state = false;
  }
 }
 
 if(!Serial.available() > 0)
 {
  Serial.readBytesUntil('\n',s,5);
  if(s[0] == 'w' and s[1] == 'a')
  {
     forwardLeft();
    }
  else if(s[0] == 'w' and s[1] == 'd')
  {
     forwardRight(); 
    }
  else if(s[0] == 's' and s[1] == 'a')
  {
     backwardLeft(); 
    }
  else if(s[0] == 's' and s[1] == 'd')
  {
     backwardRight(); 
    }
  else if(s[0] == 'w')
  {
    forward();
  }
  else if(s[0] == 's')
  {
    backward(); 
  }
  else if(s[0] == 'a')
  {
     left(); 
  }
  else if(s[0] == 'd')
  {
    right(); 
  }
  else if(s[0] == 'n')
  {
     neutral(); 
    }
  else if(s[0] == 'U' and s[1] == 'P' and level <3)
  {
    level++;
    setPWM();
    }
  else if(s[0] == 'D' and s[1] == 'O' and s[2] == 'W' and s[3] == 'N' and level >1)
  {
    level--;
    setPWM();
    }
  }
  
  Serial.print(analogRead(volt)*5.0/1023);
  Serial.print(',');
  Serial.println((((analogRead(current)*5.0/1023))-2.5)/0.185);
}

void forward()
{
  if(state == 0)
  {
  digitalWrite(lf,HIGH);
  digitalWrite(lr,LOW);
  digitalWrite(rf,HIGH);
  digitalWrite(rr,LOW); 
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl);    
    }
  else
  {
    escl.write(maxl1[1]);
    escr.write(maxr2[1]);
    }
}

void backward()
{
  if(state == 0)
  {
  digitalWrite(lr,HIGH);
  digitalWrite(lf,LOW);
  digitalWrite(rr,HIGH);
  digitalWrite(rf,LOW); 
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl);    
  }
  else
  {
    escl.write(maxl1[0]);
    escr.write(maxr2[0]);
  }
}

void right()
{
  if(state == 0)
  {
  digitalWrite(lf,HIGH);
  digitalWrite(lr,LOW);
  digitalWrite(rf,LOW);
  digitalWrite(rr,HIGH);
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl); 
  }
  else
  {
   escl.write(maxl1[1]);
   escr.write(maxr2[0]); 
  }
}

void left()
{
  if(state == 0)
  {
  digitalWrite(rf,HIGH);
  digitalWrite(rr,LOW);
  digitalWrite(lf,LOW);
  digitalWrite(lr,HIGH); 
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl); 
  }
  else
  {
  escl.write(maxl1[0]);
  escr.write(maxr2[1]); 
  }
}

void neutral()
{
  if(state == 0)
  {
  digitalWrite(rf,LOW);
  digitalWrite(rr,LOW);
  digitalWrite(lf,LOW);
  digitalWrite(lr,LOW); 
  analogWrite(pwmr,0);
  analogWrite(pwml,0); 
  }
  else
  {
  escl.write(90);
  escr.write(90);
  }  
}

void forwardRight()
{
  if(state == 0)
  {
  digitalWrite(lf,HIGH);
  digitalWrite(lr,LOW);
  digitalWrite(rf,HIGH);
  digitalWrite(rr,LOW); 
  analogWrite(pwmr,maxr/2);
  analogWrite(pwml,maxl); 
  }
  else
  {
  escl.write(maxl1[1]);
  escr.write(maxr2[1]-40);
  }
}
void forwardLeft()
{
  if(state == 0)
  {
  digitalWrite(lf,HIGH);
  digitalWrite(lr,LOW);
  digitalWrite(rf,HIGH);
  digitalWrite(rr,LOW); 
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl/2); 
  }
  else
  {
  escl.write(maxl1[1]-40);
  escr.write(maxr2[1]); 
  }
}
void backwardRight()
{
  if(state == 0)
  {
  digitalWrite(lr,HIGH);
  digitalWrite(lf,LOW);
  digitalWrite(rr,HIGH);
  digitalWrite(rf,LOW); 
  analogWrite(pwmr,maxr/2);
  analogWrite(pwml,maxl);
  }
  else
  {
  escl.write(maxl1[0]);
  escr.write(maxr2[0]+40); 
  }
  
}
void backwardLeft()
{
  if(state == 0)
  {
  digitalWrite(lr,HIGH);
  digitalWrite(lf,LOW);
  digitalWrite(rr,HIGH);
  digitalWrite(rf,LOW); 
  analogWrite(pwmr,maxr);
  analogWrite(pwml,maxl/2);
  }
  else
  {
  escl.write(maxl1[0]+40);
  escr.write(maxr2[0]); 
  }
}

void setPWM()
{
  switch (level)
  {
  case 1:
    maxl = 102;
    maxr = 165;
    maxl1[0] = 40;
    maxl1[1] = 140;
    maxr2[0] = 40;
    maxr2[1] = 140;
    digitalWrite(red,LOW);
    digitalWrite(green,HIGH);
    digitalWrite(blue,HIGH);
    break;
  case 2:
    maxl = 125;
    maxr = 195;
    maxl1[0] = 20;
    maxl1[1] = 160;
    maxr2[0] = 20;
    maxr2[1] = 160;
    digitalWrite(red,HIGH);
    digitalWrite(green,HIGH);
    digitalWrite(blue,LOW);
    break;
  case 3:
    maxl = 180;
    maxr = 255;
    maxl1[0] = 0;
    maxl1[1] = 180;
    maxr2[0] = 0;
    maxr2[1] = 180;
    digitalWrite(red,HIGH);
    digitalWrite(green,LOW);
    digitalWrite(blue,HIGH);
    break; 
  }
}
