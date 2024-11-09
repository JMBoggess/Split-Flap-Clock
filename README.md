# Split-Flap-Clock
Clock using a split-flap display

# Background
In December 2023, I bought my first microcontroller. I first began working on a similar project using a split-flap display to show number of instagram followers which I began in February 2024. I began this project in November 2024 seeking to build on what I learned through the previous project. The goal of this project is to create a split-flap display clock with a self-setting time feature. I will be using a Raspberry Pi Pico W microcontroller and 3D printed split-flap displays.

# Components

## 14-Flap Split-Flap Display
The split-flap displays were designed primarily from [Scott Bezek's work](https://github.com/scottbez1/splitflap). My primary alteration is a 14-flap version since I am primarily interested in displaying numbers. I found 14 flaps was a good compromise in reducing the overall dimensions while leaving enough room for certain components (e.g. magnet in the spool section for the Hall sensor). The overall dimensions of each display is:
- Width: 90mm
- Height: 133mm
- Depth: 60mm

## Split-Flap Electronics
- Shift-bit Register (2) - used with the four digit displays
- 28BYJ-48 Stepper Motors (5)
- Driver Boards (5)
- Hall Monitors (5)

## LED
Used to indicate program status
- 1 LED
- 220 Ohm resistor

## Buttons
Allows user to interact with the clock
- 2 buttons
  - Control Configuration mode
  - Manually run NTP Time Update mode

## Slide Switch
Used as an on/off switch

# Source Code

## Events

| Event | Description |
| --- | --- |
| Startup | When the clock is turned on, program execution begins. If enabled in configuration, NTP Time Update mode is executed. Display Update mode is then executed. |
| Config Button Click | A short button press places the clock in Configuration mode. A long button press exits configuration mode. Configuration mode can also be exited in the website |
| Set Date Time Click | A short button press manually starts the Set Date Time mode. A long button press cancels this mode. |
| Set Date Time Timer | Every hour, the clock automatically starts the Set Date Time mode. |

## Modes

### Configuration Mode
The clock is set as an Access Point (AP) allowing users to connect using wi-fi. The user connects with a web browser allowing them to perform the following actions:
- Setup wi-fi connection allowing the clock to connect to their home wi-fi for internet access to set the date and time
- Manually set the date and time of the clock
- View log files for troubleshooting issues
- Exit configuration mode

### Set Date Time Mode
If configured, the clock connects to the internet and updates the date and time using the [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol) (NTP). The clock then runs the Display Update mode.
- This mode will automatically run every hour.
- Users can also click a button to run this mode at any time.

### Display Update Mode
The clock updates the split-flap displays to show the date and time. This mode executes:
- Automatically every minute
- After manually setting the date and time in Configuration mode
- The last step of the Set Date Time mode

## LED Indicator

| Light | Description |
| --- | --- |
| Solid On | The clock is in Set Date Time mode |
| Steady Blinking | The clock is in Configuration mode |
| Four-Pulse Rapid Blinking | An error occurred, view the log for details. The light blinks rapidly four times with a pause and then repeats several times before shutting off |

## Note about Chat GPT
I did not use Chat GPT or any other generative AI (GenAI) to produce any of the code. While I am not opposed to the use of GenAI as a programer, I believe it should be used as a supplemental reference and not in place of learning how to program.

# Notes
- TODO: Determine how to make the program start on power-up
