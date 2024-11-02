module nut_hole() {
    // Shape for inserting the screw
    translate([-2, 0])
        square([4,3]);
    
    // Shape for the nut
    translate([-3.55,3])
        square([7.2,3.1]);
    
    // Space for screw past nut
    translate([-2, 6.1])
        square([4, 3]);
}

module squares() {
    // Main squares for base
    translate([0, 3])
        square([42,63]);
    
    // Tabs left
    translate([5,0])
        square([10,3]);
    translate([28,0])
        square([10,3]);
    
    // Tabs right
    translate([5,66])
        square([10,3]);
    translate([28,66])
        square([10,3]);
    
    // Wood mount squares
    translate([-10,3])
        square([10,10]);
    
    translate([-10,56])
        square([10,10]);
}

module base_2d() {
    
    difference() {
        // Primary Shape
        squares();
        
        // Screw/Nut hole left
        translate([21,3])
            nut_hole();
        
        // Screwn/Nut hole right
        translate([21,66])
            rotate([0,0,180]) {
                nut_hole();
            };
        
        // Wood mount screw holes
        translate([-6, 8])
            circle(r=2, $fn=15);
        translate([-6, 61])
            circle(r=2, $fn=15);
    }
}

module base() {
    linear_extrude(3) {
        base_2d();
    };
}

base();
//nut_hole();