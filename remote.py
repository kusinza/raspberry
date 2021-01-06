from lirc import RawConnection
from printer import print_function
def ProcessIRRemote():
       
    #get IR command
    #keypress format = (hexcode, repeat_num, command_key, remote_id)
    try:
        keypress = conn.readline(.0001)
    except:
        keypress=""
              
    if (keypress != "" and keypress != None):
                
        data = keypress.split()
        sequence = data[1]
        command = data[2]
        
        #ignore command repeats
        if (sequence != "00"):
           return
        if("H" in command):
            print_function()
        print(command)        
            

#define Global
conn = RawConnection()

def remote_command():
    print("Remote IR init command Starting Up...")
    while True:
        ProcessIRRemote()