# Class for working with time
from machine import RTC

class JMBTime:
    """
    Class for working with time. This class requires an internet connection has already been established (see WIFI class).

    init(timezone) - Instantiate the class object
        timezone (str) - (optional) IANA Time Zone name or None (default)
    
    get_timezone - Issue a request to ipapi to obtain local IANA Time Zone name (must be connected to the internet)
        return (bool) - indicates success (True)
    
    set_rtc - Attempts to set Real Time Clock (RTC) using Network Time Protocol (NTP) (must be connected to the internet)
        return (bool) - indicates sucess (True)
    
    get_localtime - Obtains the current local time (timezone must already be set)
        return (tuple) - [year, month, day, weekday (1-7), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM)]
    """

    def __init__(self, timezone=None):
        """
        Initializes the JMBTIME object

        timezone (str) - (optional) IANA Time Zone name or None (default)
        """
        self.timezone = timezone
        # if self.timezone != None:
        #     self.set_timedelta()

    def get_localtime(self):
        """
        Obtains the current local time
        Requires timezone to already be set (either in constructor or using set_timezone)

        return (tuple) - (weekday (1-7), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM))
        """
        # Get the utc datetime
        rtc = RTC()
        dt_utc = rtc.datetime()

        # Compute hour offset
        hr = dt_utc[4] + self.offset
        if hr < 0:
            hr = 24 - (abs(hr) % 24)
            if hr == 24:
                hr = 0
        elif hr > 23:
            hr = hr % 24
        
        # Convert hour to 12-hour clock and set meridiem
        meridiem = 'AM' if hr < 12 else 'PM'
        if hr > 12:
            hr -= 12
        elif hr == 0:
            hr = 12

        return (dt_utc[3], hr, dt_utc[5], dt_utc[6], meridiem)