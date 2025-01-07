#! /usr/bin/env python3
from gpiozero import PWMOutputDevice
import time
import os

# Configuration
FAN_PIN = 18       # BCM pin used to drive PWM fan
WAIT_TIME = 10     # [s] Time to wait between each refresh
PWM_FREQ = 200     # [kHz] 25kHz for Noctua PWM control

# Configurable temperature and fan speed
MIN_TEMP = 35      # under this temp value fan is switched to the FAN_OFF speed
MAX_TEMP = 90      # over this temp value fan is switched to the FAN_MAX speed
FAN_LOW = 30       # lower side of the fan speed range during cooling
FAN_HIGH = 100     # higher side of the fan speed range during cooling
FAN_OFF = 0        # fan speed to set if the detected temp is below MIN_TEMP 
FAN_MAX = 100      # fan speed to set if the detected temp is above MAX_TEMP 
TOLERANCE_MIN = 5  # [°C] Tolerance for FAN_OFF below MIN_TEMP

# Get CPU's temperature
def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return round(float(f.read()) / 1000, 1)

# Get SSD 1 temperatures
def getSsd1Temperatures():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme0n1 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp1, temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0, 0

# Get SSD 2 temperatures
def getSsd2Temperatures():
    try:
        # Run smartctl to fetch temperatures
        result = os.popen("sudo smartctl -A /dev/nvme1n1 | grep Temperature").read()
        lines = result.splitlines()
        temp1 = round(float([line for line in lines if "Temperature Sensor 1" in line][0].split()[-2]), 1)
        temp2 = round(float([line for line in lines if "Temperature Sensor 2" in line][0].split()[-2]), 1)
        return temp1, temp2
    except (IndexError, ValueError):
        # If parsing fails, assume a safe fallback temperature
        return 0, 0
        
# Get the highest temperature
def highest_temp():
    cpu_temp = getCpuTemperature()
    ssd1_temp1, ssd1_temp2 = getSsd1Temperatures()
    ssd2_temp1, ssd2_temp2 = getSsd2Temperatures()
    print(f"CPU Temperature: {cpu_temp}°C")
    print(f"SSD 1 Temperature Sensor 1: {ssd1_temp1}°C")
    print(f"SSD 1 Temperature Sensor 2: {ssd1_temp2}°C")
    print(f"SSD 2 Temperature Sensor 1: {ssd2_temp1}°C")
    print(f"SSD 2 Temperature Sensor 2: {ssd2_temp2}°C")   
    
    highest = max(cpu_temp, ssd1_temp1, ssd1_temp2, ssd2_temp2, ssd2_temp2)
    print(f"Highest Temperature: {highest}°C")
    return highest

def setFanSpeed(speed):
    pwm_fan.value = speed / 100  # divide by 100 to get values from 0 to 1
    print(f"Fan Speed Set To: {round(speed, 1)}%")

# Handle fan speed with tolerance
def handleFanSpeed():

    # Pulizia dell'output precedente
    print("\033c", end="")  # This clears the screen on most terminals
    
    
    temp = highest_temp()
    # Turn off the fan if temperature is below MIN_TEMP - TOLERANCE_MIN
    if temp < MIN_TEMP - TOLERANCE_MIN:
        setFanSpeed(FAN_OFF)
        print(f"Fan OFF: {round(speed, 1)}%")
    # Set fan speed to MAXIMUM if temperature is between MIN_TEMP - TOLERANCE_MIN and MIN_TEMP
    elif MIN_TEMP - TOLERANCE_MIN <= temp and temp < MIN_TEMP:
        setFanSpeed(FAN_LOW)
        print(f"Fan LOW: {round(speed, 1)}%")
    # Set fan speed to MAXIMUM if temperature is above MAX_TEMP
    elif temp > MAX_TEMP:
        setFanSpeed(FAN_MAX)
        print(f"Fan MAX: {round(speed, 1)}%")
    # Calculate dynamic fan speed
    else:
        step = (FAN_HIGH - FAN_LOW) / (MAX_TEMP - MIN_TEMP)
        temp_speed = temp
        temp_speed -= MIN_TEMP
        speed = FAN_LOW + (round(temp_speed) * step)
        setFanSpeed(speed)
        print(f"Dynamic Fan Speed: {round(speed, 1)}% (Highest Temp.: {round(temp, 1)}°C)")

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
