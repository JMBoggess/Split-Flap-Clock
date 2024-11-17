# Split-Flap Display Test
After assemblying a split-flap display, use the test_display python file to test the display and take readings which can be used in program configuration.

## Script Configuration

### Flap Values
The script assumes a 14-flap design. Ensure the proper flap values are set (__init__ function of the Digit class):

```python
# Array of flaps - first value (index: 0) should be the Home character
# Version 1: digits
# self.flap_values = ['0','1','2','3','4','5','6','7','8','9',',',':','!',' ']
# Version 2: day-of-week (0=Sun) and meridem
self.flap_values = ['0-AM','0-PM','1-AM','1-PM','2-AM','2-PM','3-AM','3-PM','4-AM','4-PM','5-AM','5-PM','6-AM','6-PM']
```

### Home Reads
Home Reads are the number of positive magnet reads by the Hall Sensor to set as the home or zero-index position of the display. Use the hall_readings method (described below) to assist with setting this value. This value should be consistent for all displays in the final clock and the Digit class in the clock's code should be updated.

```python
self.home_reads = 90
```

### Pin Configuration
After the Digit class code and all testing methods, ensure the correct GPIO pin numbers are set to create the digit object.

```python
digit = Digit([2,3,4,5], 0)
```

## Tests
The script contains tests at the bottom of the script. Comment/uncomment sections as appropriate to execute a test.

### One Full Rotation
This test slows rotates the display one full revolution. Use cases:
- Ensure the display can rotate freely
- Ensure flaps do not stick
  - If the spools are too tight, flaps may not fall freely when rotating
  - Carefully spread the spools apart slightly to correct

```python
hall_reading(digit, 1, 4)
```

### Hall Readings
The display rotates 10 times (alter as needed) display the number of positive (and negative) magnet reads after each rotation.
- Look for consistency in the number of positive reads
- Home position should be somewhere within these positive reads
- Current home position value is 90 - this is sufficient to move past the first magnet read but does not advance past the first card
- At this step, just establish a range of positive magnet reads to work with
- Continue to watch that cards fall as desired and make note of any cards for a late test (see Display Characters)

```python
hall_reading(digit, 10)
```

### Configure Home
The display is advanced to the first magnet read and then advanced slowly printing each step. Use this to help determine the Home position, modify the configuraiton value for home reads as appropriate. Then uncomment and use the go_home function to test any modified values.

```python
configure_home(digit)
# digit.go_home()   # Set the Home Reads variable and test setting
```

### Display Characters
Use this section to display specific digits/characters.
- Go to any cards that are sticking to make adjustments as needed
- Test responsiveness of going to a character, pausing, and then displaying other characters

```python
# digit.display_character('1-AM')   # Display a single character
# Modify the following show list as desired to move between characters
# show = ['3','7',' ','2','0','6']
show = ['2-PM','6-AM','0-PM']
for d in show:
   digit.display_character(d)
   time.sleep(1)
```

