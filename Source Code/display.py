# Used to display the desired date time
# Do not use asyncio to sleep for stepper motor
#   Requires microseconds, it doesn't appear this is recommended or possible with asyncio sleep/sleep_ms
from machine import Pin
from time import sleep_us

class Display:
    """
    Class for displaying desired digits

    Methods:
    display_datetime() - sets the split-flap displays to display the date and time

    Components:
        Stepper Motor (28BYJ-48)
        Driver Board (ULN2003)
        Hall effect sensor (A3144)
        8-bit Serial-In Parellel-Out (SIPO) Shift Register (74HC595)
    
    Pin Configuration:
        Stepper Motor connects to Driver Board
        Driver Board
            GND (-) > Ground pin
            VCC (+) > SysBus (5v) - assumes pico is powered by USB
            IN1-4 > Shift Register
        Shift Register
            1-7,15 QA-QH - driver boards (2 driver boards)
            8 GND > Ground
            9 QH' > Daisy chain > Shift Register 14 (serial input)
            10 SRCLR (shift register clear) - SysBus 5 Volts
            11 SRCLK "clock" (shift register clock) - GPIO (all shift registers use the same pin)
            12 RCLK "latch" (storage register clock) - GPIO (all shift registers use the same pin)
            13 OE (output enable) - Ground
            14 SER (serial input) - GPIO (first shift register goes to Pico pin, remaining are daisy chained)
            16 VCC - SysBus 5 volts
            Note: SysBus 5 Volts - used for simplicity since Driver Boards are connected to this
                Assumes Pico W is powered by USB
                HC595 can also be powered by 3.3V instead
                Daisy Chain example: GPIO > Shift Register 1 pin 14 (serial input) > Shift Register 1 pin 9 > Shift register 2 pin 14 > Shift 2 pin 9 > Shift 3 pin 14...
        Hall sensor
            GND (-) > Ground pin
            VC (+) > SysBus (5v)
            IN > Any GPIO - use Pin.PULL_UP
    """

    def __init__(self, pins_sr, pins_hall):
        """
        Initialize the display object

        pins_sr ([int,int,int]) - List of Pico GPIO pins the Shift Registers are connected to, in the following order:
            0 - Clock: Shift Register Clock (pin 11 on shift register)
            1 - Latch: Storage Register Clock (pin 12 on shift register)
            2 - Serial Input (pin 14 on shift register)
        
        pins_hall ([int,int,...]) - List of Pico GPIO pins the Hall sensors are connected to, 0 = left-most digit
        """
        ########## Set Pins

        # Hall Sensors (10)
        self.pins_hall = [Pin(pin_hall, Pin.IN, Pin.PULL_UP) for pin_hall in pins_hall]

        # Shift Register
        self.pin_clock = Pin(pins_sr[0], Pin.OUT)
        self.pin_latch = Pin(pins_sr[1], Pin.OUT)
        self.pin_serial = Pin(pins_sr[2], Pin.OUT)

        ########## Constants
            
        # Array of flaps - first value (index: 0) should be the Home character
        self.flap_values_digit = ['0','1','2','3','4','5','6','7','8','9',',',':','!',' ']
        self.flap_values_dow = ['0-AM','0-PM','1-AM','1-PM','2-AM','2-PM','3-AM','3-PM','4-AM','4-PM','5-AM','5-PM','6-AM','6-PM']

        # Number of split-flap displays
        self.display_count = 4 # TODO: change to 5
        self.shift_register_count = 2 # TODO: change to 3

        # Flap Value Current - the current index of the character displayed (If unknown or not set: None)
        self.flap_value_current = [None] * self.display_count

        # Flap Count - (Added to reduce redundant code: len function calls)
        self.flap_count = 14

        # Seq - Motor step sequence (order to set motor pins to rotate motor)
        #   Index 0 - sequence step
        #   Index 1 - 0 = no display turns, 1 = right-only, 2 = left-only, 3 = both turn
        self.seq = [[0,3,48,51],[0,6,96,102],[0,12,192,204],[0,9,144,153]]
        
        # Home Reads - Number of positive magnet reads to set as home position
        self.home_reads = 90

    def display_datetime(self, dt):
        """
        Rotates the displays to display the desired text

        dt (tuple) - (year, month (1-12), day (1-31), weekday (0-6:Sun-Sat), hour (1-12), min (0-59), sec (0-59), meridiem (AM/PM))
        """
        # Convert datetime elements to target index
        h = f'{dt[4]:2}'
        m = f'{dt[5]:02}'
        flap_0 = self.flap_values_digit.index(h[:1])
        flap_1 = self.flap_values_digit.index(h[1:])
        flap_2 = self.flap_values_digit.index(m[:1])
        flap_3 = self.flap_values_digit.index(m[1:])
        # flap_4 = self.flap_values_dow.index(f'{dt[3]}-{dt[7]}') # TODO: uncomment
        self.flap_value_target = [flap_0,flap_1,flap_2,flap_3] # TODO: add back: ,flap_4]

        # Initialize sequence index (0-3)
        seq_index = 0

        # Set maximum attempts to reach target characters (min of 2), expected possibilities for each flap:
        #   1) already at target (0 attempts)
        #   2) go to character (1 attempt)
        #   3) go home > go to character (2 attempts)
        #   4) Error finding character or home (3+ attempts)
        max_attempts = 3

        # Determine steps to turn each display to reach the desired value
        steps_remaining = [self._calculate_steps(i) for i in range(self.display_count)]
        # steps_remaining.append(0) # TODO: uncomment (keep following comment) Account for no 6th display

        # Start attempts
        while sum(map(abs, steps_remaining)) > 0 and max_attempts > 0:

            # Set maximum number of steps to prevent potentially endless running (1.25 revolutions 2048 + 512)
            steps_max = 2560

            # Advance Steps
            while sum(map(abs, steps_remaining)) > 0 and steps_max > 0:
                # Take a step
                bytes_seq = [self.seq[seq_index][(0 if steps_remaining[i] == 0 else 1) * 2 + (0 if steps_remaining[i+1] == 0 else 1)] for i in range(0, self.display_count, 2)]
                self._bytes_out(bytes_seq)

                # Determine Steps Remianing
                for i in range(self.display_count):
                    if steps_remaining[i] > 0:
                        # Decrement steps
                        steps_remaining[i] -= 1

                    elif steps_remaining[i] == -1:
                        # Determine if off magnet
                        if self.pins_hall[i].value() == 1:
                            # Find first magnet read
                            steps_remaining[i] = -2
                    
                    elif steps_remaining[i] == -2:
                        # Determine if magnet read
                        if self.pins_hall[i].value() == 0:
                            # Advance to home position
                            steps_remaining[i] = self.home_reads

                # Reduce maximum number of steps
                steps_max -= 1

                # Move to next sequence index
                seq_index = (seq_index + 1) if seq_index < 3 else 0

            # If reached max steps, assume an error occurred
            if steps_max < 0:
                # Set current positions to unknown
                self.flap_value_current = [None] * self.display_count
            
            # Determine remaining steps needed to reach final values
            steps_remaining = [self._calculate_steps(i) for i in range(self.display_count)]

            # Decrement max attempts
            max_attempts -= 1

        # Reset pins for next action
        self._bytes_out([0] * self.shift_register_count)
        
    def _calculate_steps(self, display_index):
        """
        Return the number of steps to rotate a display to reach the target and update current index

        display_index (int) - index of the display to calculate steps (0 based index)

        return (int) - integer indicating the following:
            0 = at target value already (no steps needed)
            -1 = go to home position - magnet is positive, move off magnet
            -2 = go to home position - magnet is negative, find first positive read
            >0 = number of steps to rotate display
        """
        # Go to home position if 1) current flap is not known or 2) target is past/on Home character
        if self.flap_value_current[display_index] is None or self.flap_value_target[display_index] < self.flap_value_current[display_index]:
            # Set current value to 0 - display will be at Home position
            self.flap_value_current[display_index] = 0

            # -1 if magnet is currently being sensed, -2 if not, find first positive read
            return -1 if self.pins_hall[display_index].value() == 0 else -2
        
        # Is desired target character already being displayed?
        if self.flap_value_current[display_index] == self.flap_value_target[display_index]:
            return 0
        
        # Calculate number of steps to reach Target
        steps = int(round(2048 * ((self.flap_value_target[display_index] - self.flap_value_current[display_index]) / self.flap_count ), 0))
    
        # Set current value to target - display will be at desired target after attempt
        self.flap_value_current[display_index] = self.flap_value_target[display_index]

        # Return steps
        return steps

    def _bytes_out(self, data):
        """
        Sends the desired bytes through the HC595 cycle

        data ([byte,...]) - data to send through shift registers, list of n bytes (n= number of shift registers)
        """
        # Loop bytes in reverse to send the right-digits=farthest shift register
        self.pin_latch.low()
        sleep_us(200)

        for i in range(self.shift_register_count, 0, -1):
            byte = data[i-1]
            for bit in range(8):
                self.pin_clock.low()
                sleep_us(200)
                value = 1 & (byte >> bit)
                self.pin_serial.value(value)
                sleep_us(200)

                self.pin_clock.high()
                sleep_us(200)

        self.pin_latch.high()
        sleep_us(200)
