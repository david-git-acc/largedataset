import pandas as pd
import numpy as np
import datetime as dt

names = ["Heathrow" , "Hurn" , "Leeming" , "Leuchars" , "Camborne"]
name_data = []


# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]

for name in names:

    # Read in the excel sheet - the data begins the first 5 rows
    data2015 = pd.read_excel("weather_data.xls", sheet_name=f"{name} May-Oct 2015", skiprows=5)

        
        

    # Kill the last 4 rows, they're not actually data
    data2015 = data2015.drop(index=data2015.tail(4).index)


        
    # I want to remove the units off the names so it's easier to address them
    old_column_names = list( data2015.columns )
    new_column_names = [ trim_units(name) for name in old_column_names  ]

    # Renaming time
    renaming = dict(zip(old_column_names, new_column_names))

    # Doing the renaming
    data2015 = data2015.rename(columns=renaming)



    # Convert the date strings to datetimes so we can perform a monthly resampling
    data2015["Date"] = pd.to_datetime( data2015["Date"] )

    # Set the index to date for resampling
    data2015 = data2015.set_index("Date")

    # Perform resampling 
    data2015 = data2015.resample("M").mean()

    # Let's get the monthly mean temperature

    monthlytemp = list( data2015["Daily Mean Temperature"] )
    sunshine = list ( data2015["Daily Total Sunshine"])
    
    # Gather all of the data for this location and add to the name data
    info_dict_for_this_data = {"name" : name, "monthlytemp" : monthlytemp, "sunshine" : sunshine}
    name_data.append(info_dict_for_this_data)
    
    
    if name == "Camborne":
        print(monthlytemp)


from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

fig, ax = plt.subplots(1,1,subplot_kw={"projection" : "3d"})

x =  2*np.repeat(np.arange(5), 6)
y = 2*np.concatenate( [np.arange(6)] * 5 )
z = np.zeros(30)

d = np.ones(30)

my_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["darkred", "yellow", "lime"], N=256) 



totalmonthlytemp = []
totalmonthlysunshine = []
for nm in name_data:
    totalmonthlytemp.extend( nm["monthlytemp"] )
    totalmonthlysunshine.extend( nm["sunshine"] )
    
totalmonthlytemp = np.asarray(totalmonthlytemp)
totalmonthlysunshine = np.asarray(totalmonthlysunshine)

# Normalize your data to the colormap's range (0 to 1)
norm = mcolors.Normalize(vmin=totalmonthlysunshine.min(), vmax=totalmonthlysunshine.max())
    

the_bars = ax.bar3d(x, y, z, d, d, totalmonthlytemp,color=my_cmap(norm( totalmonthlysunshine) ), cmap = my_cmap)

ax.set_yticklabels(["placeholder", "May","June","July","August","September","October"])
ax.set_xticklabels(["placeholder"] +  names)

ax.set_zlim(0, totalmonthlytemp.max())

ax.set_xlabel("Month")
ax.set_ylabel("Location")
ax.set_zlabel("Mean temperature")

# Implementing the bar - the fraction and pad are to keep it well sized
bar = plt.colorbar(mappable = the_bars, extend="both", orientation="horizontal", fraction=0.046, pad=0.04, label="Daily mean sunshine")



plt.show()


