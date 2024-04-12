import os
import sys
from subprocess import Popen, PIPE, STDOUT
import time
import re

#
# config
#

# command to get LEDA card information
ledagssh        =   "ledag-ssh -o localhost"

# prefix of command to enter LEDA prompt with board selection
ledagssh_select =   "ledag-ssh -o localhost -s"


#
# globals
#

# print extra messages for debugging
verbose = False

def get_leda_info( ):
    '''Get LedaG card info.'''

    slots = []

    #
    # This is gnarly code to invoke the ledagssh command,
    # async capture the output, detect the ledagssh prompt, 
    # and send it the quit command, and capture any error
    # code when the process exits.
    #
    cmd = ledagssh.split()
    if verbose: print("\nRunning leda command", cmd, "\n" )
    p = Popen( cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT) 
    os.set_blocking(p.stdout.fileno(), False)
    while True:
        if p.poll()!=None:
            if verbose: print("leda command terminated.")
            if p.returncode!=0:
                print("ERROR: Leda command returned error code %d" % p.returncode)
                return False
            else: break
        b = p.stdout.readline()
        if b==b'':   
            time.sleep(0.01)
            continue
        bs = b.decode('utf-8')
        if verbose: print("leda output: %s" % bs, end="")
        if bs.find("slot")>=0:
            slots.append( bs )
        if bs.startswith("localhost >"):
            if verbose: print()
            p.communicate( str.encode("quit") )

    if verbose: print("ledag slot info:", slots)

    # return number of boards and the board slot details array
    return len(slots), slots


def get_board_power( board_num,  ):
    '''Get board power info.'''

    slots = []
    got_power = False

    #
    # This is gnarly code to invoke the ledagssh command,
    # async capture the output, detect the ledagssh prompt, 
    # and send it the quit command, and capture any error
    # code when the process exits.
    #
    cmd = ledagssh_select.split() + [ str(board_num) ]
    if verbose: print("\nRunning leda command", cmd, "\n" )
    p = Popen( cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    os.set_blocking(p.stdout.fileno(), False)
    while True:
        if p.poll()!=None:
            if verbose: print("leda command terminated.")
            if p.returncode!=0:
                print("ERROR: Leda command returned error code %d" % p.returncode)
                return False
            else: break
        b = p.stdout.readline()
        if b==b'':
            time.sleep(0.01)
            continue
        bs = b.decode('utf-8')
        if verbose: print("leda output: %s" % bs, end="")
        if bs.find("slot")>=0:
            slots.append( bs )
        if bs.startswith("slot"):
            if verbose: print()
            p.stdin.write( str.encode("calc_pwr\n") )
            p.stdin.flush()
        if bs.startswith("Board Power"):
            if verbose: print()
            got_power = bs
            p.communicate( str.encode("quit\n") )
            break

    if got_power:
        regex = re.compile("Board Power \((.+)\):(.*)")
        #regex = re.compile("Board Power (.*)")
        matches = regex.match( got_power )
        if matches:
            units = matches.groups()[0]
            val = float(matches.groups()[1].strip())
            powerstr = "%f %s" % (val, units)
            if verbose: print("Got power:", powerstr)
            return powerstr 
      
    if verbose: print("ERROR: Could not get power.")            
    return False


#
# unit tests
#
if __name__ == "__main__":

    print("Executing unit tests for", sys.argv[0])
    filePointer = open("powerTest.txt",'w')
    for i in range(100):
        #print("Trying to get board power...")
        power = get_board_power(0)
        filePointer = open("powerTest.txt",'a')
        filePointer.write(str(power)+"\n")
        filePointer.close()
