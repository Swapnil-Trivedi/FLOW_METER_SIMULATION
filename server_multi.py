#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:55:45 2020

@author: swapnil
"""

"""
importing necessary modules for development.
importing socket for socket creation
importing time to provide with system delay
importing pickle for converting objects to byte stream
importing threading module to create and handle threads
"""

import socket 
import pickle
import time
import threading

"""
Defining Host IP and Standard Port value to bind 
This is meant for server's static port and ip
"""

host="127.10.10.10"
port=8071

#making a socket object of type TCP(STREAM) and Inet Family
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#setting socket config to reuse address
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#binding port and listeninig
server.bind((host,port))
server.listen(5)

#creating list of clients to keep track on incoming connections
clients=[]
"""
Transmission function is used to connect to a client and recieve it's data
it is used to inform the client about successfully adding device

"""
def transmission(conn,addr,user_data,device):
    data=pickle.loads(user_data)
    print(f"Reciving Data fron Device {device}")
    print("\nDEVICE NAME : ",data["dname"],"\nDEVICE TYPE :",data["dtype"],"\nDEVICE SRNO :",data["dsr"])
    message="Device added Succesfully !\nRestart Connection to Transmitt Data"
    print(message)
    conn.sendto(message.encode(),addr)

"""
For a new user a set of instructons are sent to the cliennt on accepting and successfully
accepting data the connection is sent to transmission for reseting and transfering data
the flag is sent to client which can be true or false based on which client respond
the client's IP is saved to the client list and is kept track of
i am not using any database to keep record to keep the data flow simple and 
for keeping it simple 
""" 
def user(conn,addr,device):
        flag="true"
        flag=flag.encode()
        conn.sendto(flag,addr)
        print("Asking New Device for Details...")
        message="Getting Details: DEVICE NAME  DEVICE TYPE  DEVICE SERIAL NO."
        conn.sendto(message.encode(),addr)
        data=conn.recv(1024)
        message="Adding Device.....\n"
        print(message)
        conn.sendto(message.encode(),addr)
        clients.append(device)
        message="Redirecting for Data Transmission...."
        conn.sendto(message.encode(),addr)
        transmission(conn,addr,data,device)
   
"""
Old user or the clients who's IP is in client list is sent to this function where
it is redirected to function read_data where a simple addition of data takes place
"""    
def old_user(conn,addr,device):
       try:
        flag="false"
        flag=flag.encode()
        conn.sendto(flag,addr)
        read_data(conn,addr,device)
       except socket.error as e:
        print(e)
        conn.close()
"""
The read_data functi0on simply takes two number from client and 
perform a simple sum and return back two the client
"""        
def read_data(conn,addr,device):        
        print(f"Device Already Registered\nAccepting Data From ....{device}")
        try:
           while True:   
            data=conn.recv(1024)
            data=pickle.loads(data)
            sumc=data[0]+data[1]
            print(f"Data for Device {device} SUM is : {sumc}") 
            mssg=pickle.dumps(sumc)
            conn.sendto(mssg,addr)
            time.sleep(2)
        except EOFError:
               print("Connection Terminated by Device....")
        
    
"""
action is used to check clients in the list and carry out further 
actions once the connectioon is established
"""
def action(conn,addr):
    device=conn.recv(1024)
    device=device.decode()
    if device not in clients:
          user(conn,addr,device)
    elif device in clients:
        old_user(conn,addr,device)
    print(f"\nWaiting for connection on {host}:{port}.....")
    
    
"""
creating a simple thread to handle multiple connections and accepting
connections from clients
"""    
if __name__=='__main__':   
 print(f"Waiting for connection on {host}:{port}.....")
 try:
  while True:
    conn,addr=server.accept()
    th1=threading.Thread(target=action,args=[conn,addr])
    th1.start()
  th1.join()
    

    
 except (socket.error,KeyboardInterrupt):
    print("\nERROR ON SERVER SIDE!!!!\nClosing Socket")
 server.close()    
