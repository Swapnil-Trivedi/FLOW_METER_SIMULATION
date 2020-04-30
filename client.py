#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:28:52 2020

@author: swapnil
"""
"""
Well our client programm is pretty simple we first aim to establish a conection
and sending two random numbers so our server can add them and send them back
"""

import pickle
import socket
import time

"""
giving our client the permanent ip of the server and port
also providing our client with a unique ip since we're on a local device
"""
port=8071
device_ip="127.0.0.1"
device=device_ip.encode()
host="127.10.10.10"

"""
giving unique name and traits to our client so it can be identified as a device
"""
dname="FLX25"
dtype="Flow_Meter"
dsr="TLSSX258NC1235"

data={
      "dname":dname,
      "dtype":dtype,
      "dsr":dsr,
      }
#converting data dictionary to byte stream
data=pickle.dumps(data)
#creating our client socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#setting a default timeout for our client so it does not keep waiting
client.settimeout(5)

#diving to the main client code:
try:
   #connecting to host
   client.connect((host,port))
   #sending device data
   client.send(device)
   message=client.recv(1024)
   message=message.decode()
   #if flag from server is true we declare a new user else it is considered as and old user
   if(message=="true"):
      message=client.recv(1024)
      print(message.decode())
      client.send(data)
      message=client.recv(1024)
      print(message.decode())
      message=client.recv(1024)
      print(message.decode())
   #if a new device is registered we ask it to restart connection so it can transmit
   #if the user is already registered we simply start transmitting    
   else:
       print("Device already Registered\nConnected To : ",host,"Sending Data.... ")
       #selecting two random numbers to transmit
       a,b=15,25
       try:
        while True:
         data=[a,b]
         data=pickle.dumps(data)
         client.send(data)
         time.sleep(1)
         mssg=client.recv(1024)
         mssg=pickle.loads(mssg)
         print(f"Sum of {a}+{b} is : {mssg}")
         a+=5
         b+=10
        print("Data Sent Succesfully")
        client.close()
       #we want the client to keep sending data always but stil if say someone wants to disconnect we give a keyboardinterrupt exception 
       except KeyboardInterrupt:
           print("\nTERMINATED BY CLIENT")
           
   client.close()    
except socket.error as e:
    print(e)
