set terminal postscript eps enhanced mono size 3.02 , 2.40
set output "M_I.eps"
set boxwidth 1 relative
set xlabel "Classifier"
set ylabel "Statistic (%)"
set xlabel offset -1,-1
set style data histograms
set style histogram cluster gap 3
set style fill solid 1
set style fill pattern 3
set grid
set yrange [0:130]
set ytics 20
plot 'M_I' using ($2*100) title "Accuracy" fs pattern 3,'M_I' using ($3*100) title "Precision" fs pattern 1, 'M_I' using ($4*100) title "Recall" fs pattern 4,'M_I' using ($5*100):xtic(1) title "F1" fs pattern  2,