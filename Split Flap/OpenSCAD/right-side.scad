
module right_side_2d() {
    difference() {
        // Main shape
        square([42,126]);
        
        // Screw hole top
        translate([21, 126 - 4])
            circle(r=2, $fn=15);
        
        // Top inserts
        translate([4.9, 126 - 5.6])
            square([10.2, 3.1]);
        translate([27.9, 126 - 5.6])
            square([10.2, 3.1]);
        
        // Screw hole for spool
        //      9mm from edge
        translate([33,63])
            circle(r=2.1, $fn=15);
        
        // Home mount screws
        //  Center: x=18.5 from motor hole (12.5 to magnet + 6 to screw holes; spool hole x - 18.5)
        //      y=5 from center (10 apart)
        translate([14.5,63+5])
            circle(r=1.05,$fn=15);
        translate([14.5,63-5])
            circle(r=1.05,$fn=15);
        
        // Home mount insert
        //  1.5 from edge of home screws (2.5 from center)
        translate([0,63-10])
            square([12,20]);
        
        
        // Bottom flap restraint
        translate([4, 12])
            square([34, 4.1]);
        
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

module right_side() {
    linear_extrude(3) {
        right_side_2d();
    };
}

right_side();