// https://microkontroller.ru/esp32-projects/ispolzovanie-shirotno-impulsnoj-modulyaczii-shim-v-esp32/

// пины моторшилда
const int M1 = 18;  // 18 corresponds to GPIO16
const int M2 = 5;
// устанавливаем настройки формирования ШИМ
const int Hz = 15000; // частота ШИМ (для моторов рекомендуют не менее 20 кГц)
const int M1Channel = 0; // создаем канал для первого ШИМ
const int M2Channel = 1; // создаем канал для второго ШИМ
const int bits = 8; // разрядность (для управления) ШИМ
const int dt = 20; // скорость изменения скорости моторов (для теста)

void setup(){
  // настраиваем ШИМ в соответствии с ранее указанными настройками
  ledcSetup(M1Channel, Hz, bits);
  ledcSetup(M2Channel, Hz, bits);
  // назначаем контакт и канал для формирования ШИМ
  ledcAttachPin(M1, M1Channel);
  ledcAttachPin(M2, M2Channel);
  // переключаем ШИМы в ноль(чтобы все стояло)
  ledcWrite(M1Channel, 0);
  ledcWrite(M2Channel, 0);
}
void loop(){
  // крутим мотор вперед (ускорение)
  for (int i = 0; i<255; i++) {
    ledcWrite(M1Channel, i);
    delay(dt);
  }
  // крутим мотор вперед (торможение)
  for (int i = 255; i>0; i--) {
    ledcWrite(M1Channel, i);
    delay(dt);
  }
  // крутим мотор назад (ускорение)
  for (int i = 0; i<255; i++) {
    ledcWrite(M2Channel, i);
    delay(dt);
  }
  // крутим мотор назад (торможение)
  for (int i = 255; i>0; i--) {
    ledcWrite(M2Channel, i);
    delay(dt);
  }
}
