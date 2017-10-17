#!/usr/bin/python
import MySQLdb, datetime, os
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_log(location, event):

    # Connect to the db and execute our query
    db = MySQLdb.connect( host   = os.getenv('TWOX_LOG_SERVER'), 
                          user   = os.getenv('TWOX_LOG_USER'), 
                          passwd = os.getenv('TWOX_LOG_PASSWORD'),
                          db     = os.getenv('TWOX_LOG_DATABASE')
    ) 
    cursor = db.cursor()
    cursor.execute("SELECT time, value FROM log where DATE(time) = subdate(current_date, 1) AND location='" + location + "' AND event='" + event + "'")


    # List comprahend down to neat arrays
    ret = cursor.fetchall()
    times  = [row[0] for row in ret]
    values = [row[1] for row in ret]

    # Close the connection
    db.close()

    return times, values



times, values = get_log('kitchen', 'motion')
  
layout = 310

fig = plt.figure()
ax = fig.add_subplot(layout + 3)
for val in times :
    xx = [val, val]
    yy = [0, 1]
    ax.plot(xx, yy, color='red', linewidth=0.4)
myFmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)
ax.set_yticks([])
ax.set_ylabel('Kitchen Motion')
ax.set_xlabel('Time (h:m)')
# fig.autofmt_xdate()
ax.set_xlim([datetime.date.today() - datetime.timedelta(1), datetime.date.today()])

times, values = get_log('None', 'temperature')


ax2 = fig.add_subplot(layout + 2)
ax2.plot(times, values)
ax2.set_xlim([datetime.date.today() - datetime.timedelta(1), datetime.date.today()])
ax2.set_xticks([])
ax2.set_ylabel('Temp (C)')

fig.savefig('/home/pi/test.pdf')


