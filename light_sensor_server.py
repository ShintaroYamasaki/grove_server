from datetime import datetime
import socket
import time
import grovepi

light_sensor = 1
grovepi.pinMode(light_sensor,"INPUT")

address = ('0.0.0.0', 4011)
max_size = 1000

print('Starting the service at', datetime.now())
print('Wating for a client to call')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen(5)

while True:
  client, addr = server.accept()
  data = client.recv(max_size)

  print('At', datetime.now(), client, 'said', data)

  if data.decode('utf-8') == 'read':
    try:
      sensor_value = grovepi.analogRead(light_sensor)
      resistance = (float)(1023 - sensor_value) * 10 / sensor_value
      print(str(resistance) + ' K')
      client.sendall(str(int(resistance)).encode('utf-8'))
    except KeyboardInterrupt:
      break
    except IOError:
      print ("Error")
  elif data.decode('utf-8') == 'write':
    data = client.recv(max_size)
    print (data)
  client.close()
  time.sleep(.5)

server.close()

