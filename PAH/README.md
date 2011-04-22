About
=====

This directory contains files necessary to set up the dust model for the 
Milky Way from Draine (2003) with the size distribution for the 
Milky-Way and for R_V=3.1 with C/H = b_C = 60 ppm in log-normal size 
dists, but renormalized by a factor 0.93 (now has C/H= 60*0.93 = 55.8 
ppm in log-normal size distributions).

Documentation
=============

The following two files will compute the Draine (2003) dust model for 
grains smaller and greater than 200A respectively:

    d03_3.1_6.0_A_lt200A.in
    d03_3.1_6.0_A_gt200A.in

To run, you will need the bhmie code installed, after which you can do:

    bhmie d03_3.1_6.0_A_lt200A.in
    bhmie d03_3.1_6.0_A_gt200A.in


