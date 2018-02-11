# ServerClass.py
# references:
# https://pythonspot.com/python-network-sockets-programming-tutorial/
# https://docs.python.org/3.4/howto/sockets.html

import socket
import threading
import select
import sys

class ServerClass:
     def __init__(self, ip_address='127.0.0.1', tcp_port=23):
          self.TCP_IP = '127.0.0.1'
          self.TCP_PORT =  tcp_port  #23:telnet  502: modbus
          self.BUFFER_SIZE = 50  # Normally 1024, but we want fast response
           
          self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.s.bind(('', self.TCP_PORT))
          self.s.listen()
          self.s.settimeout(0.2)
          self.count=0
          self.keep_going = True
          self.connections = []
          self.threads = []
          self.notify = []
          self.addr = "0"
          threading.Thread(target = self.checking_thread, name="checking_thread" ).start()
          #print('exit init')

     def connect_thread(self, conn):
          #print('Connection address: ', str(self.addr))
          print("starting connect_thread " + threading.currentThread().getName())
          self.connections.append(conn)
          data_string = ""
          while True:
               try:
                    conn.setblocking(0)
                    ready = select.select([conn], [], [], 1)

                    if ready[0]:
                         data = conn.recv(self.BUFFER_SIZE)
                         if not data:
                              break
                         #print(threading.currentThread().getName()+ " received data:", data)
                         if not self.keep_going:
                              print("exit " + threading.currentThread().getName())
                              break
                         #conn.send(data)  # echo
                         data_string = data_string + data.decode('utf-8')
                         if '\n' in data_string:
                              self.notify_rec_data(conn, data_string)
                              data_string = ""
                    if not self.keep_going:
                         break
               except:
                    print("exception "+ threading.currentThread().getName())
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("connect_thread Unexpected error:", sys.exc_info()[0])
                    print("connect_thread line error: " + str(exc_tb.tb_lineno))
                    break
               
          if conn in self.connections:
               self.connections.remove(conn)
          conn.close()
          print("exit connect_thread " + threading.currentThread().getName())

     def checking_thread(self):
          #print('start checking_thread')
          while True:
               #print('x')
               if not self.keep_going:
                    #print('y')
                    break
               try:
                    #print('wait for connection')
                    conn, self.addr = self.s.accept()
                    #print('got connection')
                    self.connections.append(conn)
                    self.count = self.count + 1
                    thread_name = "thread"+str(self.count)
                    #print('start thread')
                    thrd = threading.Thread(target = self.connect_thread,name=thread_name, args=(conn,) )
                    self.threads.append(thrd)
                    thrd.start()
               except socket.timeout:
                    pass
                    #print('except socket.timeout')
               except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("Unexpected error:", sys.exc_info()[0])
                    print("line error: " + str(exc_tb.tb_lineno))
                    
          print('exit checking_thread')


     def send(self, connection, data):
          #print('send' + str(data))
          connection.send(data)

     def get_connections(self):
          #print('get_connectiions')
          return self.connections
     
     def get_threads(self):
          #print('get_connectiions')
          return self.threads

     def register_to_rec_data(self, meth):
          #print('register_to_rec_data')
          if meth not in self.notify:
               self.notify.append(meth)
               
     def unregister_to_rec_data(self, meth):
          #print('unregister_to_rec_data')
          if meth in self.notify:
               self.notify.remove(meth)
          
     def notify_rec_data(self, connection, data):
          #print('notify_rec_data')
          for meth in self.notify:
               meth(connection, data)

if __name__ == '__main__':
     # connect to this with "telnet 127.0.0.1"
     # press single q to quit
     SC = ServerClass()
     endprogram = False
     
     def rec_func(con, dta):
          global SC
          global endprogram
          print("receive data: " + dta)
          SC.send(con, dta.encode()) # echo
          if dta.strip() == "q":
               SC.send(con, "EXIT!!!".encode())
               endprogram = True
               
     def rec_func2(con, dta):
          global SC
          global endprogram
          print("receive data: " + str(dta.decode('utf-8')))
          SC.send(con, dta) # echo
          if dta == b'q':
               SC.send(con, "EXIT!!!".encode())
               endprogram = True

     SC.register_to_rec_data(rec_func)

     #t=threading.Thread(target = SC.checking_thread, name="checking_thread" )
     #t.start()

     while not endprogram:
          pass
     
     SC.keep_going = False
     #t.join()

     thrds = SC.get_threads()
     for item in thrds:
          print("wait for end of thread: " + str(item))
          item.join()

     print("program done")
