int checkPirSensor(){
  if(analogRead(A0) < 800){
    return(0);
  } else if(analogRead(A1) < 800){
    return(1);
  } else if(analogRead(A2) < 800){
    return(2);
  } else if(analogRead(A3) < 800){
    return(3);
  } else{
    return(-1);
  }
}

boolean checkSoilSensor(){
  int val = analogRead(A4);
  Serial.println("Soil: " + String(val));
  return(val < 817);
}
