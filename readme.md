#Ft polishing estimator

This program accompanies the paper "PAPER NAME HERE".

The model in this program allows for Ft calculation through random parent isotope distribution within a convex crystal.
The random parent isotope sources each have a 'shell' of alpha particles modelled of which the fraction that are outside
the crystal is calculated. This 'local Ft' for each parent isotope is summed over the whole crystal to the z cut-off
to give total Ft. The summation of local Ft works in this instance as it is calculated for all sources, not just those
within the 'polished' crystal.

## Stabilisation graph - how many sources to use

As the number of sources increases the time taken by the program increases. However, a sufficient number of sources are
required to ensure accuracy of the result. One way to ensure a sufficient number is used is to check that increasing
said number doesn't change the Ft value measured within a specified precision. Here for a tetragonal prism with
pyramidal terminations of height 200 and width and depth 100 a graph is plotted to show the difference in totalFt value
calculated when different numbers of sources are used.



In the paper which this program accompanies, a value of 100000
was used, while for very low values of z_cut_off this doesn't reach great reliability, the time taken for the program
to run and the reliability of Ft for values of z_cut_off of 50% and above meant that this was viewed as sufficient for
requirements.