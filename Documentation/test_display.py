# Use this script to test a split-flap display
from machine import Pin
import time

# Class controlling stepper motor
class Digit:
    """
    Control a single split-flap digit. (14-flap version)

    Pin Configuration:
        Stepper Motor (28BYJ-48) connects to Driver Board
        Driver Board (ULN2003)
            GND (-) > Ground pin (any)
            VCC (+) > SysBus (5v) - assumes pico is powered by USB
            IN1-4 > Any 4 GPIO pins
        Hall sensor (A3144)
            GND (-) > Ground pin
            VCC (+) > SysBus (5v)
            IN > Any GPIO - use Pin.PULL_UP

    """

    def __init__(self, pins_motor, pin_hall):
        """
        Instantiate a digit object

        pins_motor (int list) - list of GPIO pins the motor is connected to in order

        pin_hall (int) - the GPIO pin the Hall effect sensor is connected to
        """
        # Set Pins
        self.pin_hall = Pin(pin_hall, Pin.IN, Pin.PULL_UP)
        self.pins_motor = [Pin(pins_motor[i], Pin.OUT) for i in range(4)]
        
        # Constants
            
        # Array of flaps - first value (index: 0) should be the Home character
        # Version 1: digits
        # self.flap_values = ['0','1','2','3','4','5','6','7','8','9',',',':','!',' ']
        # Version 2: day-of-week (0=Sun) and meridem
        self.flap_values = ['0-AM','0-PM','1-AM','1-PM','2-AM','2-PM','3-AM','3-PM','4-AM','4-PM','5-AM','5-PM','6-AM','6-PM']

        # Flap Value Current - the current index of the character displayed (If unknown or not set: None)
        self.flap_value_current = None

        # Flap Count - (Added to reduce redundant code: len function calls)
        self.flap_count = len(self.flap_values)

        # Seq - Motor step sequence (order to set motor pins to rotate motor)
        self.seq = [9,12,6,3]           # Use when step counter is incrementing
        
        # Home Reads - Number of positive magnet reads to set as home position
        self.home_reads = 90

    ########## Public Methods ##########
        
    def display_character(self, char):
        """
        Rotates the display to the desired character

        char (str) - The character to display (case sensitive), throws an error if character is not valid (not in Flap Values)
        """
        # Ensure character is valid
        if char not in self.flap_values:
            raise IndexError('char not found in Flap Values list')
        
        # Get the desired flap index
        target_index = self.flap_values.index(char)
        
        # If current flap is not known/set, go to and use Home position
        if self.flap_value_current is None:
            self.go_home()
            self.flap_value_current = 0

        # End function if desired character is already being displayed
        if self.flap_value_current == target_index:
            return
        
        # Is the target past/on Home character
        if target_index < self.flap_value_current:
            # Yes, first go home (ensures better calibration)
            self.go_home()
            self.flap_value_current = 0
        
        # Based on above: 1) Target index is greater than Current index and 2) Target Index <> Current Index
        
        # Calculate number of steps to reach Target index
        steps = round(2048 * ((target_index - self.flap_value_current) / self.flap_count ), 0)
        
        # Advance number of steps
        for i in range(steps):
            self.step(self.seq[i % 4])

        # Reset pins for next action
        self.pin_reset()

        # Set Current Flap Value to what is now displayed
        self.flap_value_current = target_index

    ########## Internal Methods ##########
    
    def go_home(self):
        """
        Turn until home position is obtained. Turns at most, 1 full revolution
        """
        # If the magnet is currently being sensed, advance until not being read
        i = 0 # Used to ensure we don't exceed 1 revolution
        while self.pin_hall.value() == 0 and i < 2048:
            self.step(self.seq[i % 4])
            i += 1  # Advance counter

        # Find first positive magnet read
        i = 0
        while self.pin_hall.value() == 1 and i < 2048:
            self.step(self.seq[i % 4])
            i += 1  # Advance counter
        
        # Advance to Home based on desired magnet reads
        for i in range(self.home_reads):
            self.step(self.seq[i % 4])
        
        # Reset pins for next action
        self.pin_reset()

    # One motor step (also used by configure file)
    def step(self, seq):
        """
        One motor step - created to reduce code redundancy

        seq (int) - the step in the sequence to execute
        """
        # Set pins
        for i in range(4):
            b = 1 << i  # Bit-shift logic for value to send
            self.pins_motor[i].value(1 if (seq & b) > 0 else 0)   # Set each pin
        
        time.sleep_ms(2)    # Pause between motor steps
    
    # Motor pin reset (also used by configure file)
    def pin_reset(self):
        """
        Reset motor step pins for next action
        """
        for i in range(4):
            self.pins_motor[i].value(0)


def hall_reading(digit, revolutions=1, speed=2):
    """
    Take Hall reaadings at every step and output results

    digit (Digit01) - digit class object

    revolutions (int, default: 1) - number of revolutions; each revolution includes 1 set of readings

    speed (int, default: 2) - speed in ms (milliseconds) between steps (min 2)
    """
    print('---------- Hall Readings ----------')
    for rev in range(revolutions):

        # Hall sensor value: 1 = False (magnet not found; high voltage); 0 = True (presence of magnet; low voltage)
        hall_false = 0
        hall_true = 0

        # Make one complete revolution
        for i in range(2048):
            s = digit.seq[i % 4]    # Step in sequence
            
            for j in range(4):
                b = 1 << j  # Bit-shift logic for value to send
                digit.pins_motor[j].value(1 if (s & b) > 0 else 0)   # Set each pin
            
            # Read hall sensor and record
            if digit.pin_hall.value() == 0:
                hall_true += 1
            else:
                hall_false += 1

            time.sleep_ms(speed)    # Pause between motor steps
        
        # Reset pins for next action
        for i in range(4):
            digit.pins_motor[i].value(0)
    
        # Output hall sensor values (debugging)
        print(f"Reading: {rev}; True: {hall_true}; False: {hall_false}")

def configure_home(digit):
    """
    Use to determine home step. Locates first magnet reading, then steps slowly printing each step.

    Record at what step the card turns, modify Home Reads variable to some point prior to this
    """

    # If the magnet is currently being sensed, advance until not being read
    i = 0 # Used to ensure we don't exceed 1 revolution
    while digit.pin_hall.value() == 0 and i < 2048:
        digit.step(digit.seq[i % 4])
        i += 1  # Advance counter
    
    # Find first positive magnet read (up to 1 complete revolution)
    i = 0
    while digit.pin_hall.value() == 1 and i < 2048:
        digit.step(digit.seq[i % 4])
        i += 1  # Advance counter
    
    # Step slowly printing each step to determine when flap falls (stop when magnet read not found)
    i = 0
    while digit.pin_hall.value() == 0 and i < 2048:
        digit.step(digit.seq[i % 4])
        i += 1  # Advance counter
        print(f"Step {i}")  # Print the step
        time.sleep_ms(300)  # Delay to give time to watch for flap fall

    digit.pin_reset()   # Reset pins for next action

# Create the Digit object
digit = Digit([2,3,4,5], 0)

########## Tests

# One-full rotation - rotate once moderately to ensure no physical issues
# hall_reading(digit, 1, 4)

# Hall Readings - rotates 10 times taking readings to indicate number of positive magnet reads (check consistency)
# hall_reading(digit, 10)

# Configure Home - find how many steps past first magnet read should be considered "home"
# configure_home(digit)
# digit.go_home()   # Set the Home Reads variable and test setting

# Display Characters
# digit.display_character('1-AM')   # Display a single character
# Modify the following show list as desired to move between characters
# show = ['3','7',' ','2','0','6']
# show = ['2-PM','6-AM','0-PM']
# for d in show:
#    digit.display_character(d)
#    time.sleep(1)
