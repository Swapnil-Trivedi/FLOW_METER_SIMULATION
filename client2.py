#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:50:15 2020

@author: swapnil
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:28:52 2020

@author: swapnil
"""
"""
our client 2 script is same as main client but i have changed the device ip and device features
"""
import pickle
import socket
import time

port=8071
device_ip="127.2.1.2"
device=device_ip.encode()

host="127.10.10.10"
dname="FLX85"
dtype="Flow_Meter"
dsr="TLSSE975NA8525"

data={
      "dname":dname,
      "dtype":dtype,
      "dsr":dsr,
      
      }
data=pickle.dumps(data)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(5)
try:
   client.connect((host,port))
   client.send(device)
   message=client.recv(1024)
   message=message.decode()
   if(message=="true"):
      message=client.recv(1024)
      print(message.decode())
      client.send(data)
      message=client.recv(1024)
      print(message.decode())
      message=client.recv(1024)
      print(message.decode())
   else:
       print("Device already Registered\nConnected To : ",host,"Sending Data.... ")
       #also changing value so we can easily differentiate the output
       a,b=1,1
       try:
        while True:
         data=[a,b]
         data=pickle.dumps(data)
         client.send(data)
         time.sleep(1)
         mssg=client.recv(1024)
         mssg=pickle.loads(mssg)
         print(f"Sum of {a}+{b} is : {mssg}")
         a+=1
         b+=1
        print("Data Sent Succesfully")
        client.close()
       except KeyboardInterrupt:
           print("\nTERMINATED BY CLIENT")
           
   client.close()    
except socket.error as e:
    print(e)
