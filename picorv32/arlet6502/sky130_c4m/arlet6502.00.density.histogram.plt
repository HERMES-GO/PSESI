set title "GCell Densities"
set grid
set grid noxtics
set xrange [-0.5:9.5]
set xtics ( "<10%%" 0 ,"<20%%" 1 ,"<30%%" 2 ,"<40%%" 3 ,"<50%%" 4 ,"<60%%" 5 ,"<70%%" 6 ,"<80%%" 7 ,"<90%%" 8 ,"<100%%" 9 )
set yrange [0:0.5]
set ytics ( "0%%" 0 ,"10%%" 0.1 ,"20%%" 0.2 ,"30%%" 0.3 ,"40%%" 0.4 )
set style histogram cluster gap 1
set style fill solid noborder
set boxwidth 1
plot "arlet6502.00.density.histogram.dat" using 1 title "Avg. Density" with histogram linecolor rgb "green", \
     "arlet6502.00.density.histogram.dat" using 2 title "Peak Density" with histogram linecolor rgb "red"
