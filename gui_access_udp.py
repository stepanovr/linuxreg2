#!/usr/bin/env python3

import xml.etree.ElementTree as ET

import socket
from tkinter import *
import tkinter as tk

from tkinter import ttk

from tkinter import filedialog

class Window(tk.Toplevel):
    config_data = []

    field = []

    def ff0(self):
      self.write_reg(0)

    def ff1(self):
      self.write_reg(1)

    def ff2(self):
      self.write_reg(2)

    def ff3(self):
      self.write_reg(3)

    def ff4(self):
      self.write_reg(4)

    def ff5(self):
      self.write_reg(5)

    def ff6(self):
      self.write_reg(6)

    def ff7(self):
      self.write_reg(7)

    def ff8(self):
      self.write_reg(8)

    def ff9(self):
      self.write_reg(9)

    def ff10(self):
      self.write_reg(10)

    def ff11(self):
      self.write_reg(11)

    def ff12(self):
      self.write_reg(12)

    def ff13(self):
      self.write_reg(13)

    def ff14(self):
      self.write_reg(14)

    def ff15(self):
      self.write_reg(15)

    def ff16(self):
      self.write_reg(16)

    def ff17(self):
      self.write_reg(17)

    def ff18(self):
      self.write_reg(18)

    def ff19(self):
      self.write_reg(19)

    def ff20(self):
      self.write_reg(20)

    def ff21(self):
      self.write_reg(21)

    def ff22(self):
      self.write_reg(22)

    def ff23(self):
      self.write_reg(23)

    def ff24(self):
      self.write_reg(24)

    def ff25(self):
      self.write_reg(25)

    def ff26(self):
      self.write_reg(26)

    def ff27(self):
      self.write_reg(27)

    def ff28(self):
      self.write_reg(28)

    def ff29(self):
      self.write_reg(29)

    def ff30(self):
      self.write_reg(30)

    funct = []

    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x300')
        self.title('Toplevel Window')

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)

    def __init__(self, parent, reg_data):
        super().__init__(parent)

#        print(len(reg_data))
        self.app = parent

        self.funct = [self.ff0, self.ff1, self.ff2, self.ff3, self.ff4, self.ff5, self.ff6, self.ff7, self.ff8, self.ff9,
             self.ff10, self.ff11, self.ff12, self.ff12, self.ff13, self.ff14, self.ff15, self.ff16, self.ff17,
             self.ff18, self.ff19, self.ff20, self.ff21, self.ff22, self.ff23, self.ff24, self.ff25, self.ff26,
             self.ff27, self.ff28, self.ff29, self.ff30]

        self.field = []
        size = '700x'+ str(50 + len(reg_data)*28)
#        print("size: " + size)
        self.geometry(size)

        first = reg_data[0]

        L1 =  Label(self, text = "Register")
        L1.place(x = 10, y = 10)

        L2 = Label(self, text = "Address")
        L2.place(x = 160, y = 10)
 
        L3 = Label(self, text = "Value")
        L3.place(x = 350, y = 10)
        self.config_data = reg_data.copy()
        del self.config_data[0]
#        print(self.config_data)

        pos = 1 
        for register in reg_data:
          if register[1] == "title":
            print(register[0])
          else:
            print(register[0], register[1])
            Lb1 = Label(self, text = register[0])
            Lb1.place(x = 10, y = 10 + 28 * pos)

            Lb2 = Label(self, text = register[1])
            Lb2.place(x = 160, y = 10 + 28 * pos)

            self.ent = Entry(self)
            self.field.append(self.ent)
            self.ent.place(x = 350, y = 10 + 28 * pos)
            but = Button(self, text = "Write", command = self.funct[pos-1])
            but.place(x = 510, y = 7 + 28 * pos)
            pos += 1

        self.but = Button(self, text = "Refresh", command = self.read_mem)
        self.but.place(x = 300, y = 15 + 28 * pos)
        self.title(first[0])

    def read_mem(self):
      pos = 0
      for reg in self.config_data:
        data = app.udp_exchange(reg[1] + " 32")
        data = data.rstrip()
        print(data)
        self.field[pos].delete(0,END)
        self.field[pos].insert(0, data)
        pos += 1


    def write_reg(self, num):
      reg = self.config_data[num]
#      print(reg[1])
#      print(num)
      addr = reg[1]
      val = self.field[num].get()

      bits = "32"

      request = ""
      request += addr
      request += " "
      request += bits
      request += " "
      request += val

      print(request)

      data = app.udp_exchange(request)
      print (data)


class Application(Frame):
  """ GUI application for access the remote memory access application over TCP  """

  tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  address_step = 4
  connected = False
  num_per_line = 4
  log_enable = False
  logname = "logfile.txt"

  def __init__(self):
    """ To provide usage of API """
    super(Application, self).__init__()

  def __init__(self, master):
    """ Initialize Frame. """
    super(Application, self).__init__(master)
    self.grid()
    self.create_widgets()

  def create_widgets(self):
    """ Create widgets to get story information and to display story. """
    Label(self,
      text = "Specify server information "
      ).grid(row = 0, column = 0, columnspan = 2, sticky = W)

    Label(self,
      text = "Address: "
      ).grid(row = 1, column = 0, sticky = W)

    self.serv_addr_ent = Entry(self)
    self.serv_addr_ent.grid(row = 1, column = 1, sticky = W)
    self.serv_addr_ent.delete(0,END)
    self.serv_addr_ent.insert(0, "192.168.1.8" )
    Label(self,
      text = "Port:"
      ).grid(row = 2, column = 0, sticky = W)
    self.serv_port_ent = Entry(self)
    self.serv_port_ent.grid(row = 2, column = 1, sticky = W)
    self.serv_port_ent.delete(0,END)
    self.serv_port_ent.insert(0, "35035" )

    Button(self,
      text = "Test connection",
      command = self.open_connection_UDP
      ).grid(row = 3, column = 0, sticky = W)

    self.story_txt = Text(self, width = 96, height = 20, wrap = WORD)
    self.story_txt.grid(row = 10, column = 0, columnspan = 4)

    Label(self,
      text = "Write address\t\t\tvalue"
      ).grid(row = 4, column = 0, columnspan = 2, sticky = W)

    Label(self,
      text = ""
      ).grid(row = 5, column = 0, sticky = W)
    self.wr_addr_ent = Entry(self)
    self.wr_addr_ent.grid(row = 5, column = 0, sticky = W)

    Label(self,
      text = ""
      ).grid(row = 5, column = 1, sticky = W)
    self.wr_val_ent = Entry(self)
    self.wr_val_ent.grid(row = 5, column = 1, sticky = W)

    Button(self,
      text = "Write",
      command = self.write_reg_udp
      ).grid(row = 6, column = 0, sticky = W)


    Label(self,
      text = "Read start address"
      ).grid(row = 7, column = 0, columnspan = 2, sticky = W)

    Label(self,
      text = ""
      ).grid(row = 8, column = 0, sticky = W)
    self.rd_addr_ent = Entry(self)
    self.rd_addr_ent.grid(row = 8, column = 0, sticky = W)

    Button(self,
      text = "Read",
      command = self.read_mem
      ).grid(row = 9, column = 0, sticky = W)

    self.bits = StringVar()
    self.bits.set(None)

    bitss = ["8", "16", "32", "64"]
    column = 3 
    row = 2
    for part in bitss:
      Radiobutton(self,
        text = part,
        variable = self.bits,
        value = part
        ).grid(row = row, column = column, sticky = W)

      row += 1

  def udp_exchange(self, request):
    self.serv_addr = self.serv_addr_ent.get()
    self.serv_port = self.serv_port_ent.get()
    self.serverAddressPort = (self.serv_addr, int(self.serv_port))
    self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    bytesToSend = str.encode(request)
    self.udp_socket.sendto(bytesToSend, self.serverAddressPort)
    self.udp_socket.settimeout(2.0)
    self.log_message(request)

    try:
      val, address = self.udp_socket.recvfrom(1024)
      data = str(val, "utf-8")
      self.log_message(data)

      self.display_message(data)
    except socket.timeout:
      self.display_message("No target connection")

    return data

  def write_reg(self):
    """ Write button handler """
    # get values from the GUI
    addr = self.wr_addr_ent.get()
    val = self.wr_val_ent.get()
    if self.connected == True:

      request = "w "
      request += addr
      request += " "
      request += val

      print(request)

      self.tcp_sock.sendall(str.encode(request))
      data = str(self.tcp_sock.recv(1024), "utf-8")
      print(data)


  def write_reg_udp(self):
    """ Write button handler """
    # get values from the GUI
    addr = self.wr_addr_ent.get()
    val = self.wr_val_ent.get()


    self.serv_addr = self.serv_addr_ent.get()
    self.serv_port = self.serv_port_ent.get()


    self.serverAddressPort = (self.serv_addr, int(self.serv_port))

    bits = self.bits.get()
    if ((bits == "8") or (bits == "16")):
      bits = 32  # For 32 bit architecture. Wont work if 64bit is used

    bits = self.set_format(bits)

    request = ""
    request += addr
    request += " "
    request += bits
    request += " "
    request += val

    print(request)

    report = "Wrote "
    report += bits
    report += " bits" 

    self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    bytesToSend = str.encode(request)
    self.udp_socket.sendto(bytesToSend, self.serverAddressPort)
    self.udp_socket.settimeout(2.0)
    self.log_message(request)

    try:
      val, address = self.udp_socket.recvfrom(1024)
      self.display_message(report)
    except socket.timeout:
      self.display_message("No target connection")

    data = str(val, "utf-8")
    print(data)
    self.log_message(data)

  def open_connection(self):

    if self.connected != True:
      self.serv_addr = self.serv_addr_ent.get()
      self.serv_port = self.serv_port_ent.get()

      sockaddr = socket.getaddrinfo(self.serv_addr, self.serv_port)

      print("Connection " + self.serv_addr)
      print(self.serv_port)
      bits = self.bits.get()
      print(bits)

      self.tcp_sock.connect((self.serv_addr, int(self.serv_port)))

      self.connected = True
    else:
      quit()

  def open_connection_UDP(self):
    self.serv_addr = self.serv_addr_ent.get()
    self.serv_port = self.serv_port_ent.get()
    self.serverAddressPort = (self.serv_addr, int(self.serv_port))

    msgFromClient       = "-h"

    self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    bytesToSend = str.encode(msgFromClient)
    self.udp_socket.sendto(bytesToSend, self.serverAddressPort)
    self.udp_socket.settimeout(2.0)

    try:
      data, addr = self.udp_socket.recvfrom(1024)
      self.display_message("Connected")
    except socket.timeout:
      self.display_message("No target connection")


    msg = str(data, "utf-8")
    print(msg)


  def read_mem(self):
    lines_num = 16
    start_addr_s = self.rd_addr_ent.get()
    start_addr = int(start_addr_s, 0)
    out_string = ""
    addr = start_addr



    self.display_message("")

    self.serv_addr = self.serv_addr_ent.get()
    self.serv_port = self.serv_port_ent.get()
    self.serverAddressPort = (self.serv_addr, int(self.serv_port))

    self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    bits = self.bits.get()
    bits = self.set_format(bits)

    self.udp_socket.settimeout(2.0)

    for ii in range(self.num_per_line * lines_num):
      if (ii % self.num_per_line) == 0:
        out_string += "\n" + hex(addr) + ": "

      request = ""
      request += hex(addr)
      request += " "
      request += bits

      bytesToSend = str.encode(request)
      self.udp_socket.sendto(bytesToSend, self.serverAddressPort)
#      self.udp_socket.settimeout(2.0)

      try:
        data, addr_udp = self.udp_socket.recvfrom(1024)
        timeout = False
      except socket.timeout:
        timeout = True
        self.display_message("No target connection")

      val = str(data, "utf-8")
      val = val.strip("\n")
      out_string += " "
      out_string += val
      addr += self.address_step

    if timeout :
      self.display_message("No target connection")
    else:
      self.log_message(out_string)
      self.display_message(out_string)
    print(out_string)

  def display_message(self, out_string):
    self.story_txt.delete(0.0, END)
    self.story_txt.insert(0.0, out_string)


  def set_format(self, bits):

    if bits == "8":
        self.num_per_line = 16
        self.address_step = 1
    elif  bits == "16":
        self.num_per_line = 8
        self.address_step = 2

    elif  bits == "32":
        self.num_per_line = 4
        self.address_step = 4

    elif  bits == "64":
        self.num_per_line = 2
        self.address_step = 8
    else:
        self.num_per_line = 4
        self.address_step = 4
        bits = "32"
    return bits

  def run_script(self):
    print("Execute script")
    # Display the dialog for browsing files.
    filename = filedialog.askopenfilename()
    with open(filename) as f:
      lines = [line.rstrip() for line in f]
    for line in lines:
      data = self.udp_exchange(line)
      data = data.strip("\n")

      print(line + " " + data)



  def run_xml(self):
#    print("Use XML registers set")
    # Display the dialog for browsing files.
    filename = filedialog.askopenfilename()

    regs = self.parse_reg_xml(filename)
    open_window = Window(self, regs)

#    with open(filename) as f:
#      lines = [line.rstrip() for line in f]
#    for line in lines:
#      data = self.udp_exchange(line)
#      data = data.strip("\n")

#      print(line + " " + data)

  def parse_reg_xml(self, finame):
    self.regs=[]
#    print("+++++++++++")
    tree = ET.parse(finame)

    root = tree.getroot()

    for register in root.findall('register'):
      addr = register.find('addr').text
      name = register.get('name')
      reg = []
      reg.append(name)
      reg.append(addr)
      self.regs.append(reg)

#    for register in self.regs:
#      print(register[0], register[1])
    return self.regs


  def log_message(self, message):
    if self.log_enable:
      message = message + "\n"
      fi = open(self.logname, "a")  # append mode
      fi.write(message)
      fi.close()

  def log_on(self):
    self.log_enable = True

  def log_off(self):
    self.log_enable = False

# main
root = Tk()
root.title("Memory Access")

# create a menubar
menubar = Menu(root)
root.config(menu=menubar)

app = Application(root)

file_menu = Menu(menubar)

# add a menu items to the menu
file_menu.add_command(
    label='Script',
    command=app.run_script
)

# add a menu items to the menu
file_menu.add_command(
    label='Regs XML',
    command=app.run_xml
)

# add a menu items to the menu
file_menu.add_command(
    label='Log ON',
    command=app.log_on
)

# add a menu items to the menu
file_menu.add_command(
    label='Log OFF',
    command=app.log_off
)

file_menu.add_command(
    label='Exit',
    command=root.destroy
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)


root.mainloop()


#######################################

