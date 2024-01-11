#!/usr/bin/env python
# coding: utf-8

# In[96]:


import pyfirmata
import time
from pyfirmata import Arduino, SERVO, util

from getpass import getpass
import os
import replicate
import time
from IPython.display import Image
import cv2


# In[97]:


a = replicate.Client(api_token='r8_8D7daow37iLmiXWlfQaqhsWUf1lmnYU3W2HNd')


# In[110]:


# Define the COM port of your Arduino
arduino_port = 'COM5'  # Replace 'COMX' with the appropriate port name

# Create a new board and set up the connection
board = pyfirmata.Arduino(arduino_port)

# Define the pins connected to the L298N motor driver
enA = board.get_pin('d:11:p')  # Enable for Motor A
in1 = board.get_pin('d:9:o')  # Input 1 for Motor A
in2 = board.get_pin('d:10:o')  # Input 2 for Motor A


# In[111]:


# Define a function to control the motor
def control_motor(direction, speed):
    if direction == 'F':
        in1.write(True)
        in2.write(False)
    elif direction == 'B':
        in1.write(False)
        in2.write(True)
    elif direction == 'S':
        in1.write(False)
        in2.write(False)
    enA.write(speed)


# In[112]:


board.digital[5].mode = SERVO

def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    time.sleep(0.015)


# In[113]:


user_prompt = 'just give the name of the object in the image, and wheather it is bio degradeable or non-bio degradable. Give the answer in the format: Object_name = Bio degradable or non biodegradable'


# In[114]:


while True:
    
    try:
        
        
        print('motor taking the garbage to camera')
    
        control_motor('F', 0.01)  # Move the motor forward at full speed
        
        time.sleep(5)
        
        control_motor('S', 0.0)  # Stop the motor
        
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite(f"captured images/{(len(os.listdir('captured images'))+1)}.jpeg", frame)
        cap.release()
        img = f"captured images/{(len(os.listdir('captured images')))}.jpeg"
        
        print('rotating servo based on garbage')
        
        output = a.run(
            "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
            input={"image": open(img, "rb"), "prompt": user_prompt}
        )
        
        for item in output:
            print(item, end="")
            
        print('\n')
            
        if item == 'Non-biodegradable':
            for i in range(0,180):
                rotateservo(5,i)
                
        if item == 'degradable':
            for i in range(0,90):
                rotateservo(5,i)
                
        print('Taking the garbage to bin')
            
            
        control_motor('F', 0.01)  # Move the motor forward at full speed
        
        time.sleep(5)        
        
        print('Next Garbage')
        
        control_motor('S', 0.0)  # Stop the motor
        
        time.sleep(3)
        
        print('*'*100)

    except KeyboardInterrupt:
        board.exit()
        print("Connection closed.")


# In[ ]:





# In[ ]:





# In[ ]:




