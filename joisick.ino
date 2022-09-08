

int X_accis_pin = A0;
int Y_accis_pin = A1;


void setup() {
  //Setup Serielle Komunikation
  Serial.begin(115200);

  //Setup pins
  pinMode(X_accis_pin, INPUT):
  pinMode(Y_accis_pin, INPUT);
  
}



void loop() {
  Serial.print("X:");
  Serial.print(analogRead(X_accis_pin));
  Serial.print("\nY:");
  Serial.print(analogRead(Y_accis_pin));
  Serial.print("\n");
  
  
}
