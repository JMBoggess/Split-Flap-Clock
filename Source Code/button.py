import asyncio
from machine import Pin
import time

class Button:
    """
    Class for controlling a button

    Attributes:
    pin (machine.Pin) - Pico Pin (In Pull Up) of the button
    event_click (asyncio.Event) - Event to trigger when the button is pressed
    event_long (asyncio.Event) - Event to trigger when the button is pressed and held for 2+ seconds

    """

    def __init__(self, pin_btn, event_click, event_long):
        """
        Setup the object

        pin_btn (int) - GPIO pin the button is connected to (In - other terminal sould be to ground)

        event_click (asyncio.event) - event to set for a single button press

        event_long (asyncio.event) - event to set when user pushes the button for more than 2 seconds
        """
        self.pin = Pin(pin_btn, Pin.IN, Pin.PULL_UP)
        self.state = 0  # 0=waiting for press; 1=currently pressed
        self.event_click = event_click
        self.event_long = event_long
        asyncio.create_task(self._listen())
    
    async def _listen(self):
        """
        Internal method used to listen for event types: click and long-click (2 seconds)
        """
        while True:
            if self.pin.value() == 0:
                # Button press
                if self.state == 0:
                    # First time the press has been detected
                    self.ts_press = time.ticks_ms()
                    self.state = 1
            else:
                # Button not pressed
                if self.state == 1:
                    # Button released, determine which event to set (if event is not already set)
                    if time.ticks_diff(time.ticks_ms(),self.ts_press) >= 2000:
                        if not self.event_long.is_set():
                            self.event_long.set()
                    else:
                        if not self.event_click.is_set():
                            self.event_click.set()
                    
                    self.state = 0
            
            await asyncio.sleep_ms(100)