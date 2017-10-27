#!/usr/bin/python
#
#        Usage:
#        python spi_mpc4251.py 100
#
import spidev, time, pickle, sys, os

# Set up the MCP4251-104 variable resistor
spi              = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000000 
pickfile         = os.getenv('HOME') + '/volume.pickle'

def main() : 
 
    # If we haven't run this yet, initialize the variable...  
    if (os.path.isfile(pickfile) == False) : 
         pickle.dump(128, open(pickfile, "wb")) 

    # Do some sanity checking
    volset = int(sys.argv[1])	
    vol    = pickle.load(open(pickfile, "rb"))
    if (volset == -1) : 
        print(vol)
        exit()
    if ((volset < 0) or (volset > 256)): 
        print("Invalid range " + str(volset) + " (0-256 is valid) ")
        exit()

    # Are we decreasing or increasing the volume	
    if (vol > volset) : step = -1
    else : step = 1
    
    # Change the volume by incrementing the reisstance - means that 
    # there will be no abrupt changes in temperature. Smooth! 	
    for i in range(vol, volset, step):
        if (vol > volset) : data = [0b00010100, 0b00000100]
        if (vol <= volset) : data = [0b00011000, 0b00001000]
        spi.writebytes(data)
        #print('VOLUME '  + str(i))
   
        # Keep pickling the current volume to file  
        pickle.dump(volset, open(pickfile, "wb")) 


if __name__ == "__main__":
   main()

