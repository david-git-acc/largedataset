# largedataset
Repository containing my visualisations on the A Level Maths large dataset.

The repository containing my data visualisation programs on the large data set (A Level Maths). This is a dataset provided by Pearson/Edexcel for 
A Level Mathematics students for their level 3 stats exams in the UK. The plots are primarily focussed on the 5 UK weather stations 
(Hurn, Heathrow, Camborne, Leuchars, Leeming).

I thought this data was a good opportunity to learn how to plot 3D graphs with matplotlib and also test my knowledge of pandas, which I have only recently begun to learn.

There are 3 main programs here:

**meantempsuk.py**
This is a 4D (3 space, 1 colour) set of bar charts. The goal is to compare the differences in daily mean temperature and sunshine 
between the figures in 1987 and those in 2015, measuring these at 5 specific weather stations in the UK. Each bar is for a weather station at a 
given month, with the z-axis and colour dimension representing the data for that station at that time.

x-axis: The weather stations 
y-axis: The month (Ranges from May-Oct) 
z-axis: Daily Mean Temperature (°C) (daily data meaned for each month) 
colour: Daily Total Sunshine (hrs) (daily data meaned for each month)

This program has 3 graphs - the first showing conditions in 1987, the second showing conditions in 2015, and the third plotting the temperature 
difference between them. Note that the colour axis doesn't exist in the latter, since I chose a red-blue colourmap to better emphasise the changes 
in temperature.

There is also a version which only plots one graph for the sake of clarity and emphasis.

**windycorrelationsuk.py**
This is a 4D (3 space, 1 colour) scatter plot which tries to correlate weather conditions in the UK for a given weather station. Once plotted, 
a least-squares regression plane is drawn to suggest correlation between the variables.

x-axis: Daily Mean Visibility (dm) 
y-axis: Daily Mean Pressure (hPa) 
z-axis: Daily Mean Windspeed (kn) 
colour: Daily Mean Total Cloud (oktas)

The regression plane coefficients are also mentioned in the figure. I don't know how to calculate the PMCC for 3D 
so unfortunately this could not be included in the plot.

**weatherboxplots.py** 
This is a set of 4 box plot diagrams that takes any weather station (the 5 UK ones + Beijing, Perth, Jacksonville) 
and compares these quantities recorded in 1987 with those of 2015:

Daily Mean Air Temperature (°C) 
Rainfall (mm) 
Daily Mean Pressure (hPa) 
Daily Mean Wind Speed (kn)

For each quantity, a subplot is drawn, with 2 boxplots (one for 1987 data and another for 2015 data) being drawn on each subplot for a total of 8 boxplots.

**other programs**
I also kept my 3D bar chart and scatter plot tutorials in my project, since this is the first time I've worked with 3D data 
and I believe that they were crucial to my learning experience.

Also I've attached the images of my plots as well.
