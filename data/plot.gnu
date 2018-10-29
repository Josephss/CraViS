#!/usr/bin/gnuplot --persist
set ylabel "Temperature [degree C]" offset 0.000000,0.000000  font ""
#set yrange [ -250 : 40 ] noreverse nowriteback
set lmargin -1
set bmargin -1
set rmargin -1
set tmargin -1
set size 1, 1
set key center center

set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%m/%d\n%H:%M"

set terminal png
set output 'cooling.png'
#set label "-185 degree C" at graph 0.5,0.5
plot "sensor01.csv" every ::0::3800 using 1:2 title "detector plate" with line,\
 "sensor02.csv" every ::0::3800 using 1:2 title "base plate" with line
set output # important! close output file

set output 'warming.png'
plot "sensor01.csv" every ::3000::20000 using 1:2 title "detector plate" with line,\
 "sensor02.csv" every ::3000::20000 using 1:2 title "base plate" with line
set output # important! close output file
