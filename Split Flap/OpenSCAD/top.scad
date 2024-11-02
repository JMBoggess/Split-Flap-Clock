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
    // Main squares
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
}

module top_2d() {
    
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
    }
}

module wood_mount_2d() {
    // screw hole mount for wood (one side)
    difference() {
        square([10,10]);
        
        translate([5, 6])
            circle(r=2, $fn=15);
    }
}

module top() {
    linear_extrude(3) {
        top_2d();
    };
    
    translate([40, 13.75, 3])
        rotate([90,0,90])
            linear_extrude(2)
                wood_mount_2d();
    
    translate([40, 45.25, 3])
        rotate([90,0,90])
            linear_extrude(2)
                wood_mount_2d();
}

top();
//nut_hole();