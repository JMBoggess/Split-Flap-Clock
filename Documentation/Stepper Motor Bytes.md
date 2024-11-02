# Stepper Motor Bytes
Turning a stepper motor effectively involves setting the polarity of two magnets. This is done by turning on or off four poles. There is a sequence of four steps in changing these polarities which results in turning the motor. These four on/off settings can be expressed in binary as follows.

| 8 | 4 | 2 | 1 | Integer | Step |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 3 | 1 |
| 0 | 1 | 1 | 0 | 6 | 2 |
| 1 | 1 | 0 | 0 | 12 | 3 |
| 1 | 0 | 0 | 1 | 9 | 4 |

For the split-flap display, the motor needs to be run in reverse sequence: `9 > 12 > 6 > 3`. 74HC595 Shift Registers are used to control two split-flap displays. The Shift Regsiters are daisy chained to reduce the number of GPIO pins used on the Raspberry Pi Pico W. These Shift Registers output 8-bit information. With each step, both split-flap displays may or may not need to be moved forward. To determine the byte (8-bit) to send to each Shift Register, the following table was used to derive sequence numbers. A display which does not need to move is denoted with a zero in the Step column.

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 | Integer | Display 1 Step | Display 2 Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 153 | 4 | 4 |
| 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 204 | 3 | 3 |
| 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 102 | 2 | 2 |
| 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 51 | 1 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 144 | 4 | 0 |
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 192 | 3 | 0 |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 96 | 2 | 0 |
| 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 48 | 1 | 0 |
| 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 9 | 0 | 4 |
| 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 12 | 0 | 3 |
| 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 6 | 0 | 2 |
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 3 | 0 | 1 |
