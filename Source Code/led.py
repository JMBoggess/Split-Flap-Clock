import asyncio
from machine import Pin
from button import Button

class LED:
    """
    Class for controlling an LED

    Attributes:
    pin (machine.Pin) - the Pico Pin Out of the LED

    Methods:
    blink_constant() - blinks the LED at a constant rate indefinitely
    blink_error() - blinks the LED in a series of 4 short flashes 5 times and then stops
    on() - turns the LED on
    off() - turns the LED off
    """
    def __init__(self, pin_led):
        self.pin = Pin(pin_led, Pin.OUT)
        self._blink_constant_on = False
        self._blink_error_on = False
    
    async def _blink_constant(self):
        """
        Async event to run constant blinking light
        """
        while self._blink_constant_on == True:
            self.pin.toggle()
            await asyncio.sleep_ms(500)
    
    async def _blink_error(self):
        """
        Async even to run blinking error light
        4 blinks (8 on/off cycles) followed by a pause run this 5 times
        
        """
        blink_count = 8 * 5
        while self._blink_error_on == True:
            if blink_count > 0:
                self.pin.toggle()
                if blink_count % 8 == 1:
                    await asyncio.sleep_ms(1000)
                else:
                    await asyncio.sleep_ms(200)
                blink_count -= 1
            else:
                self._blink_error_on = False
    
    def blink_constant(self):
        """
        Constant blinking light
        """
        # Disable any other modes
        self._blink_error_on = False
        self.pin.off()

        # Enable this mode and start the async function
        self._blink_constant_on = True
        asyncio.create_task(self._blink_constant())

    def blink_error(self):
        """
        Error blinking light (4 short blinks followed by a pause)
        """
        # Disable any other modes
        self._blink_constant_on = False
        self.pin.off()

        # Enable this mode and start the async function
        self._blink_error_on = True
        asyncio.create_task(self._blink_error())
    
    def on(self):
        """
        Turn on the LED
        """
        # Disable any other modes
        self._blink_constant_on = False
        self._blink_error_on = False

        # Turn on LED
        self.pin.on()
    
    def off(self):
        """
        Turn off the LED
        """
        # Disable any other modes
        self._blink_constant_on = False
        self._blink_error_on = False

        # Turn off LED
        self.pin.off()
