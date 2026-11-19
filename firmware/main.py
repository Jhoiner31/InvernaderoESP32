import time
import config
import sensores
import actuadores
import control
import mqtt_cliente

print("Conectando WiFi...")
wifi_ok = mqtt_cliente.conectar_wifi()
print("WiFi:", wifi_ok)

if wifi_ok:
    print("Broker:", mqtt_cliente.conectar_broker())
    mqtt_cliente.suscribirse()

estado_anterior = None

while True:
    temp, hum_aire = sensores.leer_dht()
    hum_suelo = sensores.leer_suelo()
    luz = sensores.leer_luz()

    mqtt_cliente.revisar_mensajes()
    control.actualizar(temp, hum_suelo, luz)

    alertas = control.revisar_alertas(temp, hum_suelo)
    for alerta in control.alertas_nuevas(alertas):
        print("ALERTA:", alerta)
        mqtt_cliente.publicar_alerta(alerta)
        actuadores.pitido(0.5, 2000)

    mqtt_cliente.publicar_sensores(temp, hum_aire, hum_suelo, luz)

    estado_actual = (actuadores.estado(), control.modo)
    if estado_actual != estado_anterior:
        mqtt_cliente.publicar_actuadores(*estado_actual)
        estado_anterior = estado_actual

    print("Temp:", temp, "| Aire:", hum_aire, "| Suelo:", hum_suelo,
          "| Luz:", luz, "| Modo:", control.modo)
    time.sleep(config.INTERVALO_LECTURA)