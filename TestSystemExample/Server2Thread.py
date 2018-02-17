# server.py
# telnet 127.0.0.1 62.
# https://pythonspot.com/python-network-sockets-programming-tutorial/
# https://docs.python.org/3.4/howto/sockets.html

import socket
import threading
import select
 
TCP_IP = '127.0.0.1'
TCP_PORT = 80 #
#TCP_PORT = 23 # telnet
#TCP_PORT = 502 # modbus
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen()
s.settimeout(0.2)
count=0
keep_going = True


def connect_thread(conn):
     global keep_going
     print('Connection address:', addr)
     while 1:
          try:
               conn.setblocking(0)
               ready = select.select([conn], [], [], 1)

               if ready[0]:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                         break
                    print(threading.currentThread().getName()+ " received data:", data)
                    if data == b'\x03':
                         keep_going = False
                         print("exit " + threading.currentThread().getName())
                         break
                    conn.send(data)  # echo
               if not keep_going:
                    break
          except:
               print("exception "+ threading.currentThread().getName())
               break
     conn.close()

         
while True:
     if not keep_going:
          break
     try:
          conn, addr = s.accept() 
          count = count + 1
          thread_name = "thread"+str(count)
          threading.Thread(target = connect_thread,name=thread_name, args=(conn,) ).start()
     except socket.timeout:
          pass
     except:
          pass
     
print("program done")
     


