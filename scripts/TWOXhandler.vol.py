import TWOXhandler as handler
import pickle, vlc, os


class VolEvent(handler.TWOXhandler) : 
    def event_handler(self, event, value) : 
        if (event == 'play-audio') :
            if (value != '') : 
                self.play_sound(value)
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
        elif (event == 'radio-start') : 
        	return self.play_sound('http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio4fm_mf_p?s=1494265402')
        elif (event == 'radio-stop') : 
			return self.sound_off()
        elif (event == 'volume') : 
            self.volume = value
            return True

    def update_led_file(self, led, val) :
        programmes = pickle.load( open( self.led_file, "rb" ) )
        programmes[led] = val
        pickle.dump( programmes, open( self.led_file, "wb" ) )
        return True

    def sound_off(self):
        try:
            player.stop()
        except NameError as e:
            print("Nothin' is playing")

    def play_sound(self, station) :
        self.sound_off()
        instance = vlc.Instance()
        global player
        player = instance.media_player_new()
        media = instance.media_new(station)
        player.set_media(media)
        player.audio_set_volume(self.volume)
        player.play()
        return True

    def set_vars(self) :    
        self.logserver = os.getenv('TWOX_LOG_SERVER')
        self.led_file  = os.getenv('TWOX_LED_FILE')
        self.volume    = 45  

if __name__ == "__main__":
	handler.start_event_server(VolEvent)