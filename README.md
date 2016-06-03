# plotyoda
use matplotlib to plot yoda histogram files.

This is a very simple script which I use to plot yoda histogram files.
It creates latex pgf and corresponding pdf images.
The input is read from a json file which you have use as cmd line option
    python plot.py test.json

## JSON options:
It plots all histograms specified in "histograms" if "which" contains normal.
If "which" also contains "ratio", it plots the ratio HistogramN/Histogram1. 
Matplotlib options are given in "config". I added all options so far.
