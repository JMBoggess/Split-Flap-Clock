# Display Assembly
The following provides information on how to assemble a split-flap display.

## Parts

### 3D Printed Parts
- Left side
- Right side
- Split-flap cards (see below for parts list)
- Spool-box (4 long rectangles)
- Axel-holder
- Left and Right Spools
- Top
- Bottom/Base
- Face (for testing purposes)
- Jigs
  - Split - for cutting cards in half
  - Hole - for punching out holes on side of cards
  - Hold - for holding cards in place during assembly
![3D Printed Parts](/Media/assembly_3d_parts.jpg)

### Split-flap cards
- [CR80 30 mil PVC cards](https://a.co/d/4AWDuIj) (commonly used for badges)
- [Card Slot Hole Punch](https://a.co/d/3zdMEoE)
- X-acto knive
- Permenant marker
- Stencils
  - [3-inch letters and numbers](https://a.co/d/gLgWajX) (used for digit display)
  - [1/2 and 3/4 inch letters](https://a.co/d/g1cRKLc) (used for AM/PM and days of week)
- Rubbing alchohol
- Masking tape or painters tape
- 3D printed Jigs (as listed above)
  - Split - for cutting cards in half
  - Hole - for punching holes or slots in side of card
![Split-Flap Card Parts](/Media/assembly_flap_parts.jpg)

### Hardware
- Hex Drive Button Socket Cap Screws
  - [M4 x 10mm](https://a.co/d/h3HqGNw) (qty: 6)
  - [M4 x 16mm](https://a.co/d/axGSh9M) (qty: 1)
- Phillips Head Machine Screws
  - [M2 x 6mm](https://a.co/d/1rp4N2g) (qty: 2)
- [M4 Nuts](https://a.co/d/0MgO0n8) (qty: 8)
- [M2 Nuts](https://a.co/d/1rp4N2g) (qty: 2)

### Electronics
- [Hall Effect Sensor](https://a.co/d/9E8ezPd) (3144E A3144)
- [3mm Magnet](https://a.co/d/gIFRxZn)
- [ULN2003 Driver Board](https://a.co/d/5FAjnlJ)
- [28BYJ-48 Stepper Motor](https://a.co/d/5FAjnlJ)
- [Wire](https://a.co/d/huoj8Pj)
![Electronic Parts](/Media/assembly_electronics.jpg)

### Tools and Other
- Files
  - Used to file 3D printed parts as needed
- Allen wrench
- Small phillips screw driver

## Split-Flap Cards
- Place a card under the "Split" jig so that the lip of the jig is on the outside of the card
  - The jig falls at the middle of the card
- Use an x-acto knife to score a line down the middle of the card at the jig
- Bend the card back and forth until it breaks along the score line
  - I also found it useful to bend the card, turn it over, and score the opposite side of the card along the bend line
- On either side of the card, use the "Hole" jig to position the Card Slot Hole Punch and punch a slot/hole on either side
  - This will form the small spoke-like sections which can be inserted into the spool holes
  - Use an x-acto knife to clean up the holes as needed
- (Optional) Use rubbing alchohol to clean both sides of the card from any dirt and oils from handling the cards
- Place the desired stencil on the card and fill-in using a permenant marker
  - For digits, the number spans two cut cards (i.e. one full uncut card length)
  - I used painters tape to hold the cards and stencil in place

## Spool Box Assembly

### Install Magnet
Prior to inserting the magnet into the spool (right-side), you must first determine which pole of the magnet is read by the Hall Sensor. For the Hall Sensors I purchased, the sensor head was bent the opposite direction from where it needed to be in the final assembly. As a result, I had to first bend the sensor head away from the pins (where the cables attach). Connect the Hall Sensor to the Pico W and run a script to continuously read. Hold the magnet near the sensor and determine which side results in a positive read (reverse the magnet as needed). Use a marker to place a dot on the side that needs to be read from to ensure proper assembly into the spool.

Pin configuration:
- Minus (-) - ground
- Plus (+) - SysBus (5v) assuming powered by USB
- Serial In (S) - any GPIO port (use Pin.PULL_UP)

Example script:
```python
from machine import Pin
from time import sleep

p = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    try:
        print(p.value())
        sleep(1)
    except KeyboardInterrupt:
        break
```

Once the correct side is determined, place the magnet in the spool hole with the side you marked facing out. The indent for the nut is the outside of the spool and the same side the hall sensor will be reading the magnet. In some cases, I found I had to use some CA glue to keep the magnet in the spool hole. The below image shows the correct side facing out/up which will be read by the hall sensor.
![Spool with magnet](/Media/assembly_spool_magnet.jpg)

### Spool Lineup
Identify where the holes lineup between the left and right spool. In the below image, on the left, the slots lineup but the holes do not. In the right image, both the slots and holes line up. Place a mark on the spools to identify holes that align. I placed a dot on the holes opposite the magnet as these are the holes for split-flap card zero - the first split-flap card index to be displayed.
![Spool Hole Lineup](/Media/assembly_spool_lineup.jpg)

### Axel-Holder
Using an M4 x 16mm screw and nut, attach the axel-holder to the right-spool. The head of the screw will be on the inside (side opposite the inset space for the hex net). Leave the assembly loose to rotate the axel-holder into final position. The screw will be tightened after installing the flaps and spool box components.
![Axel Holder](/Media/assembly_axel_holder.jpg)

### Spool Box
Attach all four supports for the spool box to the left spool (non-magnet spool). Push these flush with the outside/bottom of the spool. Push the four supports onto the axel-holder and slightly into the right spool. I loosened the axel-holder screw significantly to push the axel holder as far down into the box as possible. The more space provided to install the flaps the better while simultaneously starting to insert the four supports is optimal. The most difficult part of this assembly is lining up the flaps with the holes while simultaneously pushing the spools onto the spool box supports.

The "spool box" is four support pieces. I am referring to this as the spool box as the original design this is drawn from the four components form an actual box to which the spools sit on either end. In reducing the size of the display, I found it necessary to not make these components meet into a true box. For lack of better term, I am still referring to this as the "spool box".
![Spool Box](/Media/assembly_spool_box.jpg)

### Flap-Spool Assembly
This is the most difficult part of assembly. Place one of the Hold jigs on a work surface. Place the left spool (non-magnet spool) inside the jig. Place the flaps into the left-spool holes using the jig to support the flaps and help keep them aligned. Be sure to start with the desired flap (flap 0) in the holes located opposite the magnet (marked previously during spool lineup). The spool will rotate counter-clockwise from the current viewing position. Flaps should be placed in sequence so they will display in order as the spool turns this direction.
![Flap Lower](/Media/assembly_flap_lower.jpg)

Once the flaps are inserted securly in the left-spool (on bottom), place another Hold jig on the top to help line up the flaps with the right-spool (on top). Ensure the flaps are in each hole otherwise they will bend when pressing the spools together.
![Flap Full](/Media/assembly_flap_full.jpg)

Press the right-spool (on top) down to lock the flaps and spool box in place. I worked this in quarter sections, lining up flaps on one side and pressing that side together, turning, and repeating the process back and forth until the spool locked down into place. In the below photo, notice the flap ends are visible through the holes indicating they are in place and not bent inside the spool assembly. You can carefully turn over the assembly with the jigs in place to inspect both ends as needed.
![Flap Close Up](/Media/assembly_flap_closeup.jpg)

Once all flaps are in place and the spools are pressed down so the spool box support pieces are flush, remove the jigs. Ensure the spool box suppor pieces are not extending beyond the spool (i.e. overtighten) otherwise the flaps will not rotate freely. Use the hex wrench to then tighten the axel-holder screw (insert the hex wrench through the hole of the opposite spool).
![Flap Final](/Media/assembly_flap_final.jpg)

## Outer Box Assembly

### Hall Sensor
Install the Hall Sensor on the right side piece using M2 x 6mm screws and nuts. The back of the Hall Sensor board faces the outside of the finished assembled box. Note the slot in the right side piece for the flap-stop screw, this is at the bottom of the finished box. The Hall Sensor should be bent around the plastic so that it will be near the magnet when the spool assembly is added. The below depicts the installed hall sensor on the inside (left image) and outside (right image).
![Hall Sensor](/Media/assembly_hall_sensor.jpg)




