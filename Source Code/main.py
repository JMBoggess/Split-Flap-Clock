import asyncio
from button import Button
from jmbtime import JMBTime
from led import LED
from timer import Timer
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
    global task_display_update
    
    while True:
        # Run Display Update mode (if not currently running)
        sleep_sec = 60
        if task_display_update == None or task_display_update.done():
            task_display_update = asyncio.create_task(display_update_mode())
            dt = await task_display_update
            sleep_sec = 60 - dt[3]

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
    global led
    # global wifiap
    # global wifi

    # Main code
    try:
        # Set light blinking to indicate config mode is starting
        led.blink_constant()

        # Disconnect wifi (only disconnects if currently connected)
        # wifi.disconnect()

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

async def setdt_mode():
    """
    
    """
    global task_display_update

    # Update the display (if not already running)
    if task_display_update == None or task_display_update.done():
        task_display_update = asyncio.create_task(display_update_mode())
        await task_display_update

async def display_update_mode():
    """
    Updates the display with the date and time as set in the Real Time Clock (RTC)

    return (tuple) - (weekday (1-7), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM))
    """
    print('Run: Display Update Mode')
    return (1,1,0,0,'AM')



########## Main Method
async def main():
    """
    Main program loop
    """
    global timer_setdt

    # Waiters and Timers
    asyncio.create_task(timer_display_update())
    asyncio.create_task(waiter_timer_setdt())
    asyncio.create_task(waiter_btn_config_click())
    asyncio.create_task(waiter_btn_config_cancel_click())
    asyncio.create_task(waiter_btn_setdt_click())
    asyncio.create_task(waiter_btn_setdt_cancel_click())

    # Set the Date Time using NTP if configured
    # TODO: if config, run NTP Time Update mode

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
# display = Display([11,12,13],[21,20,26,27])
timer_setdt = Timer(event_timer_setdt, 3600, 60) # One hour timer (3,600 seconds) wait 1 min (60 sec) between timer checks
btn_config = Button(18, event_btn_config_click, event_btn_config_cancel_click)
btn_setdt = Button(19, event_btn_setdt_click, event_btn_setdt_cancel_click)
jmbtime = JMBTime()
led = LED(16)
wifiap = WIFIAP(event_config_exit)
# wifi = WIFI()
# instagram = Instagram()

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