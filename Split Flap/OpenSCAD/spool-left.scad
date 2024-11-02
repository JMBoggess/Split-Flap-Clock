flap_hole_count = 14;
flap_hole_radius = 1.25;
inner_radius = 9;
outer_radius = 15.5;

module flap_holes() {
    for(i=[0:360/flap_hole_count:359]) {
        translate([inner_radius*cos(i), inner_radius*sin(i)])
            circle(r=flap_hole_radius, $fn=15);
    };
}

// Shape for stepper motor insert
module motor_insert() {
    difference() {
        // Increased radius .1 for fit
        circle(r = 2.6, $fn=15);
        translate([4,0])
            square(5, center = true);
        translate([-4,0])
            square(5, center = true);
    }
}

module spool_box_insert() {
    for(i=[0:90:359]) {
        translate([5.7*cos(i),5.7*sin(i)])
            rotate([0,0,i])
                square([2.1, 5.2], center=true);
    }
}

module spool_left_2d() {
    difference() {
        // Main circle
        circle(r=outer_radius, $fn=60);
        
        // Flap Holes
        flap_holes();
        
        // Motor insert hole
        motor_insert();
        
        // Spool Box inserts
        spool_box_insert();
    }
}

module spool_left() {
    linear_extrude(3) {
        spool_left_2d();
    }
}

spool_left();