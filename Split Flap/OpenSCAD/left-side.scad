module left_side_2d() {
    difference() {
        // Main shape
        square([42,126]);
        
        // Motor hole
        //   Center: x=9 from edge
        translate([33,63])
            circle(r=5, $fn=20);
        
        // Motor screw holes
        //  Center: x=17 from edge (8 from motor hole)
        //      y=17.5 from motor hole (35mm apart)
        translate([25,63+17.5])
            circle(r=2, $fn=15);
        translate([25,63-17.5])
            circle(r=2, $fn=15);
        
        // Screw hole top
        translate([21, 126 - 4])
            circle(r=2, $fn=15);
        
        // Top inserts
        translate([4.9, 126 - 5.6])
            square([10.2, 3.1]);
        translate([27.9, 126 - 5.6])
            square([10.2, 3.1]);
        
        // Screw hole bottom
        translate([21,4])
            circle(r=2, $fn=15);
        
        // Bottom inserts
        translate([4.9, 2.4])
            square([10.2, 3.1]);
        translate([27.9, 2.4])
            square([10.2, 3.1]);
    };
}

module left_side() {
    linear_extrude(3) {
        left_side_2d();
    };
}

// Used for testing
left_side();

