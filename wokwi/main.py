# Dependências
import time # Usado para pausar a aplicacao
import dht # Usado para o sensor de temperatura e umidade
from machine import Pin, SoftI2C, reset # Uso do ESP32
from umqtt.simple import MQTTClient # Enviar dados para o servidor 
from machine_i2c_lcd import I2cLcd # Interagir com o Display
from utilsdefs import (
    play_note, log_display,
    send_data, connect_wifi,
    show_info_on_display, show_time_on_display
) # Funções Separadas para melhor organização do código

# Parâmetros da conexâo do WI-FI
WIFI_LOGIN = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Parâmetros da conexâo do MQTT
MQTT_CLIENT_ID = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC"
MQTT_BROKER = "mqtt.beebotte.com"
MQTT_USER = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC"
MQTT_PASSWORD = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC"
MQTT_BASE_TOPIC = "trip13601"
MQTT_PORT = 8883

# Parâmetros do I2C (usado para simplificar a estrutura) e o LED LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
SDA_PIN = Pin(21)
SCL_PIN = Pin(22)

# Parâmetros do Sensor de Movimentacao
MOTIONSENSOR1_PIN = Pin(34, Pin.IN) # Sensor da Esquerda (Entrada de Passageiros)
MOTIONSENSOR2_PIN = Pin(35, Pin.IN) # Sensor da Direita (Saida de Passageiros)

# Parâmetros do Sensor de Temperatura e Umidade
DHT22_PIN = Pin(23)

# Parâmetros do Sensor de GPS
GPS_OUT_PIN = Pin(5)
GPS_IN_PIN = Pin(18)

# Parâmetros do led RGB
LED_R_PIN = Pin(25, Pin.OUT) # Vermelho
LED_G_PIN = Pin(33, Pin.OUT) # Verde
LED_B_PIN = Pin(32, Pin.OUT) # Azul

# Parâmetros do buzzer
BUZEER_PIN = 5

# Inicializar LCD
i2c = SoftI2C(sda=SDA_PIN, scl=SCL_PIN, freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Inicializar GPS
altitude = -27.631182
longitude = -48.641013

# Inicializar contagem de passageiros
motion_1_status = False
motion_2_status = False
persons_in = 0
persons_out = 0
persons_total = 0

# Guardar registro da última medicão, para não enviar dados duplicados
prev_temperature = -1
prev_humidity = -1
prev_persons_in = -1
prev_persons_out = -1
prev_persons_total = -1

# Acionar catch em caso de erros
try:
  # Inicializar LED
  # Pinos configurados em LOW são acessos. Acender LED branco (Todas as cores)
  LED_R_PIN.off()
  LED_G_PIN.off()
  LED_B_PIN.off()

  # Inicializar Sensor de Temperatura
  sensor = dht.DHT22(DHT22_PIN)

  # Inicializar Wi-Fi
  log_display(lcd, "Iniciar WI-FI...")
  play_note(BUZEER_PIN, lcd)
  connect_wifi(WIFI_LOGIN, WIFI_PASSWORD)
  log_display(lcd, "Wifi Conectado!")
  play_note(BUZEER_PIN, lcd)

  # Inicializar conexão MQTT
  log_display(lcd, "Conectar MQTT...")
  play_note(BUZEER_PIN, lcd)
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, port=MQTT_PORT, ssl=True)
  client.connect()
  log_display(lcd, "MQTT conectado!")
  play_note(BUZEER_PIN, lcd)

  while True:

    # Variavel para verificar se algo mudou no display
    changed = False

    # Efetuar a medicão
    sensor.measure()

    # Temperatura
    temperature = sensor.temperature()

    # Umidade
    humidity = sensor.humidity()

    # Entrada de Passageiros
    readMotion1 = MOTIONSENSOR1_PIN.value()
    if(readMotion1 == 1):
      if not motion_1_status:
        changed = True
        persons_in += 1
        motion_1_status = True
    else:
      if motion_1_status:
        motion_1_status = False

    # Saída de Passageiros
    readMotion2 = MOTIONSENSOR2_PIN.value()
    if(readMotion2 == 1):
      if not motion_2_status:
        changed = True
        persons_out += 1
        motion_2_status = True
    else:
      if motion_2_status:
        motion_2_status = False
    
    # Total de Passageiros
    persons_total = max(persons_in - persons_out, 0)

    # Enviar dados da temperatura
    if temperature != prev_temperature:
      # Enviar novos dados ao servidor MQTT
      changed = True
      prev_temperature = temperature
      log_display(lcd, "Enviando dados de temperatura...")
      play_note(BUZEER_PIN, lcd)
      send_data(client, MQTT_BASE_TOPIC, "temperature", temperature)

      # Acrender led vermelho em caso de calor, azul em caso de frio e verde temperatura normal
      if temperature < 15:
        LED_R_PIN.on()
        LED_G_PIN.on()
        LED_B_PIN.off()
      elif temperature > 26:
        LED_R_PIN.off()
        LED_G_PIN.on()
        LED_B_PIN.on()
      else:
        LED_R_PIN.on()
        LED_G_PIN.off()
        LED_B_PIN.on()
    #

    # Enviar dados da Umidade
    if prev_humidity != humidity:
      # Enviar novos dados ao servidor MQTT
      changed = True
      prev_humidity = humidity
      log_display(lcd, "Enviando dados de umidade...")
      play_note(BUZEER_PIN, lcd)
      send_data(client, MQTT_BASE_TOPIC, "humidity", humidity)
    #

    if prev_persons_in != persons_in:
      # Enviar novos dados ao servidor MQTT
      changed = True
      prev_persons_in = persons_in
      log_display(lcd, "Enviando dados de Passageiros...")
      play_note(BUZEER_PIN, lcd)
      send_data(client, MQTT_BASE_TOPIC, "persons_in", persons_in)
    #

    if prev_persons_out != persons_out:
      # Enviar novos dados ao servidor MQTT
      changed = True
      prev_persons_out = persons_out
      log_display(lcd, "Enviando dados de Passageiros")
      play_note(BUZEER_PIN, lcd)
      send_data(client, MQTT_BASE_TOPIC, "persons_out", persons_out)
    #

    if prev_persons_total != persons_total:
      # Enviar novos dados ao servidor MQTT
      changed = True
      prev_persons_total = persons_total
      log_display(lcd, "Enviando dados de Passageiros")
      play_note(BUZEER_PIN, lcd)
      send_data(client, MQTT_BASE_TOPIC, "persons_total", persons_total)
    #

    # Mostrar na tela LCD a nova medição
    if changed:
      show_info_on_display(lcd, temperature, humidity, altitude, longitude, persons_in, persons_out)

    # Aguardar 1 segundo
    show_time_on_display(lcd)
    time.sleep(1)

# Em caso de erros (como de conexão), reiniciar o sistema
except OSError as e:
  text = str(e)
  print("ERRO:")
  print(text)
  lcd.clear()
  log_display(lcd, "Erro interno, reiniciando sistema...")
  repetitions = 6
  for _ in range(repetitions):
      play_note(BUZEER_PIN, lcd)
  time.sleep(5)
  reset()