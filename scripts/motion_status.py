import RPi.GPIO as GPIO
import time
import pigpio


#GPIO.setup(self.motionpin, GPIO.IN)
GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()
print('22')
print(pi.get_PWM_dutycycle(22))
print('24')
print(pi.get_PWM_dutycycle(24))
print(pi.get_PWM_dutycycle(17))

class KitchenMotion: 

    redpin = 22
    bluepin = 17
    greenpin = 24
    motionpin = 6
    fadesteps = 100 
    fadetime = 0.01

    defcols = [255, 255, 255] 
    color = [0, 0, 0]

    onoff = 0

    ts = time.time()

    pi = pigpio.pi()

    def __init__(self):
        print("Starting Motion Sensor")
        GPIO.setup(self.motionpin, GPIO.IN)
        GPIO.setmode(GPIO.BCM)
        self.setColor([0, 0, 0])
        self.getState();
        self.getColor();

    def getState(self):
         self.onoff = self.pi.get_PWM_dutycycle(self.redpin) + self.pi.get_PWM_dutycycle(self.bluepin) + self.pi.get_PWM_dutycycle(self.greenpin)     
         return self.onoff

    def getColor(self):
         self.color = [self.pi.get_PWM_dutycycle(self.redpin), self.pi.get_PWM_dutycycle(self.bluepin), self.pi.get_PWM_dutycycle(self.greenpin)]     
         return self.color 


    def setColor(self, color):
         pins = [self.redpin, self.bluepin, self.greenpin]
         oldcols = self.getColor()
         for i in range(1, self.fadesteps - 1):
              for j in range(0, 3):
                   colorval = self.pi.get_PWM_dutycycle(pins[j]) + (color[j] - oldcols[j])/self.fadesteps
                   if ((colorval > 0) and (colorval < 256)):
                      self.pi.set_PWM_dutycycle(pins[j], colorval)
                   time.sleep(self.fadetime)

         # Make sure the precice color is set if our rounding was off
         for j in range(0, 3): 
              self.pi.set_PWM_dutycycle(pins[j], color[j])


    def flipState(self):
        if (self.getState() == 0):
            self.setColor(self.defcols)
            # for i in range(1, self.fadesteps - 1):
            #     self.pi.set_PWM_dutycycle(self.redpin,  self.pi.get_PWM_dutycycle(self.redpin) + self.defcols[0]/self.fadesteps)
            #     self.pi.set_PWM_dutycycle(self.bluepin,  self.pi.get_PWM_dutycycle(self.bluepin) + self.defcols[1]/self.fadesteps)
            #     self.pi.set_PWM_dutycycle(self.greenpin,  self.pi.get_PWM_dutycycle(self.greenpin) + self.defcols[2]/self.fadesteps)
            #     time.sleep(self.fadetime)
        else: 
             self.setColor([0, 0, 0])
             #self.pi.set_PWM_dutycycle(self.redpin,  0)
             #self.pi.set_PWM_dutycycle(self.bluepin,  0)
             #self.pi.set_PWM_dutycycle(self.greenpin,  0)
             #for i in range(1, self.fadesteps - 1):
             #    self.pi.set_PWM_dutycycle(self.redpin,  self.pi.get_PWM_dutycycle(self.redpin) - self.defcols[0]/self.fadesteps)
             #    self.pi.set_PWM_dutycycle(self.bluepin,  self.pi.get_PWM_dutycycle(self.bluepin) - self.defcols[1]/self.fadesteps)
             #    self.pi.set_PWM_dutycycle(self.greenpin,  self.pi.get_PWM_dutycycle(self.greenpin) - self.defcols[2]/self.fadesteps)
             #    time.sleep(self.fadetime)
	self.getState()

    def run(self):

        try:
            while True:
                # if (self.getState() == 0) :
                if GPIO.input(self.motionpin):
                    # Start a timer 
                    self.ts = time.time()
                    print("Motion Detected " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    if (self.onoff == 0): self.flipState()
                    with open('/var/www/html/motion/index.html', 'w') as the_file:
                        the_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    # print(self.onoff)
                    time.sleep(5)
                else:                    
                    if (time.time() - self.ts > 60): 
		        if (self.onoff > 0): self.flipState()
                    time.sleep(1)

            time.sleep(1)
        except KeyboardInterrupt:
             print "Quit"
             GPIO.cleanup()


KM = KitchenMotion()
KM.run()
