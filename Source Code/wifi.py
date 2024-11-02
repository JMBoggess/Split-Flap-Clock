import asyncio
import network
from config import Config

class WIFI:
    """
    Class for connecting to a wifi network
    """

    def __init__(self):
        """
        Setup the object
        """
        # Setup the wlan object
        self.wlan = network.WLAN(network.STA_IF)
    
    def disconnect(self, print_debug=False):
        """
        Disconnects from a wireless network and deactivates the network interface

        print_debug (bool) - print debug statements (default: False)
        """
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
    
        # Debug
        if print_debug:
            print('Wifi Disconnected')

    async def connect(self, log):
        """
        Connects to wifi and returns an indicator status

        log (Log) - Log object to write detailed results

        return (str) - Returns either 'Success' or 'Failure' (user should see log in event of failure)
        """
        # Retrieve configuration
        config = Config()
        if config.ssid == None or config.password == None:
            log.write('No WIFI configuration settings found')
            return 'Failure'

        # Activate the network interface and connect to the wireless network
        self.wlan.active(True)
        self.wlan.connect(ssid=config.ssid, key=str(config.password))

        log.write(f'Connecting to wifi network: {config.ssid}')

        # Wait a max of 10 seconds for a connection
        i = 10

        while i > 0:
            # Check if connected
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break # Connected
            i -= 1

            await asyncio.sleep(1)
        
        # Determine final status to return
        if self.wlan.status() != 3:
            # Error attempting to connect - log the error
            if self.wlan.status() == -1:
                log.write('Error connecting to wifi network: (-1) CYW43_LINK_FAIL - Connection failed')
            elif self.wlan.status() == -2:
                log.write('Error connecting to wifi network: (-2) CYW43_LINK_NONET - No matching SSID found (could be out of range, or down)')
            elif self.wlan.status() == -3:
                log.write('Error connecting to wifi network: (-3) CYW43_LINK_BADAUTH - Authenticatation failure')
            else:
                log.write('Error connecting to wifi network: Error status code {}'.format(self.wlan.status()))
            
            return 'Failure'
        else:
            # Connected
            log.write('Successfully connected to wifi')
            return 'Success'
