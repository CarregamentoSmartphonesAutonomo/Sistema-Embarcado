import socket
import retirada_de_smartphone

s = socket.socket()
host = '10.3.141.1' #ip of raspberry pi
port = 4141
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print ('Got connection from',addr)
  c.send('Thank you for connecting')

  if c == 1:
    remove_smartphone()
  elif c == 2:
    c.send('Running functionality 2')
  else:
    c.close()
