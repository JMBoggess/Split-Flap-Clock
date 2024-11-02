import json

class Config:
    """
    Handles interaction with the configuration file

    Properties:

    file (str) - name of the config file

    ssid (str) - name of the Wifi SSID network

    password (str) - password for the Wifi network

    ntp_enabled (int) - 0 = Do not use Network Time Protocol; 1 = Enable use of NTP

    timezone (str) - IANA Time Zone name

    Methods:

    read() - Read values in from config file

    write() - Write current values to config file
    """

    def __init__(self):
        """
        Setup the config object
        """
        self.file = "config.dat"
        self.read()
    
    def read(self):
        """
        Read in values from the config file. If file doesn't exist, values are set to None
        """
        try:
            with open(self.file, 'r') as f:
                settings = json.load(f)
            
            self.ssid = settings['ssid']
            self.password = settings['password']
            self.ntp_enabled = int(settings['ntp_enabled'])
            self.timezone = settings['timezone']
        except OSError:
            self.ssid = None
            self.password = None
            self.ntp_enabled = None
            self.timezone = None
    
    def write(self):
        """
        Write values to the config file
        """
        settings = {
            'ssid' : self.ssid,
            'password' : self.password, 
            'ntp_enabled' : str(self.ntp_enabled), 
            'timezone' : self.timezone
        }
        with open(self.file, 'w') as f:
            json.dump(settings,f)