import MySQLdb, datetime, os, math, sys, urllib, urllib2, pickle

#
#   TWOX is a helper class that performs functions that are common for all devices, e.g. logging,
#   notifications, SQL queries, etc.
# 

class twox() :

    def __init__(self) :
        self.logserver = os.getenv('TWOX_LOG_SERVER')
        self.db_host   = os.getenv('TWOX_LOG_SERVER')
        self.db_user   = os.getenv('TWOX_LOG_USER')
        self.db_passwd = os.getenv('TWOX_LOG_PASSWORD')
        self.db_db     = os.getenv('TWOX_LOG_DATABASE')
        self.led_file  = os.getenv('TWOX_LED_FILE')
        
        self.server    = os.getenv('TWOX_SERVER')
#        self.server    = os.getenv('TWOX_SERVER')
#        self.server    = os.getenv('TWOX_SERVER')
        

        # Make sure we have *some* variables set
        if (self.logserver == None) : 
            print("No evironment variables are set!")
            exit()

        self.timers = None

    # Excecute a MySQL query. If we want we can supply credentials that are not related to the logging db.
    def query_sql(self, sql, host = None, user = None, passwd = None, db = None) :  

        # if None supplied the use the log database
        if (host == None) : host = self.db_host
        if (user == None) : user = self.db_user
        if (passwd == None) : passwd = self.db_passwd
        if (db == None) : db = self.db_db

        # Connect to the DB with the credentials given in env vars
        db = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db )

        # Run the query
        cursor = db.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()

        # Close the connection
        db.close()

        return ret

    def time_since(self, event, location=None, value=None) :
        where = 'event = "' + event + '"'
        if (location != None) : where = where + ' AND location="' + location + '"'
        if (value != None) : where = where + ' AND value="' + value + '"'
        sql = 'SELECT TIME_TO_SEC(TIMEDIFF(NOW(), time)) FROM log WHERE '+ where +' ORDER by ID desc LIMIT 1'    
        ret = self.query_sql(sql)
        return int(ret[0][0])

    # Log an event
    def log(self, location, event, value='', tlimit='') : 
        try : 
            args = {'location': location, 'event': event, 'value': value, 'limit': limit}
            response = urllib2.urlopen('http://' + self.logserver + '/log/?' + urllib.urlencode(args))
        except:
            # Need to do something more useful here 
            self.alert_dev("Dude - unable to log!")
            print("Yo!")

    # Send a notification to the user
    def alert(self, message) : 
        os.system('sh $HOME/twox/scripts/slack_notification.sh $SLACK_NOTIFICATION_URL "' + message + '"')

    # Send a notification to the dev channel
    def alert_dev(self, message) : 
        os.system('sh $HOME/twox/scripts/slack_notification.sh $SLACK_DEV_URL "' + message + '"')

    # Some basic timer functions, applied throught the house
    def timer_start(self, name) : 
        self.timers[name] = time.time()

    # Stop the timer
    def timer_reset(self, name) : 
        self.timers[name] = None
 
    # Get the length of time a timer has been running for, with a format flag, if needed. 
    def timer_read(self, name, format = '') : 
        if (self.timers[name] == None) : return 0
        diff = time.time() - self.timers[name]
        if (format == 'm') : diff = diff / 60.0
        if (format == 'h') : diff = diff / 3600.0
        if (format == 'd') : diff = diff / 86400.0
        return diff

    # Trigger event on a remote device
    def trigger_event(self, server, event, value, port='8081') : 
        try : 
            args = {'event': event, 'value': value}
            response = urllib2.urlopen('http://' + server + ':' + port + '/event/?' + urllib.urlencode(args))
        except:
            # Need to do something more useful here 
            self.alert_dev("Dude - unable to sent event!")

    def update_led_file(self, led, val) :
        programmes = pickle.load( open( self.led_file, "rb" ) )
        programmes[led] = val
        pickle.dump( programmes, open( self.led_file, "wb" ) )
        return True
    
    def process_event(self, event, value='') :
        if (event == 'play-audio') :
            if (value != '') : 
                os.system('aplay ' + value)
                return True
            else : return False
        elif (event == 'led-green') : 
            return self.update_led_file('green', value)
        elif (event == 'led-red') : 
            return self.update_led_file('red', value)
        elif (event == 'led-clear') : 
            return self.update_led_file('clear', value)
        elif (event == 'led-yellow') : 
            return self.update_led_file('yellow', value)
            
#    def get_hour(self) :
        
            


