# Split-Flap Displays
The split-flap displays were designed primarily from [Scott Bezek's work](https://github.com/scottbez1/splitflap).

## Overall Dimensions
A single display has the following dimensions:
- Width: 90mm
  - 3D Printed Box: 69mm
- Height: 133mm
- Depth: 60mm
  - An additional 5-15mm is needed for wire management

## 14 Flaps
The original display by Scott Bezek contains 40 flaps. I chose to reduce this as I am primarily interested in display digits. Reducing the number of flaps reduces the dimensions of various parts. In order to retain enough space for some components (such as the magnet used by the Hall sensor), I found I needed a minimum of 14 flaps.

The 14 Flaps for the primary clock display include:
- Digits 0-9
- Comma `,`
- Semicolon `:`
- Exclamation Mark `!`
- Blank

A single 14-flap display is also used for day-of-week and time-of-day, including:
- Sun - Sat displayed on the top
- AM or PM displayed on the bottom

## 3D Printed Components

### Dimensions
Unless otherwise specified, all components were made to be 3mm thick.

- Top: 42mm x 69mm
  - Includes insert tabs (3mm on either side): 69mm - 6mm = 63mm
  - Includes two vertical screw-hole tabs for attaching to a face plate
    - These are both 10mm x 10mm
    - Component overall height is 13mm (3mm thickness + 10mm tabs)
- Base: 52mm x 69mm
  - Includes insert tabs (3mm on either side): 69mm - 6mm = 63mm
  - Includes two screw-hole tabs for attaching to a base
    - Both are 10mm x 10mm
    - 52mm - 10mm = 42mm
- Left Side: 42mm x 126mm
  - Motor hole center:
    - 9mm from edge
    - 63mm from bottom
- Right Side: 42mm x 126mm
  - Hole for spindle (opposite motor) same as Left Side (9mm from edge; 63mm from bottom)
  - Bottom flap restraint: begins 12mm from bottom, 4mm from either side
- Spool Left: 31mm diameter
  - Flap holes center: 9mm from center (2.5mm diameter)
- Spool Right: 31mm diameter
  - Flap holes center: 9mm from center (2.5mm diameter)
  - Magnet hole for Hall sensor: 12.5mm from center (3.2mm diameter)
    - Flap "0" should be located directly across from this hole
- Spool Box: 4 parts - 5mm x 55mm each
  - 2mm thick
  - Used for stability and assembly
- Axel Holder: 7mm x 7mm
  - 3.2mm thick
  - Used on right-side to hold axel screw (opposite motor)
- Face: 69mm x 30mm
  - This piece was used for testing, final wood box will act as face
  - Distance between holes: 31.5mm

In addition to the above components, I 3D printed a series of jigs
- Jig Flap Split: 60mm x 46mm
  - Used to score/cut cards in half to make flaps
  - 1mm thick lip 3mm wide to create a ledge against which the cards are placed
  - Results in flaps 43mm heigh (46mm - 3mm ledge)
- Jig Flap Hole: 40mm x 29mm
  - L-shaped jig, placed on the edge of a flap against which the hole punch is placed to cut the slot in the flap
- Jig Flap Hold: 37mm diameter
  - Used to hold flap cards in place while assemblying the spool
  - 33mm internal diameter

### Development
- I used OpenSCAD v2021.01 for 3D modeling
- STL files were then exported from OpenSCAD
- Creality Slicer v4.8.2 was used to encode the STL file to GCODE for the 3D printer
  - Some components were combined for printing into a single GCODE file
  - To create files:
    - Open STL file(s)
    - If desired, duplicate components (right-click)
    - Click Slice button
    - Red areas indicate problems (where model needs support)
    - Save the file as a GCODE file
    - Copy to sd card to load to Ender printer

### Card Layout
The following table depicts the card layout for the digits and day-of-week (DOW) and time-of-day (TOD) display.
- Flap - The visible flap displayed to the user (consists of different cards making up the Top and Bottom of the display)

| Flap | Position | Card | Digits | DOW/TOD |
| --- | --- | --- | --- | --- |
| 1 | Top | 1 | 0 | SUN |
| 1 | Bottom | 14 | 0 | AM |
| 2 | Top | 2 | 1 | SUN |
| 2 | Bottom | 1 | 1 | PM |
| 3 | Top | 3 | 2 | MON |
| 3 | Bottom | 2 | 2 | AM |
| 4 | Top | 4 | 3 | MON |
| 4 | Bottom | 3 | 3 | PM |
| 5 | Top | 5 | 4 | TUE |
| 5 | Bottom | 4 | 4 | AM |
| 6 | Top | 6 | 5 | TUE |
| 6 | Bottom | 5 | 5 | PM |
| 7 | Top | 7 | 6 | WED |
| 7 | Bottom | 6 | 6 | AM |
| 8 | Top | 8 | 7 | WED |
| 8 | Bottom | 7 | 7 | PM |
| 9 | Top | 9 | 8 | THU |
| 9 | Bottom | 8 | 8 | AM |
| 10 | Top | 10 | 9 | THU |
| 10 | Bottom | 9 | 9 | PM |
| 11 | Top | 11 |  | FRI |
| 11 | Bottom | 10 | , | AM |
| 12 | Top | 12 | : | FRI |
| 12 | Bottom | 11 | : | PM |
| 13 | Top | 13 | ! | SAT |
| 13 | Bottom | 12 | ! | AM |
| 14 | Top | 14 |  | SAT |
| 14 | Bottom | 13 |  | PM |

