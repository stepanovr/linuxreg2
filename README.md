# linuxreg2
Next generation of the linuxreg. Allows direct memory/device registers access from the userspace.

The application supports 32 bit and 64 bit target architectures.
To choose the target architecture select an appropriate directory in the target subdirectory.

Warning! Reading of some registers may crash you system.
Writing to some registers of some deviced i.e. PMIC may damage your hardware.
Do not try access the devices that are unknown to you. 
Use the application on your own risk.

The application consists of two parts:
The first one is a simple udp server to run on the target machine. The UDP server receives command from 
the remote GUI application, execute them and responds to the remote GUI application.
There are two versions of the server in the target directory: target/arch_32 and target/arch_64.

The second part is a Python scripts that uses tkinter for GUI.

To install tkinter use
Ubuntu
sudo apt-get install python3-tk 

Fedora
sudo dnf install python3-tkinter

MacOS
brew install python-tk

On Windows firewall doesn't support rfc4787 (Network Address Translation (NAT) Behavioral Requirements
for Unicast UDP). That may be fixed with a rule creation or firewall disabling.


For writing use 32 bit words only.


Installing the target udp server on the 32 bit architecture:
Copy files in target/arch_32 to a target machine.
Execute  make

Installing the target udp server on the 64 bit architecture:
Copy files in target/arch_64 to a target machine.
Execute  make


Then execute the script as superuser:
sudo ./mem_access.sh


On a remote machine run the Python application gui_access_udp.py

Set the target machine's IP address to the corresponding entry field in the dialog window.
The default port is 35035.

The File menu:
* Allows turning logging on and off

* Option "Script" opens a script file that contains the sequence of reading and writing commands.
  See the "program" file as an example. That file has a list of read commands. 
  Adding a value at the end of a read commands converts it to a write command writing the added value.

* Option "Regs XML" opens an *.xml file that contains register set to open im a new dialog window.
  That allows access to a custom register group.
  See *.xml files presented for a refernce.


Open with an ediitor the registers.xml file that is an example.

The first register name is "ADC Regssters" that is the name of the window to be opened.
All "register name" fields after the first appearance are used for naming registers 
with the address indicated with the "addr" field.

Try oppening the registers.xml file with the application's File->Regs XML.
That will open the window that is specified with the registers.xml.

### Install on Yocto

devtool add regview https://github.com/stepanovr/linuxreg2

Replace the recipe
build/workspace/recipes/regview/regview_git.bb
with:
```
# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://LICENSE;md5=b234ee4d69f5fce4486a80fdaf4a4263"

SRC_URI = "git://github.com/stepanovr/linuxreg2;protocol=https;branch=master"

# Modify these as desired
PV = "1.0+git"
SRCREV = "346be6905e39d77ddd8024ea4bcbda0c0f9f58c9"

S = "${WORKDIR}/git"


# NOTE: this is a Makefile-only piece of software, so we cannot generate much of the
# recipe automatically - you will need to examine the Makefile yourself and ensure
# that the appropriate arguments are passed in.

do_configure () {
        # Specify any needed configure commands here
        :
}

do_compile () {
        # You will almost certainly need to add additional arguments here
        oe_runmake
}

do_install () {
        # NOTE: unable to determine what to put here - there is a Makefile but no
        # target named "install", so you will need to define this yourself
        install -d ${D}${bindir}
        install -m 0755 ${S}/target/arch_32/udpserv32 ${D}${bindir}/udpserv32
        install -m 0755 ${S}/target/arch_64/udpserv64 ${D}${bindir}/udpserv64
}
```

add to build/conf/local.conf

```
IMAGE_INSTALL:append = " regview"
```

