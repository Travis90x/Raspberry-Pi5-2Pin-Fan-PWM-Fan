# Raspberry Pi5 PWM Fan Control

Manage a 12v/24v (external power with GND in common with raspberry) Fan with IRP520 usig GPIO 18
Take the highest temp from CPU, and 2 SSD NVME, to set the PWM value.

![immagine](https://github.com/user-attachments/assets/b397c76b-bfbd-4916-a956-e86a77e3acdc)

As a Service

You need two files from the repository:

    pifancontrol.service
    fan_control.py

Collect the two files the way you prefer and copy them in the locations suggested below.

You can simply...

  git clone https://github.com/Travis90x/Raspberry-Pi5-2Pin-Fan-PWM-Fan.git
  cd Raspberry-Pi5-2Pin-Fan-PWM-Fan

Install

  sudo cp pifancontrol.service /lib/systemd/system/pifancontrol.service
  sudo cp fan_control.py /usr/local/sbin/
  sudo chmod 644 /lib/systemd/system/pifancontrol.service
  sudo chmod +x /usr/local/sbin/fan_control.py
  sudo systemctl daemon-reload
  sudo systemctl enable pifancontrol.service
  sudo systemctl start pifancontrol.service

Check status

        user@host:~ $ sudo service pifancontrol status
        ● pifancontrol.service - Dynamic FAN control
             Loaded: loaded (/lib/systemd/system/pifancontrol.service; enabled; preset: enabled)
             Active: active (running) since Thu 2024-01-04 12:51:13 CET; 19s ago
           Main PID: 2158 (python3)
              Tasks: 4 (limit: 4453)
                CPU: 91ms
             CGroup: /system.slice/pifancontrol.service
                     └─2158 /usr/bin/python3 /usr/local/sbin/fan_control.py

Remove / Uninstall

  sudo systemctl stop pifancontrol.service
  sudo systemctl disable pifancontrol.service
  sudo systemctl daemon-reload
  sudo rm /usr/local/sbin/fan_control.py
  sudo rm /lib/systemd/system/pifancontrol.service

The script will be started on boot and will be restarted in case of errors.
