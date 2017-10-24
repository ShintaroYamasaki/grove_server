from datetime import datetime
import socket
import time
import grovepi

potentiometer = 2
grovepi.pinMode(potentiometer,"INPUT")

address = ('0.0.0.0', 4012)
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
      sensor_value = grovepi.analogRead(potentiometer)
      voltage = round((float)(sensor_value) * 5 / 1023, 2)
# 0 to 300
      degree = int(round((voltage * 300) / 5, 2))
      print(str(degree))
      client.sendall(str(degree).encode('utf-8'))
    except KeyboardInterrupt:
      break
    except IOError:
      print ("Error")
  elif data.decode('utf-8') == 'write':
    data = client.recv(max_size)
    print (data)
  client.close()

server.close()

