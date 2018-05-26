import socket
import retirada_de_smartphone

s = socket.socket()
host = '10.3.141.1' #ip of raspberry pi
port = 4141
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()

   try:
        print ('Got connection from',addr)
        # Receive the commands data in small chunks and retransmit the results
        while True:
            data = connection.recv(16)
            print ('received "%s"' % data)
            if data:
                print ('go to step "%s"' % data)

                if c == 1:
                  result = remove_smartphone()
                  connection.sendall(result)
                elif c == 2:
                  c.send('Running functionality 2')
                else:
                  c.close()
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()
