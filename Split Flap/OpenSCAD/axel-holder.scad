// Used a 16mm long screw

module squares() {
    square(9.4, center=true);
    translate([4.625, 4.625])
        square(4.15, center=true);
    translate([4.625, -4.625])
        square(4.15, center=true);
    translate([-4.625, 4.625])
        square(4.15, center=true);
    translate([-4.625, -4.625])
        square(4.15, center=true);
}

module squares_cut() {
    // Subtract out triangles for holes
    difference() {
        squares();
        
        translate([6.7, 6.7])
            rotate([0,0,45])
                square(5.87, center=true);
        translate([6.7, -6.7])
            rotate([0,0,45])
                square(5.87, center=true);
        translate([-6.7, 6.7])
            rotate([0,0,45])
                square(5.87, center=true);
        translate([-6.7, -6.7])
            rotate([0,0,45])
                square(5.87, center=true);
    }
}

module axel_holder_2d() {
    difference() {
        squares_cut();
        circle(r=2, $fn=15);
    }
}

module axel_holder() {
    linear_extrude(3.2) {
        axel_holder_2d();
    }
}

axel_holder();