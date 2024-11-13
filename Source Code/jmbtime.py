# Class for working with time
import asyncio
from log import Log
from machine import RTC
import ntptime

class JMBTime:
    """
    Class for working with time. This class requires an internet connection has already been established (see WIFI class).

    init() - Instantiate the class object

    load_timezone_offset(timezone) - load the timezone offsets (tz_offset, tz_offset_dst)

    set_rtc_ntp() - Attempts to set Real Time Clock (RTC) using Network Time Protocol (NTP) (must be connected to the internet)

    set_rtc(year, month, day, hours, min) - Set the Real Time Clock (RTC) using passed parameters

    get_localtime - Obtains the current local time (from RTC)
        return (tuple) - (year, month, day, weekday, hour, min, sec, meridiem)

    _ordinal(y,m,d) - Returns the number of days with 01-Jan-0001 as day 1

    _weekday(y,m,d) - Returns the day of week for the given date (0=Sunday)

    _date_from_ordinal(ordinial) - Returns the year, month, day from the ordinal days with 01-Jan-0001 as day 1
    
    Properties

    tz_offset (int) - Hours offset for the Timezone
    tz_offset_dst (int) - Hours offset for the Timezone during daylight savings time

    """

    def __init__(self, timezone):
        """
        Initializes the JMBTIME object
        """
        # Set timezone offsets
        self.load_timezone_offset(timezone)
    
    def load_timezone_offset(self, timezone):
        """
        Loads the timezone offset properties. If no time zone is set, offsets are 0 (UTC time)

        timezone (str) = Timezone as set in the Config file, valid values are:
            EST EDT
            CST CDT
            MST MDT
            MST
            PST PDT
            AKST SKDT
            HST HDT
            HST
        """
        if timezone is None:
            self.tz_offset = 0
            self.tz_offset_dst = 0
        else:
            # Reference list of time zones ('Time Zone', [Std Offset, Dst Offset])
            zones = {
                'EST EDT': (-5, -4), 
                'CST CDT': (-6, -5), 
                'MST MDT': (-7, -6), 
                'MST': (-7, -7), 
                'PST PDT': (-8, -7), 
                'AKST AKDT': (-9, -8), 
                'HST HDT': (-10, -9), 
                'HST': (-10, -10)
            }
            tz = zones.get(timezone,None)
            if tz is None:
                self.tz_offset = 0
                self.tz_offset_dst = 0
            else:
                self.tz_offset = tz[0]
                self.tz_offset_dst = tz[1]
    
    async def set_rtc_ntp(self):
        """
        Attempts to set Real Time Clock (RTC) using Network Time Protocol (NTP)
        Assumes pico is connected to the internet (i.e. wifi.connect())

        return (bool) - indicates success (True)
        """
        # Setup the log
        log = Log()

        # Set number of attempts
        i = 10 # Number of attempts
        time_set_success = False
        while i > 0:
            i -= 1
            try:
                ntptime.settime()
                time_set_success = True
                i = 0
            except OSError:
                await asyncio.sleep(1)
                continue
        
        if time_set_success:
            # Time is now in UTC, convert to time offset
            rtc = RTC()
            dt_utc = rtc.datetime()

            # Determine if we are in daylight savings
            #   Daylight savings between: 2nd Sunday of March - 1st Sunday of November

            # 2nd Sunday of March
            dst_start_wd = self._weekday(dt_utc[0], 3, 8)   # 8th is the earliest the second Sunday could be on
            dst_start = self._ordinal(dt_utc[0], 3, 8 if dst_start_wd == 0 else 8 + (7 - dst_start_wd))
            
            # 1st Sunday of November
            dst_end_wd = self._weekday(dt_utc[0], 11, 1)  # 1st is the earliest the first Sunday could be on
            dst_end = self._ordinal(dt_utc[0], 11, 1 if dst_end_wd == 0 else 1 + (7 - dst_end_wd))

            # Current date
            dt = self._ordinal(dt_utc[0], dt_utc[1], dt_utc[2])

            # Hours to offset
            hours_offset = self.tz_offset_dst if dt >= dst_start and dt <= dst_end else self.tz_offset

            # Set new hour
            h = dt_utc[4] + hours_offset
            if h < 0:
                # Subtract one day
                dt -= 1
                h += 24
            
            # Obtain new year, month, day
            y, m, d = self._date_from_ordinal(dt)

            # Obtain weekday (weekday should be 0=Monday, 7=Sunday)
            wd = self._weekday(y, m, d)
            if wd > 0:
                wd -= 1
            else:
                wd = 6

            # Obtain Min, Sec, Subsec (waited until this point to keep time as precise as possible)
            dt_now = rtc.datetime()

            # Log settings
            log.write('RTC time set by NTP, updated to timezone, following is DateTime:')
            log.write(f'Year={y}, Month={m}, Day={d}, Weekday={wd}, Hour={h}, Min={dt_now[5]}, Sec={dt_now[6]}, Subsec={dt_now[7]}')

            # Set datetime
            try:
                rtc.datetime((y, m, d, wd, h, dt_now[5], dt_now[6], dt_now[7]))
            except OSError:
                # Raise the error (will be logged in main)
                raise



        return time_set_success

    def set_rtc(self, year, month, day, hours, min):
        """
        Sets the Real Time Clock (RTC) using the passed Date Time info

        year (int) - 4-digit year
        month (int) - 1-12
        day (int) - 1-31
        hours (int) - 0-23
        min (int) - 0-59
        """
        # Note in RTC.datetime, the weekday component is 0=Monday, 6=Sunday
        rtc = RTC()
        wd = self._weekday(year, month, day)  # 0 = Sunday
        rtc.datetime((year,month,day, wd - 1 if wd > 0 else 6,hours,min,0,0))

    def get_localtime(self):
        """
        Obtains the current local time from the Real Time Clock (RTC)

        return (tuple) - (year, month (1-12), day (1-31), weekday (0-6:Sun-Sat), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM))
        """
        # Get the utc datetime from the Real Time Clock
        rtc = RTC()
        dt_utc = rtc.datetime()

        # Convert Weekday (0=Monday to 0=Sunday)
        wd = dt_utc[3] + 1
        if wd == 7:
            wd == 0
        
        # Convert hour to 12-hour clock and set meridiem
        hr = dt_utc[4]
        meridiem = 'AM' if hr < 12 else 'PM'
        if hr > 12:
            hr -= 12
        elif hr == 0:
            hr = 12
        
        return (dt_utc[0], dt_utc[1], dt_utc[2], wd, hr, dt_utc[5], dt_utc[6], meridiem)

    def _ordinal(self, y, m, d):
        """
        The number of days with 01-Jan-0001 as day
        
        y (int) = 4-digit year
        m (int) = month (1-12)
        d (int) = day (1-31)
        """
        # ordinal_year -> number of days before January 1st of year.
        ly = y - 1
        ordinal_year = ly * 365 + ly // 4 - ly // 100 + ly // 400

        # ordinal_month > number of days in year preceding first day of month.
        days_before_month = (0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
        leap_year = y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
        ordinal_month = days_before_month[m] + (m > 2 and leap_year)

        return ordinal_year + ordinal_month + d

    def _weekday(self, y, m, d):
        """
        Returns the day-of-week (0=Sunday, 1=Monday, 6=Saturday) for a given date

        y (int) = 4-digit year
        m (int) = month (1-12)
        d (int) = day (1-31)
        """
        # Return the weekday
        return (self._ordinal(y,m,d) + 6) % 7
    
    def _date_from_ordinal(self, ordinal):
        """
        Ordinal (number of days, considering 01-Jan-0001 as day 1) converted to year, month, day
        """
        # Subtract 1 from the ordinal date
        n = ordinal - 1
        n400, n = divmod(n, 146_097)
        y = n400 * 400 + 1
        n100, n = divmod(n, 36_524)
        n4, n = divmod(n, 1_461)
        n1, n = divmod(n, 365)
        y += n100 * 100 + n4 * 4 + n1
        if n1 == 4 or n100 == 4:
            return y - 1, 12, 31
        m = (n + 50) >> 5

        days_before_month = (0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
        leap_year = y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
        prec = days_before_month[m] + (m > 2 and leap_year)

        if prec > n:
            m -= 1
            if m == 2 and leap_year:
                prec -= 29
            else:
                days_in_month = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
                prec -= days_in_month[m]

        n -= prec
        return y, m, n + 1

