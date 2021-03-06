#define PUMP_PIN 7                                                                                                                      
#define RASP_ONE 6                                                                                                                      
#define RASP_TWO 4
#define BUZZER_PIN 9

void setup(){
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(RASP_ONE, OUTPUT);
  pinMode(RASP_TWO, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(RASP_ONE, 0);
  digitalWrite(RASP_TWO, 0);
  digitalWrite(PUMP_PIN, 0);
  Serial.begin(9600);
}

void loop(){
  digitalWrite(PUMP_PIN, checkSoilSensor());
//  Serial.println(checkPirSensor());
  if(checkPirSensor() >= 0){
    //digitalWrite(RASP_TWO, 1);
    tone(BUZZER_PIN, 2000, 1000);
    delay(4000);
  } else {
    digitalWrite(RASP_TWO, 0);
  }
  delay(100);
}
