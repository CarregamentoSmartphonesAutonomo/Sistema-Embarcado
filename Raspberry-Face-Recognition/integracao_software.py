import socket
import bib_rasp
import RPi.GPIO as gpio
import sys

# GPIO configuring
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)

# Socket configuring
s = socket.socket()
host = '10.3.141.1' #ip of raspberry pi
port = 4141
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()

  try:
    print ('Got connection from',addr)
    # Receive the commands command in small chunks and retransmit the results
    while True:
      command = c.recv(32)
      command = command.rstrip() #remove last character
      print ('received', command)
      if command:
        print ('go to step', command)
        if command == '1':
          result = "1\n"
          result = result + bib_rasp.checar_cabines() + "\n"
          c.sendall(str(result))
          print 'Result: ', result
        elif command == '2':
          face_id = c.recv(32)
          face_id = face_id.rstrip()
          result = bib_rasp.obter_fotos(face_id)
          c.sendall(str(result))
        elif command == '3':
          data = c.recv(32)
          data = face_id.rstrip()
          name = data[0]
          face_id = data[1]
          cab_id = data[2]
          result = bib_rasp.colocar_na_cabine(name,face_id,cab_id)
          c.sendall(str(result))
        elif command == '4':
          cab_id = c.recv(32)
          cab_id = face_id.rstrip()
          result = bib_rasp.confirmar_fechamento(cab_id)
          c.sendall(str(result))
        elif command == '5':
          cab_id = c.recv(32)
          cab_id = face_id.rstrip()
          result = bib_rasp.remover_smartphone(cab_id)
          c.sendall(str(result))
        elif command == 'f':
          print('Terminando programa')
          gpio.cleanup()
          sys.exit()
        else:
          print('Comando nao encontrado')
          break
      else:
        print 'no more command from', addr
        gpio.cleanup()
        break

  finally:
    # Clean up the c
    print('Terminando a comunicacao com o app')
    c.close()