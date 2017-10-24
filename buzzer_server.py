from datetime import datetime
import socket
import time
import grovepi

buzzer = 2

grovepi.pinMode(buzzer,"OUTPUT")

address = ('0.0.0.0', 4002)
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
    client.sendall('0'.encode('utf-8'))
  elif data.decode('utf-8') == 'write':
    data = client.recv(max_size)
    if int(data) == 1:
      try:
        grovepi.digitalWrite(buzzer,1)
        print ('start')
        time.sleep(1)
        grovepi.digitalWrite(buzzer,0)
        print ('stop')
      except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        break
      except IOError:
        print ("Error")
  client.close()

server.close()

