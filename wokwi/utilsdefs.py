import network # Usado para conectar o WI-FI
from machine import PWM, Pin # Funçôes do ESP32
from time import sleep, time # Pausar aplicaçâo e pegar hora atual
import ujson # Usado para enviar dados em JSON no servidor
import utime # Usado para converter datas e horas

# Método para acionar o buzzer
def play_note(pin, lcdForBlink = None, freq=440, sleepduration=0.1):
  if lcdForBlink is not None:
    lcdForBlink.backlight_off()
  audio = PWM(Pin(pin), 1)
  audio.freq(freq)
  audio.duty(512)
  sleep(sleepduration)
  audio.deinit()
  if lcdForBlink is not None:
    lcdForBlink.backlight_on()
#

# Método para simplificar a mostragem de uma mensagem
def log_display(lcd, message):
  lcd.clear()
  lcd.move_to(1,1)
  lcd.putstr(message)
#

# Método para simplificar o envio de dados para o MQTT
def send_data(client, base_topic, topic, data):
  client.publish(base_topic + "/" + topic, ujson.dumps({
    "data": data,
    "write": True,
  }))
#

# Método para conectar no WI-FI
def connect_wifi(login, password):
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(login, password)
  while not sta_if.isconnected():
    sleep(0.1)
#

# Método para formatar hora
def format_timestamp(timestamp):
  # Convert the timestamp to a local time tuple
  time_tuple = utime.localtime(timestamp)
  # Format time in HH:MM:SS format
  formatted_time = "{:02}:{:02}:{:02}".format(time_tuple[3], time_tuple[4], time_tuple[5])
  return formatted_time
#

# Método para formatar coordenadas
def format_coordinate(coord_str):
    # Verificar se já contém ponto decimal
    if '.' not in coord_str:
        coord_str += '.'
    # Completar com zeros à direita até atingir 20 caracteres
    while len(coord_str) < 20:
        coord_str += '0'
    # Substituir o ponto por uma vírgula
    coord_str = coord_str.replace('.', ',')
    return coord_str
#

# Método para formatar números com 3 digitos
def format_persons(persons):
    persons_str = str(persons)
    # Adicionar zeros à esquerda até o comprimento ser 3
    while len(persons_str) < 3:
        persons_str = '0' + persons_str
    return persons_str
#

# Método para demonstrar informações no Display
def show_info_on_display(lcd, temperature, humidity, lat, lng, persons_in, persons_off):
  lcd.clear()
  lcd.move_to(0,0)
  lcd.putstr(str(temperature) + "C")
  lcd.move_to(6,0)
  lcd.putstr(str(humidity) + "%")
  lcd.move_to(12,0)
  lcd.putstr(format_timestamp(time()))
  lcd.move_to(0,1)
  latstr = format_coordinate(str(lat))
  lngstr = format_coordinate(str(lng))
  lcd.putstr("Lat: " + latstr)
  lcd.move_to(0,2)
  lcd.putstr("Lng: " + lngstr)
  lcd.move_to(0,3)
  lcd.putstr("Entrd. " + format_persons(persons_in) + " Said. " + format_persons(persons_off))
#

# Método para atualizar somente a hora no display
def show_time_on_display(lcd):
  lcd.move_to(12,0)
  lcd.putstr(format_timestamp(time()))