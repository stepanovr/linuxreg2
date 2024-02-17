# linuxreg2
Next generation of the linuxreg. Allows direct memory/device registers access from the userspace.

The application supports 32 bit systems only. Extention to 64 bit is pending.

Warning! Reading of some registers may crash you system.
Writing to some registers of some deviced i.e. PMIC may damage your hardware.
Do not try access the devices that are unknown to you
Use the application on your own risk.

Use 32 bit writing only.

32 bit architecture:
Copy files in target/arch32 to a target machine.
Execute  make
Then execute the script as superuser:
sudo ./mem_access.sh

On a remote machine run the Python application gui_access_udp.py

Set the target machine's IP address to the corresponding entry field.

The File menu:
* Allows turning logging on and off

* Option "Script" opens a script file that contails the sequence of reading and writing commands.
  See the "program" file as an example. That file has a list of read commands. 
  Adding a value at the end of a read commands converts it to a write command writing the aded walue

* Option "Regs XML" opens an *.xml file that contains register set to open im a new dialog window.
  That allows access to a custom register group.
  See *.xml files presented for a refernce


Open registers.xml file that is an example 

The first register name is "ADC Regssters" that is the name of the window to be opened
All "register name" fields after the first appearance are used for naming registers 
with the address indicated with the "addr" field

