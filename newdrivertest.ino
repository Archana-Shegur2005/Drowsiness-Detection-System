#include <Servo.h>
#define Servopin 3

Servo servo1;
char sleep_status = 0;
bool command_received = false;  

void setup() {
  Serial.begin(9600);  
  servo1.attach(Servopin);
  delay(100);            
  servo1.write(0);       
  servo1.detach();       
}

void loop() {
  
  if (Serial.available() > 0) 
  {
    sleep_status = Serial.read();
    command_received = true;    

  
    if (sleep_status == 'a' && command_received)
     {  
      servo1.attach(Servopin);  
      servo1.write(120);         
      delay(1000);              
      servo1.write(0);        
      delay(500);             
      servo1.detach();          
    } 
    else if (sleep_status == 'b' && command_received) 
    {  
      servo1.attach(Servopin);  
      servo1.write(0);         
      delay(500);              
      servo1.detach();          
    }
  }

  
  if (!command_received) {
    servo1.attach(Servopin);
    servo1.write(0);  
    delay(500);
    servo1.detach();  
  }
}
