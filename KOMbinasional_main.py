from machine import ADC, Pin
import time

# 1. Inisialisasi Potensiometer (GPIO 34)
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)       # Batas ukur tegangan 0 - 3.3V
adc.width(ADC.WIDTH_12BIT)     # Resolusi 12-bit (0 - 4095)

# 2. Inisialisasi Output LED (Terhubung Seri dengan Resistor 220 Ohm)
led_merah = Pin(18, Pin.OUT)
led_kuning = Pin(19, Pin.OUT)
led_hijau = Pin(21, Pin.OUT)

# 3. Inisialisasi Push Button (Tombol Darurat - Pull-Up Internal)
# Nilai 1 (HIGH) = Tidak ditekan | Nilai 0 (LOW) = Ditekan
button = Pin(4, Pin.IN, Pin.PULL_UP)

# Batas Ambang Tegangan (Thresholds)
V_LOW_MAX = 1.1   # Tegangan Rendah : 0.0V - 1.1V
V_MID_MAX = 2.2   # Tegangan Sedang : 1.1V - 2.2V (Tinggi: > 2.2V)

print("--- Sistem Terintegrasi ADC + LED + Emergency Button Siap ---")

while True:
    # Read status tombol darurat
    btn_pressed = (button.value() == 0)
    
    # Read nilai ADC dan hitung tegangan
    adc_raw = adc.read()
    voltage = (adc_raw / 4095.0) * 3.3

    # LOGIKA KOMBINASI & PRIORITAS:
    if btn_pressed:
        # KONDISI DARURAT: Semua LED WAJIB mati
        led_merah.value(0)
        led_kuning.value(0)
        led_hijau.value(0)
        status = "EMERGENCY! Semua LED MATI"
    else:
        # KONDISI NORMAL: LED menyala berdasarkan level tegangan
        if voltage < V_LOW_MAX:
            led_merah.value(1)
            led_kuning.value(0)
            led_hijau.value(0)
            status = "Level Rendah -> LED MERAH NYALA"
        elif voltage < V_MID_MAX:
            led_merah.value(0)
            led_kuning.value(1)
            led_hijau.value(0)
            status = "Level Sedang -> LED KUNING NYALA"
        else:
            led_merah.value(0)
            led_kuning.value(0)
            led_hijau.value(1)
            status = "Level Tinggi -> LED HIJAU NYALA"

    # Tampilkan pembacaan ke Serial Monitor
    print(f"ADC Raw: {adc_raw:<4} | Volt: {voltage:.2f}V | Button: {'TEKAN' if btn_pressed else 'LEPAS'} | Status: {status}")
    
    # Delay siklus pembacaan 100 ms
    time.sleep(0.1)