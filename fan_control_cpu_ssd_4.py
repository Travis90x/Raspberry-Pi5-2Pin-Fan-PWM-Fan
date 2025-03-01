#! /usr/bin/env python3
from gpiozero import PWMOutputDevice
import time
import os
import glob

# Configuration
FAN_PIN = 18       # BCM pin used to drive PWM fan
WAIT_TIME = 5     # [s] Time to wait between each refresh
PWM_FREQ = 200     # [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 55      # under this temp value fan is switched to the FAN_OFF speed
MAX_TEMP = 90      # over this temp value fan is switched to the FAN_MAX speed
FAN_LOW = 30       # lower side of the fan speed range during cooling
FAN_HIGH = 100     # higher side of the fan speed range during cooling
FAN_OFF = 0        # fan speed to set if the detected temp is below MIN_TEMP 
FAN_MAX = 100      # fan speed to set if the detected temp is above MAX_TEMP 
TOLERANCE_MIN = 3  # [°C] Tolerance for change Fan speed

# Get CPU's temperature
def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return round(float(f.read()) / 1000, 1)

# Get SSD 1 temp0
def getSsd1Temp0():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme0 | grep Temperature:").read()
        lines = result.splitlines()
        temp0 = round(float([line for line in lines if "Temperature" in line][0].split()[-2]), 1)
        return temp0
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0

# Get SSD 1 temp1
def getSsd1Temp1():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme0 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        return temp1
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
# Get SSD 1 temp2   
def getSsd1Temp2():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme0 | grep Temperature").read()
        lines = result.splitlines()
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0


# Get SSD 2 temp0
def getSsd2Temp0():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme1 | grep Temperature:").read()
        lines = result.splitlines()
        temp0 = round(float([line for line in lines if "Temperature" in line][0].split()[-2]), 1)
        return temp0
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0

# Get SSD 2 temp1
def getSsd2Temp1():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme1 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        return temp1
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
# Get SSD 2 temp2   
def getSsd2Temp2():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme1 | grep Temperature").read()
        lines = result.splitlines()
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
        
        
# Get SSD 3 temp0
def getSsd3Temp0():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme2 | grep Temperature:").read()
        lines = result.splitlines()
        temp0 = round(float([line for line in lines if "Temperature" in line][0].split()[-2]), 1)
        return temp0
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0

# Get SSD 3 temp1
def getSsd3Temp1():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme2 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        return temp1
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
# Get SSD 3 temp2   
def getSsd3Temp2():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme2 | grep Temperature").read()
        lines = result.splitlines()
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
        
      
# Get SSD 4 temp0
def getSsd4Temp0():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme3 | grep Temperature:").read()
        lines = result.splitlines()
        temp0 = round(float([line for line in lines if "Temperature" in line][0].split()[-2]), 1)
        return temp0
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0

# Get SSD 4 temp1
def getSsd4Temp1():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme3 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        return temp1
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
# Get SSD 4 temp2   
def getSsd4Temp2():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme3 | grep Temperature").read()
        lines = result.splitlines()
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0
        
        
        
      
# Get the highest temperature
def highest_temp():
    cpu_temp = getCpuTemperature()
    ssd1_temp0 = getSsd1Temp0()
    ssd1_temp1 = getSsd1Temp1()
    ssd1_temp2 = getSsd1Temp2()
    
    ssd2_temp0 = getSsd2Temp0()
    ssd2_temp1 = getSsd2Temp1()
    ssd2_temp2 = getSsd2Temp2()
            
    ssd3_temp0 = getSsd3Temp0()
    ssd3_temp1 = getSsd3Temp1()
    ssd3_temp2 = getSsd3Temp2()
    
    ssd4_temp0 = getSsd4Temp0()
    ssd4_temp1 = getSsd4Temp1()
    ssd4_temp2 = getSsd4Temp2()
    
    print(f"CPU Temperature: {cpu_temp}°C")
    print(f"SSD 1 Temperature: {ssd1_temp0}°C")
    print(f"SSD 1 Temperature Sensor 1: {ssd1_temp1}°C")
    print(f"SSD 1 Temperature Sensor 2: {ssd1_temp2}°C")
    print(f"SSD 2 Temperature: {ssd2_temp0}°C")
    print(f"SSD 2 Temperature Sensor 1: {ssd2_temp1}°C")
    print(f"SSD 2 Temperature Sensor 2: {ssd2_temp2}°C")  
    print(f"SSD 3 Temperature: {ssd3_temp0}°C")    
    print(f"SSD 3 Temperature Sensor 1: {ssd3_temp1}°C")
    print(f"SSD 3 Temperature Sensor 2: {ssd3_temp2}°C")
    print(f"SSD 4 Temperature: {ssd4_temp0}°C")    
    print(f"SSD 4 Temperature Sensor 1: {ssd4_temp1}°C")
    print(f"SSD 4 Temperature Sensor 2: {ssd4_temp2}°C")    
    
    highest = max(cpu_temp, ssd1_temp0, ssd1_temp1, ssd1_temp2, ssd2_temp2, ssd2_temp1, ssd2_temp2, ssd3_temp0, ssd3_temp1, ssd3_temp2, ssd4_temp0, ssd4_temp1, ssd4_temp2)
    print(f"Highest Temp.: {highest}°C")
    return highest

def setFanSpeed(speed):
    pwm_fan.value = speed / 100  # divide by 100 to get values from 0 to 1
    # print(f"Fan Speed Set To: {round(speed, 1)}%")

# Handle fan speed with tolerance
def handleFanSpeed():

    # Pulizia dell'output precedente
    print("\033c", end="")  # This clears the screen on most terminals
    
    
    temp = highest_temp()
    # Turn off the fan if temperature is below MIN_TEMP - TOLERANCE_MIN
    if temp < MIN_TEMP - TOLERANCE_MIN:
        setFanSpeed(FAN_OFF)
        print(f"Fan profile OFF: {round(FAN_OFF, 1)}%")
    # Don't change fan speed if temperature is between MIN_TEMP - TOLERANCE_MIN and MIN_TEMP + TOLERANCE_MIN
    elif MIN_TEMP - TOLERANCE_MIN <= temp and temp <= MIN_TEMP + TOLERANCE_MIN:
        # setFanSpeed(FAN_LOW)
        print("Fan profile not changed.")
    # Set fan speed to FAN_LOW if temperature is > MIN_TEMP + TOLERANCE_MIN
    elif temp > MIN_TEMP + TOLERANCE_MIN:
        setFanSpeed(FAN_LOW)
        print(f"Fan profile LOW: {round(FAN_LOW, 1)}%")
    # Set fan speed to MAXIMUM if temperature is above MAX_TEMP
    elif temp > MAX_TEMP:
        setFanSpeed(FAN_MAX)
        print(f"Fan profile MAX: {round(FAN_MAX, 1)}%")
    # Calculate dynamic fan speed
    else:
        step = (FAN_HIGH - FAN_LOW) / (MAX_TEMP - MIN_TEMP)
        TEMP_STEP = temp - MIN_TEMP
        TEMP_STEP = abs(TEMP_STEP)
        speed = FAN_LOW + (round(TEMP_STEP) * step)
        setFanSpeed(speed)
        print(f"Fan profile dynamic: {round(speed, 1)}% (Highest Temp.: {round(temp, 1)}°C)")
        
try:
    pwm_fan = PWMOutputDevice(FAN_PIN, initial_value=0, frequency=PWM_FREQ)  # initialize FAN_PIN as a pwm output
    setFanSpeed(FAN_OFF)  # initially set fan speed to the FAN_OFF value
    print("Fan Control Script Started")
    while True:
        handleFanSpeed()  # call the function that calculates the target fan speed
        time.sleep(WAIT_TIME)  # wait for WAIT_TIME seconds before recalculating
except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    print("Script Interrupted! Setting Fan to High Speed...")
    setFanSpeed(FAN_HIGH)
finally:
    pwm_fan.close()  # in case of unexpected exit, resets pin status (fan will go full speed after exiting)
    print("Script Terminated. Fan Control Released.")
