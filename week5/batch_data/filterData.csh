#!/bin/csh -f


set input="squirrel4.dat"

# read options
while ($#argv>0)
  switch("$argv[1]")

  case -input
    set input="$argv[2]"
  shift argv;shift argv
  breaksw

  case -help
    echo " "
    echo "-input name;      input filename"
    echo " "
    exit

  default:
    echo "Unknown argument $argv[1]"
    echo "Who knows"
    echo "Type gediRatList.csh -help"
    exit;

  endsw
end

set output="$input:r.csv"


echo "x,y,time" > $output
sed -e s%\(%""%g -e s%\)%""%g < $input|gawk 'BEGIN{t=323}(NR>1){printf("%s,%s,%f\n",$2,$3,t);t+=rand()*100}' >> $output

echo "Written to $output"

