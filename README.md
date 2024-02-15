# linuxreg2
Next generation of the linuxreg. Allows direct memory/device registers access from the userspace.

The application supports 32 bit systems only. Extention to 64 bit is pending.

Warning! Reading of some registers may crash you system.
Writing to some registers of some deviced i.e. PMIC may damage your hardware.
Do not try access the devices that are unknown to you
Use the application on your own risk.

32 bit architecture:
Copy files in target/arch32 to a target machine.
Execute  make
Then execute the script as superuser:
sudo ./mem_access.sh

On a remote machine run the Python application gui_access_udp.py

Set the target machine's IP adres to the corresponding entry field.

