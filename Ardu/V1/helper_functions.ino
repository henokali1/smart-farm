int checkPirSensor(){
  if(analogRead(A0) < 800){
    Serial.println("1,p,");    
    return(0);
  } else if(analogRead(A1) < 800){
    Serial.println("2,p,");   
    return(1);
  } else if(analogRead(A2) < 800){
    Serial.println("3,p,");   
    return(2);
  } else if(analogRead(A3) < 800){
    Serial.println("4,p,");   
    return(3);
  } else{
    return(-1);
  }
}

boolean checkSoilSensor(){
  return(analogRead(A4) > 500);
}
