import asyncio
from button import Button
from config import Config
from display import Display
from jmbtime import JMBTime
from led import LED
from log import Log
from timer import Timer
from wifi import WIFI
from wifiap import WIFIAP

########## Global Methods

def current_state():
    """
    Checks the global tasks and returns the current state of the program

    Returns (int):
        1: Idle - No global task is currently running
        2: Config - Configuration mode is running
        3: Set DateTime - Set Date Time mode, using NTP if configured and running Display Update mode
    """
    global task_config
    global task_setdt

    if task_setdt != None and not task_setdt.done():
        return 3
    elif task_config != None and not task_config.done():
        return 2
    else:
        return 1
    
########## Waiters and Timers

async def timer_display_update():
    """
    Ensures the display is updated every minute
    """
    global jmbtime
    global task_display_update
    
    while True:
        # Run Display Update mode (if not currently running)
        sleep_sec = 60
        if task_display_update == None or task_display_update.done():
            task_display_update = asyncio.create_task(display_update_mode())
            await task_display_update
            dt = jmbtime.get_localtime()
            sleep_sec = 60 - dt[6]

        # Wait for the next minute occurrance
        await asyncio.sleep(sleep_sec)

async def waiter_timer_setdt():
    """
    Respond to the timer event to trigger Set Date Time mode
    """
    global event_timer_setdt
    global task_setdt

    while True:
        # Wait for the timer event
        await event_timer_setdt.wait()

        # Event has been triggered, check state of program
        if current_state() == 1:
            # Create the Set Date Time task
            task_setdt = asyncio.create_task(setdt_mode())

        # Reset the event
        event_timer_setdt.clear()

async def waiter_btn_config_click():
    """
    Respond to single button click: Enter Config mode
    """
    global event_btn_config_click
    global task_config

    while True:
        # Wait for the button click
        await event_btn_config_click.wait()

        # Check current program state (only execute if Idle)
        if current_state() == 1:
            # Create the config task
            task_config = asyncio.create_task(config_mode())
        
        # Reset the event
        event_btn_config_click.clear()

async def waiter_btn_config_cancel_click():
    """
    Respond to long button click: Cancel Config mode
    """
    global event_btn_config_cancel_click
    global task_config

    while True:
        # Wait for the long button click
        await event_btn_config_cancel_click.wait()

        # Check current program state (only execute if Config is running)
        if current_state() == 2:
            # Cancel the task (assume cancellation, LED will turn off when completed)
            _ = task_config.cancel()
    
        # Clear the event to wait for the next long click
        event_btn_config_cancel_click.clear()

async def waiter_btn_setdt_click():
    """
    Respond to single button click: Set Date and Time and display
    """
    global event_btn_setdt_click
    global task_setdt

    while True:
        # Wait for the button click
        await event_btn_setdt_click.wait()

        # Check program state (only execute if idle)
        if current_state() == 1:
                # Create the setdt task
                task_setdt = asyncio.create_task(setdt_mode())

        # Reset the event
        event_btn_setdt_click.clear()

async def waiter_btn_setdt_cancel_click():
    """
    Respond to long button click: Cancel Set Date Time mode
    """
    global event_btn_setdt_cancel_click
    global task_setdt

    while True:
        # Wait for the long button click
        await event_btn_setdt_cancel_click.wait()

        # Check if the Set Date Time task is running (Program State = 3)
        if current_state() == 3:
            # Cancel the event (assume cancellation, LED will shut off when complete)
            task_setdt.cancel()

        # Clear the event to wait for the next long click
        event_btn_setdt_cancel_click.clear()

########## Modes

async def config_mode():
    """
    Main method for configuration mode
    """
    global config
    global jmbtime
    global led
    global wifiap
    global wifi

    # Main code
    try:
        # Set light blinking to indicate config mode is starting
        led.blink_constant()

        # Disconnect wifi (only disconnects if currently connected)
        wifi.disconnect()

        # Start the server
        await wifiap.start_server(print_status=True)

        # Wait for Exit event
        await event_config_exit.wait()

        # User is done
        event_config_exit.clear()
        
    finally:
        # Code to execute even if task is canceled

        # Stop the server
        wifiap.stop_server()

        # Turn of the config light
        led.off()

        # Ensure the config object is updated with the latest config data
        config.read()

        # Ensure JMBTime has the correct Timezone offsets
        jmbtime.load_timezone_offset(config.timezone)


async def setdt_mode():
    """
    Updates the Real Time Clock (RTC) using the Network Time Protocol (NTP), if enabled, and then updates the display time
    """
    global jmbtime
    global led
    global task_display_update
    global wifi

    # Turn on the led
    led.on()

    # Is NPT mode enabled?
    if config.ntp_enabled == 1:
        # Start the log
        log = Log()
        log.write('Start the Set Date Time process', 'w')

        try:
            # Wifi Connection
            if not wifi.wlan.isconnected():
                # Attempt to connect
                if await wifi.connect(log) == "Failure":
                    # Error has been written to log, give the error blink code to the user, and exit
                    led.blink_error()
                    return

            # Set the Date Time
            await jmbtime.set_rtc_ntp()

        except asyncio.CancelledError:
            # Task was canceled
            log.write("User canceled Set Date Time process")
            led.blink_error()
            raise # Raise the error up
            
        except OSError as err:
            # Unknown error
            log.write(f'{err=}')
            raise

    # Update the display (if not already running)
    if task_display_update == None or task_display_update.done():
        task_display_update = asyncio.create_task(display_update_mode())
        await task_display_update
    
    # Turn off the led to indicate the mode is finished
    led.off()

async def display_update_mode():
    """
    Updates the display with the date and time as set in the Real Time Clock (RTC)
    """
    global display
    global jmbtime

    # Get the datetime tuple (year, month (1-12), day (1-31), weekday (0-6:Sun-Sat), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM))
    dt = jmbtime.get_localtime()

    # Update the display
    display.display_datetime(dt)
    # print(dt) # Debug line


########## Main Method
async def main():
    """
    Main program loop
    """
    global task_setdt
    global timer_setdt

    # Set the Date Time
    task_setdt = asyncio.create_task(setdt_mode())
    await task_setdt

    # Waiters and Timers
    asyncio.create_task(timer_display_update()) # This will update the display immediately again, however, the previous code should have already set the correcte date/time
    asyncio.create_task(waiter_timer_setdt())
    asyncio.create_task(waiter_btn_config_click())
    asyncio.create_task(waiter_btn_config_cancel_click())
    asyncio.create_task(waiter_btn_setdt_click())
    asyncio.create_task(waiter_btn_setdt_cancel_click())

    # Start the Set Date and Time Timer
    timer_setdt.start()

    # Infinite loop
    while True:
        # Ensure the program continues to run
        await asyncio.sleep(60)

#### Globals

# Events
event_timer_setdt = asyncio.Event()
event_btn_config_click = asyncio.Event()
event_btn_config_cancel_click = asyncio.Event()
event_btn_setdt_click = asyncio.Event()
event_btn_setdt_cancel_click = asyncio.Event()
event_config_exit = asyncio.Event() # Used in wifi app to indicate when user clicks Exit

# Objects
config = Config()
display = Display([15,14,13],[1,2,3,4,5])
timer_setdt = Timer(event_timer_setdt, 3600, 60) # One hour timer (3,600 seconds) wait 1 min (60 sec) between timer checks
btn_config = Button(18, event_btn_config_click, event_btn_config_cancel_click)
btn_setdt = Button(19, event_btn_setdt_click, event_btn_setdt_cancel_click)
jmbtime = JMBTime(config.timezone)
led = LED(16)
wifiap = WIFIAP(event_config_exit)
wifi = WIFI()

# Tasks
task_config = None
task_display_update = None
task_setdt = None

# Start the prgoram
try:
    asyncio.run(main())
except KeyboardInterrupt:
    # Ensure LED is off
    led.off()
finally:
    asyncio.new_event_loop()