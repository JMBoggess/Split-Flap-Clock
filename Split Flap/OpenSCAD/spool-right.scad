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

module spool_box_insert() {
    for(i=[0:90:359]) {
        translate([5.7*cos(i),5.7*sin(i)])
            rotate([0,0,i])
                square([2.1, 5.3], center=true);
    }
}

module screw_box() {
    difference() {
        square([9,7.1], center=true);
        
        circle(r=2,$fn=15);
    }
}

module spool_right_2d() {
    difference() {
        // Main circle
        circle(r=outer_radius, $fn=60);
        
        // Flap holes
        flap_holes();
        
        // Nut insert - axel
        for(i=[0:120:359]) {
            rotate([0,0,i])
                square([4.1,7.1],center = true);
        }
        
        // Spool Box Inserts
        spool_box_insert();
        
        // Home indicator magnet hole
        translate([0, -12.5])
            circle(r=1.6, $fn=15);
        
    }
}

module spool_right() {
    linear_extrude(3) {
        spool_right_2d();
    }
    
    linear_extrude(1.2) {
        screw_box();
    }
}

spool_right();

//use<axel-holder.scad>
//translate([0,0,3])
//    color("LightBlue", 1.0)
//        axel_holder();
