

int X_accis_pin = A0;
int Y_accis_pin = A1;
int Button = A2;

void setup() {
  //Setup Serielle Komunikation
  Serial.begin(115200);

  //Setup pins
  pinMode(X_accis_pin, INPUT);
  pinMode(Y_accis_pin, INPUT);
  pinMode(Button,INPUT_PULLUP);
  
}


bool last_Button_state = false;

void loop() {
  //Serial.print(digitalRead(Button));
  if(!digitalRead(Button) == true){
    last_Button_state = true;
  }
  else{
    if(last_Button_state == true){
      last_Button_state = false;
      Serial.println("T");
    }
  }
  
  //Serial.print("X");
  int cash_x = (analogRead(X_accis_pin) - 512) / 5.12;
  if(cash_x <= 4 && cash_x >= (-4)){
    cash_x = 0;
  }
  Serial.print("X");
  Serial.println(cash_x );
  Serial.print("Y");
  int cash_y = analogRead(Y_accis_pin) - 512;
  cash_y = cash_y / 8;

  if(cash_y <= 4 && cash_y >= (-4)){
    cash_y = 0;
  }
  
  else if(cash_y < (-4)){
    cash_y = cash_y - 36;
  }
  
  else if(cash_y > 4){
    cash_y = cash_y +36;
  }


  
  Serial.println(cash_y);
  delay(100);
  
}
