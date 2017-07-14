import os
import glob
import time
import subprocess
from time import gmtime, strftime
from peewee import *
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = round(float(temp_string) / 1000.0, 2)
        return temp_c


while True:
    t  = read_temp()
    ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #with open("/home/pi/temperature/temperature.txt", "a") as myfile:
    #    myfile.write(ts + ' ' + str(t) + "\n")
    #db = MySQLDatabase('temperature', user='temperature',passwd='hothothot')
    #query = 'INSERT into temperature (temperature, time) values ("'+str(t)+'", NOW())'
    #db.execute_sql(query)
    file = open('/var/www/html/temperature/index.html','w')
    file.write(str(t))
    file.close()
    # time.sleep(60)
    print(ts + ' T = ' + str(t))
    exit()
