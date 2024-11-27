# Electronic Wiring

## Disclaimer: I am not an electrical engineer
Yes, it will be obvious as you look at the diagrams on this page... I know very little about electrical engineering. I spent some time digging into electrical diagraming and found out:
1. Learning to read and create these diagrams is a large undertaking.
2. Diagraming can be a very sensitive topic amoung electrical engineers.

Part of the purpose of this project was to be my first exposure to the world of electrical engineering. I have learned a great deal during this journey and gained a greater appreciation for what I do not know. Learning any topic involves moving through four stages:
1. Unconcious Ignorance - simply being unaware of the topic entirely
2. Concious Ignorance - becoming aware of the topic including the breadth and depth and your ignorance about the topic (I'm here)
3. Concious Knowledge - gaining knowledge about the topic, yet having to expend a great deal of mental effort to recall and use that knowledge
4. Unconcious Knowledge - where knowledge of the topic is "second nature"

Before beginning I knew I was in step 1 and my goal was to move to step 2. So please treat the below with a great deal of grace. I am excited about what I have been able to do in this project and that motivation will help me continue to pursue learning in the topic.

# Testing Diagram
The following is a functional diagram of how I connected the electronic components to test the overall functionality and code.
- I used Draw.io to create the diagram
- My goal was to make a diagram legible to the layperson (me) as a guide

![Wiring Diagram](/Media/Diagram.png)

## Observations

### Power
For testing purposes, the Pico W is connected to the computer through a USB cable. All Vcc components are indications of what is connected to the power rail (GND indicates the Ground Rail).
- I will need to determine how to properly power the final product
- HC595 shift registers can also be powered by 3.3V

### GPIO (General Purpose Input/Outuput)
All pins used on the Pico W are GPIO. I color-coded the pins to make it easier to identify what is plugged in and how many pins will be used on the Pico W.
- I used 8-bit shift registers daisy-chained together to reduce the number of pins used
- There are a total of 11 pins that will be used by the final product

## Shift Registers
There are a total of three 8-bit shift registers used. Each display requires four bits so two displays can be driven from one register. The last register has only one display so the remaining four bits are not used. Pin configuration involves:
| Pin(s) | Connection |
| --- | --- |
| QA, QB, QC, QD | One step-motor driver board |
| QE, QF, QG, QH | Another step-motor driver board |
| GND (Ground) | Ground rail |
| OE (output enabled) | Ground rail, i.e. register output is always enabled |
| VCC | SysBus 5 volts |
| SRCLR (shift register clear) | Sysbus 5 volts, i.e. register is immediately cleared each time |
| SRCLK "clock" (shift register clock) | GPIO pin - all shift registers use the same pin |
| RCLK "latch" (storage register clock) | GPIO pin - all shift registers use the same pin |
| SER (serial input) | First shift register is connected to GPIO pin, subsequent go from this pin to the GH' pin of the parent register |
| QH' | Used in daisy chain, last register will not use this pin, recieves the SER connection from a child register |

## Hall Effect Sensors
Each display uses a Hall Effect Sensor to read a magnet connected to the split-flap wheel indicating which flap is the "home" position. Each are connected to a separate GPIO pin on the Pico W. In code, Pin.PULL_UP is used to eliminate the need for a resistor.

