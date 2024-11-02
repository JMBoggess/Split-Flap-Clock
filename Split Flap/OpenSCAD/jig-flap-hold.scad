outer_radius = 18.5;
seat_radius = 17.5;

module hold_circle(height) {
    linear_extrude(height) {
        difference() {
            circle(r=outer_radius, $fn=14);
            
            circle(r=outer_radius-2, $fn=14);
        }
    }
}

module flap_seats(height) {
    for(i=[0:360/14:359]) {
        
        x = (outer_radius-1.25)*cos(i);
        y = (outer_radius-1.25)*sin(i);
        translate([x, y, height / 2])
            rotate([0,0,i])
                cube([2.5,1,height+0.1], center=true);
    };
}

module flap_hold() {
    difference() {
        hold_circle(14);
        translate([0,0,3])
            flap_seats(11);
    }
}

flap_hold();
