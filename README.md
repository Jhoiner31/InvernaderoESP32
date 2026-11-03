# InvernaderoESP32
Firmware en mycropython para la ESP32 que mide temperatura, humedad del aire, humedad del suelo y la luz, control de riego, ventilacion e iluminación en modo automático o manual. Esta se comunica mediante MQTT con una interfaz de escritorio en Python (Para el parcial 3)

Simulacion en wokwi: https://wokwi.com/projects/479639981254297601

# Componentes

|-----------------------|---------|-------------------------------|
| Elemento              | Pin     | Funcion                       |
|-----------------------|---------|-------------------------------|
| DHT22                 | GPIO 4  | Temperatura y humedad del aire|
| Sensor de suelo (ADC) | GPIO 34 | Humedad del sustrato          |
| LDR (ADC)             | GPIO 35 | Luz ambiente                  |
| Sensor de nivel       | GPIO 32 | Proteccion de bomba en seco   |
| Relé y bomba          | GPIO 26 | Riego                         |   
| Relé y ventilador     | GPIO 27 | Ventilación                   |
| led                   | GPIO 25 | Iluminación                   |
| Buzzer                | GPIO 14 | Alerta local                  |
|-----------------------|---------|-------------------------------|

# Estructura

config.py 

Sensores.py

actuadores.py

control.py

comunicacion.py

main.py