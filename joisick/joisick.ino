

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
  int cache_x = (analogRead(X_accis_pin) - 512) / 5.12;
  if(cache_x <= 4 && cache_x >= (-4)){
    cache_x = 0;
  }
  Serial.print("X");
  Serial.println(cache_x );
  Serial.print("Y");
  int cache_y = analogRead(Y_accis_pin) - 512;
  cache_y = cache_y / 8;

  if(cache_y <= 4 && cache_y >= (-4)){
    cache_y = 0;
  }
  
  else if(cache_y < (-4)){
    cache_y = cache_y - 36;
  }
  
  else if(cache_y > 4){
    cache_y = cache_y +36;
  }


  
  Serial.println(cache_y);
  delay(100);
  
}
