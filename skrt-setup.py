#! /usr/bin/env python
from subprocess import Popen,PIPE,STDOUT
import collections
import os
import sys
import time
import math
import os
import time
import random
import string
from urllib2 import urlopen

WELCOME = "## SIKRET COIN MASTERNODE INSTALLER ##"
DL_URL = "https://github.com/sikretcoin/SikretCoin/releases/download/v1.0.0"
DL_NAME = "skrt-1.0.0-x86_64-linux-gnu.tar.gz"
BIN_FOLDER = "skrt-1.0.0"
BIN_DAEMON = "skrtd"
BIN_CLI = "skrt-cli"
CONF_PORT = 10037
CONF_RPCPORT = 10038
CONF_FOLDER = "SikretCoin"
CONF_NAME = "skrt.conf"
SERVER_IP = urlopen('http://ip.42.pl/raw').read()

def print_line():
    print("\n")
    time.sleep(1)
	
def print_info(message):
    print("\x1b[0m" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_green(message):
    print("\033[1;32;40m" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_yellow(message):
    print("\033[1;33;40m" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_red(message):
    print("\033[1;31;40m\n" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_blue(message):
    print("\033[1;34;40m" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_magenta(message):
    print("\033[1;35;40m" + str(message) + "\x1b[0m")
    time.sleep(1)

def print_cyan(message):
    print("\033[1;36;40m" + str(message) + "\x1b[0m")
    time.sleep(1)

def get_terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h
    
def remove_lines(lines):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for l in lines:
        sys.stdout.write(CURSOR_UP_ONE + '\r' + ERASE_LINE)
        sys.stdout.flush()

def run_command(command):
    out = Popen(command, stderr=STDOUT, stdout=PIPE, shell=True)
    lines = []
    
    while True:
        line = out.stdout.readline()
        if (line == ""):
            break
        
        # remove previous lines     
        remove_lines(lines)
        
        w, h = get_terminal_size()
        lines.append(line.strip().encode('string_escape')[:w-3] + "\n")
        if(len(lines) >= 9):
            del lines[0]

        # print lines again
        for l in lines:
            sys.stdout.write('\r')
            sys.stdout.write(l)
        sys.stdout.flush()

    remove_lines(lines) 
    out.wait()

def start_setup():
    os.system('clear')
    print_green(WELCOME)

    dummy = raw_input("\x1b[0m" + "Press enter to start." + "\x1b[0m")

    print_info("Updating the system...")
    run_command("apt-get update")
    run_command("apt-get upgrade -y")
    run_command("apt-get dist-upgrade -y")

    print_info("Checking root privileges...")
    user = os.getuid()
    if user != 0:
        print_error("This program requires root privileges.  Run as root user.")
        sys.exit(-1)

    print_info("Downloading the file...")
    run_command("rm -f {}".format(DL_NAME))
    run_command("wget {}/{}".format(DL_URL,DL_NAME))
   
    print_info("Unzipping the file...")
    run_command("tar -zxvf {}".format(DL_NAME))
   
    print_info("Setting permissions...")   
    run_command("chmod +x ~/{}/bin/{}".format(BIN_FOLDER,BIN_DAEMON))
    run_command("chmod +x ~/{}/bin/{}".format(BIN_FOLDER,BIN_CLI))

    print_info("Setting up masternode...")
    print_info("Note:")
    print_info("If you are using putty please remember that selecting a text will automatically copy it to clipboard and right click on the window will paste the clipboard content here.")
    
    rpc_username = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
    rpc_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(40)])

    print_red("Step 1")
    masternode_name = raw_input("\033[1;33;40m" + "Please enter a name for your masternode: " + "\x1b[0m")
    
    print_red("Step 2")
    print_info("Open your desktop wallet console (Tools => Debug Console) and type the following command (green text below) to get a new address for your masternode:")
    print_green("getaccountaddress {}".format(masternode_name))
    dummy = raw_input("\x1b[0m" + "Press enter to go to next step." + "\x1b[0m")

    print_red("Step 3")
    print_info("in your desktop wallet send 10,000 coins to your masternode address that you have got in Step 2")
    dummy = raw_input("\x1b[0m" + "Press enter to go to next step." + "\x1b[0m")

    print_red("Step 4")
    print_info("type the following command (green text below) in your desktop wallet console (Tools => Debug Console) to get your masternode txhash and outputidx")
    print_green("masternode outputs")
    masternode_txhash = raw_input("\033[1;33;40m" + "Paste the txhash string here: " + "\x1b[0m")
    masternode_outputidx = raw_input("\033[1;33;40m" + "Enter the outputidx number here: " + "\x1b[0m")

    print_red("Step 5")
    print_info("type the following command (green text below) in your desktop wallet console (Tools => Debug Console) to get your masternode private key")
    print_green("masternode genkey")
    masternode_privatekey = raw_input("\033[1;33;40m" + "Paste the private key string here: " + "\x1b[0m")
    
    config = """rpcuser={}
rpcpassword={}
rpcallowip=127.0.0.1
rpcport={}
port={}
server=1
listen=1
daemon=1
banscore=1000
bantime=10
logtimestamps=1
maxconnections=256
masternode=1
externalip={}
bind={}:{}
masternodeaddr={}
masternodeprivkey={}""".format(rpc_username, rpc_password, CONF_RPCPORT, CONF_PORT, SERVER_IP, SERVER_IP, CONF_PORT, SERVER_IP, masternode_privatekey)

    print_info("Saving config file...")
    run_command("cd ~")
    run_command("cd")
    run_command("mkdir -p .{}/".format(CONF_FOLDER))
    run_command("touch .{}/{}".format(CONF_FOLDER, CONF_NAME))
    with open('.{}/{}'.format(CONF_FOLDER, CONF_NAME), 'w') as f:
        f.write(config)

    print_info("Starting the masternode...")
    os.system('./{}/bin/{} -daemon &> /dev/null'.format(BIN_FOLDER,BIN_DAEMON))
    print_info("Masternode will sync in the background...")
    print_info("Please wait...")
    time.sleep(10)

    print_red("Step 6")
    print_info("Copy and paste the following line (green text below) in your desktop masternode configuration file (Tools => Open Masternode Configuration File) in one line and save and close the file ")
    print_green("{} {}:{} {} {} {}".format(masternode_name, SERVER_IP, CONF_PORT, masternode_privatekey, masternode_txhash, masternode_outputidx) )
    dummy = raw_input("\x1b[0m" + "Press enter to go to next step." + "\x1b[0m")

    print_red("Step 7")
    print_info("After 16 confirmation of your transaction in step 3 type the following command (green text below) in your desktop wallet console (Tools => Debug Console) to start your master node")
    print_green("masternode start-alias {}".format(masternode_name))
    dummy = raw_input("\x1b[0m" + "Press enter to go to next step." + "\x1b[0m")

    print_info("The setup process has finished, you can close this window now.")
    

def main():
    start_setup()

if __name__ == "__main__":
    main()
