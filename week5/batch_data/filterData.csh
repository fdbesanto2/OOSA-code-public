#!/bin/csh -f

set input="squirrel3.dat"
set output="squirrel3.csv"

echo "x,y,time" > $output
sed -e s%\(%""%g -e s%\)%""%g < $input|gawk 'BEGIN{t=323}(NR>1){printf("%s,%s,%f\n",$2,$3,t);t+=rand()*100}' >> $output

echo "Written to $output"

