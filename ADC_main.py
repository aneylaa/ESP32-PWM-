from machine import ADC, Pin
import time

# 1. Inisialisasi Pin & ADC (GPIO 34)
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)       # Rentang tegangan 0 - 3.3V
adc.width(ADC.WIDTH_12BIT)     # Resolusi 12-bit (0 - 4095)

# Konstanta
VREF = 3.3
ADC_RES = 4095
R_TOTAL = 10000.0  # Potensiometer 10k Ohm

# 2. Inisialisasi Pesan Awal (Baudrate Wokwi otomatis 115200)
print("--- Simulasi ADC ESP32 Siap ---")

# 3, 4, 5. Pembacaan & Konversi Berulang
while True:
    # Baca nilai mentah ADC
    adc_raw = adc.read()
    
    # Hitung Tegangan & Hambatan
    voltage = (adc_raw / ADC_RES) * VREF
    resistance = (adc_raw / ADC_RES) * R_TOTAL
    
    # Cetak ke Serial Monitor secara rapi
    print(f"Raw ADC: {adc_raw:<4} | Tegangan: {voltage:.2f} V | Hambatan: {resistance:>5.0f} Ohm")
    
    # Delay 500ms tiap siklus
    time.sleep(0.5)