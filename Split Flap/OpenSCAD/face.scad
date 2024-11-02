module face_2d() {
    difference() {
        // Main shape
        square([69,30]);
        
        // Screw holes
        translate([18.75, 4])
            circle(r=2, $fn=15);
        
        translate([50.25, 4])
            circle(r=2, $fn=15);
    }
}

module face() {
    linear_extrude(3) {
        face_2d();
    }
}

face();