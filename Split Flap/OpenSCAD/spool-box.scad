// Not enough room to make interlocking
//   Material Thickness = 2
//   Overall length = 55 

module spool_box_2d() {
    square([5,55]);    
}

module spool_box() {
    linear_extrude(2) {
        spool_box_2d();
    }
}

spool_box();
