#include <Wire.h>
#include <Adafruit_INA219.h>

// Definisi pin
#define SDA_PIN 16
#define SCL_PIN 17
#define BUZZER_PIN 4

// Tentukan batas arus tertinggi untuk memicu OVERLOAD (dalam mA)
const float BATAS_ARUS = 10.0; 

Adafruit_INA219 ina219;

void setup() {
  Serial.begin(115200);
  
  // Inisialisasi pin I2C
  Wire.begin(SDA_PIN, SCL_PIN);
  
  // Inisialisasi pin Buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); // Pastikan buzzer mati di awal

  Serial.println("Memulai inisialisasi Sensor INA219...");
  
  if (!ina219.begin()) {
    Serial.println("Gagal menemukan INA219!");
    while(1) { delay(10); }
  }
}

void loop() {
  // Membaca data dari sensor
  float arus_mA = ina219.getCurrent_mA();
  float tegangan_V = ina219.getBusVoltage_V();
  float daya_mW = ina219.getPower_mW();

  // Menampilkan nilai ke Serial Monitor
  Serial.print("Tegangan: "); Serial.print(tegangan_V); Serial.println(" V");
  Serial.print("Arus    : "); Serial.print(arus_mA); Serial.println(" mA");
  Serial.print("Daya    : "); Serial.print(daya_mW); Serial.println(" mW");

  // ==========================================
  // LOGIKA PENGONDISIAN (STATUS & BUZZER)
  // ==========================================
  if (arus_mA > BATAS_ARUS) {
    // Jika arus lebih besar dari batas
    Serial.println("Status  : OVERLOAD !!!");
    digitalWrite(BUZZER_PIN, HIGH); // Nyalakan Buzzer
  } else {
    // Jika kondisi aman (arus di bawah batas)
    Serial.println("Status  : NORMAL");
    digitalWrite(BUZZER_PIN, LOW);  // Matikan Buzzer
  }
  
  Serial.println("-------------------------");
  delay(1000); 
}