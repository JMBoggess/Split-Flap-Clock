import network
from config import Config
from jmbtime import JMBTime
# from log import Log

class Response:
    """
    Handles Get/Post requests and prepares a web response

    Attributes
    exit_config (bool) - True if user wishes to exit configuration mode
    http_status (int) - HTTP Status of the response (200 = OK, 404 = Page requested not found)
    body (str) = HTML to insert into the body of the response

    Methods
    get(url) - Get request, currently handles:
        /           Home page
        /settings   Config settings form (WiFi and NTP use)
        /settime    Manually set date and time
        /log        Log messages
        /exit       Exit configuration mode
    
    post(url, kv) - Post request, currently handles:
        /settings/configure     User's responses to the Config settings form
        /settime/configure      User's reseponse to setting date and time manually
        
    """

    def __init__(self):
        """
        Initialize the response class
        """
        self.exit_config = False
        self.http_status = 200
        self.body = ""
    
    def get(self, url):
        """
        Get request: returns HTML response from the URL initiating the request

        url (str) - URL of the request
        """

        # Return the appropriate HTML based on the URL
        if url == '/':
            self.body = self._get_home()
        elif url == '/settings':
            self.body = self._get_settings()
        elif url == '/settime':
            self.body = self._get_settime()
        elif url == '/log':
            self.body = self._get_log()
        elif url == '/exit':
            self.exit_config = True
            self.body = self._get_exit()
        else:
            # Unknown get request, respond with an error
            self.http_status = 404
            self.body = '<p>Unexpected request</p><p>Return to the <a href="/">Home Page</a></p>'
        
    def post(self, url, kv):
        """
        Put request: returns HTML response after processing Post variables

        url (str) - URL of the request
        kv (dict) - Key-Value request parameters
        """
        # Process request and return appropriate body
        if url == '/settings/configure':
            self.body = self._post_configure(kv)
        elif url == '/settime/configure':
            self.body = self._post_settime(kv)
        else:
            self.http_status = 404
            self.body = '<p>Unexpected request</p><p>Return to the <a href="/">Home Page</a></p>'

    def _get_home(self):
        """
        Home page html
        """
        html = """<p><a href="/settings">Edit Settings</a></p>
            <p><a href="/settime">Manually set the date and time</a></p>
            <p><a href="/log">View Log</a> - program log messages</p>
            <p><a href="/exit">Exit Configuration</a></p>
        """
        return html

    def _get_settings(self):
        """
        Settings form to update the configuration
        """

        # Retrieve current config settings
        config = Config()

        # HTML heading
        html = """<h2>Settings</h2>
            <form method="post" action="/settings/configure">
            <p>Available Networks</p>
            <p><select name="ssid">
        """

        # Get the list of available networks
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        networks_avail = wlan.scan()
        wlan.active(False)

        for (ssid, bssid, channel, rssi, security, hidden) in networks_avail:
            ssid_name = ssid.decode('utf-8')
            if ssid_name == config.ssid:
                html += f'<option value="{ssid_name}" selected>{ssid_name}</option>'
            else:
                html += f'<option value="{ssid_name}">{ssid_name}</option>'
        
        html += '</select></p><p>Network Password</p><p><input type="password" name="pass" '
        
        if config.password != None:
            html += f'value="{config.password}" '
        
        html += '/><p><p><input type="checkbox" id="ntp" name="ntp" value="enabled" '
        
        if config.ntp_enabled == None or config.ntp_enabled == 1:
            html += 'checked '
        
        html += '/><label for="ntp">Enable automatic date time setting using my wifi information</label></p><p><select name="timezone">'

        timezones = [
            ['[Select One]', None], 
            ['Eastern Standard/Daylight Time (EST/EDT)','EST EDT'],
            ['Central Standard/Daylight Time (CST/CDT)','CST CDT'],
            ['Mountain Standard/Daylight Time (MST/MDT)','MST MDT'], 
            ['Mountain Standard Time (MST)','MST'],
            ['Pacific Standard/Daylight Time (PST/PDT)','PST PDT'],
            ['Alaska Standard/Daylight Time (AKST/AKDT)','AKST AKDT'],
            ['Hawaii Standard/Daylight Time (HST/HDT)','HST HDT'],
            ['Hawaii Standard Time (HST)','HST']
        ]

        for [k, v] in timezones:
            if v == config.timezone:
                html += f'<option value="{v}" selected>{k}</option>'
            else:
                html += f'<option value="{v}">{k}</option>'

        html += '</select></p><p><input type="submit" value="Submit" /></p></form><br /><p><a href="/">Return to Home Page</a></p>'

        return html

    def _get_settime(self):
        """
        Settings form to manually set date and time
        """

        # Retrieve the current date time according to the Real Time Clock (RTC)
        jmbtime = JMBTime()
        dt = jmbtime.get_localtime()
        hr = dt[4] if dt[7] == 'AM' else dt[4]+12

        # HTML to display
        html = f"""<h2>Manually Set Date Time</h2>
            <form method="post" action="/settime/configure">
            <p>Current Date and Time</p>
            <p><input type="datetime-local" name="dt" value="{dt[0]}-{dt[1]:02}-{dt[2]:02}T{hr:02}:{dt[5]:02}" required></p>
            <p><input type="submit" value="Submit"></p>
            </form>
            <br />
            <p><a href="/">Return to Home Page</a></p>
        """

        return html
    
    def _get_log(self):
        # log = Log()
        # return '<h2>Log</h2><p>' + log.read() + '</p><p><a href="/">Return to Home Page</a></p>'
        return '<h2>Log</h2><p>To be developed</p><a href="/">Return to Home Page</a></p>'
    
    def _get_exit(self):
        """
        User is going to exit, prior to exiting, send a message indicating Configuration mode is exited
        """
        html = "Configuration mode has been exited. To update the instagram counter, click the button."

        return html
    
    def _post_configure(self, kv: dict):
        """
        Accepts user-provided configuration values and sets the configuration file. If an error, user is notified.

        kv (dict) - dictionary of key-value pairs from the form the user completed
        """ 

        # Obtain values
        ssid = kv.get('ssid',None)
        pw = kv.get('pass',None)
        if pw == '':
            pw = None
        ntp = 1 if 'ntp' in kv else 0
        timezone = kv.get('timezone',None)
        if timezone == '' or timezone == 'None':
            timezone = None
        else: 
            timezone = timezone.replace('+',' ')

        # Update the configuration file
        config = Config()
        config.ssid = ssid
        config.password = pw
        config.ntp_enabled = ntp
        config.timezone = timezone
        config.write()

        # Notify user of success
        html = """<h2>Configuration Success</h2>
            <p>Configuration file updated successfully.</p>
            <p><a href="/">Home Page</a></p><br />
        """

        return html

    def _post_settime(self, kv: dict):
        """
        Takes user settings and updates the Real Time Clock (RTC)

        kv (dict) - dictionary of key-value pairs from the form the user completed
        """

        # Convert the date time string into a tuple to set the Real Time Clock (RTC)
        dt = kv['dt']
        y = int(dt[:4])
        m = int(dt[5:7])
        d = int(dt[8:10])
        h = int(dt[11:13])
        n = int(dt[-2:])

        # Set the Real Time Clock (RTC)
        jmbtime = JMBTime()
        jmbtime.set_rtc(y, m, d, h, n)

        # TODO: Move the display
        
        # Indicate success
        html = """<h2>Set Date Time Success</h2>
            <p>Date Time updated successfully.</p>
            <p><a href="/">Home Page</a></p>
        """
        return html