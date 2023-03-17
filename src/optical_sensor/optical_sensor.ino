const int S1 = 34;
const int S2 = 35;

void setup() {
  pinMode (S1, INPUT);
  pinMode (S2, INPUT);
  Serial.begin(9600);
}
void loop() {
  Serial.print(digitalRead(S1));
  Serial.print(" ");
  Serial.println(digitalRead(S2));
  delay(100);
}
