import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import datetime as dt

name="Leeming"

# Kill units from column names so it's easier to address
def trim_units(string):
    bad = string.index("(") if "(" in string else len(string)+1
    return string[0:bad-1]


leemingdata = pd.read_excel("weather_data.xls" , 
                            sheet_name=f"{name} May-Oct 2015" , 
                            skiprows=5, 
                            na_values=["n/a","tr"])
leemingdata = leemingdata.fillna(0)

# The last 4 columns aren't data, just background info 
leemingdata = leemingdata.drop(index= leemingdata.tail(4).index)

# I want to remove the units off the names so it's easier to address them
old_column_names = list( leemingdata.columns )
new_column_names = [ trim_units(name) for name in old_column_names  ]


# Renaming time
renaming = dict(zip(old_column_names, new_column_names))
leemingdata = leemingdata.rename(columns=renaming)

rainfall = leemingdata["Daily Mean Visibility"].values
pressures = leemingdata["Daily Mean Pressure"].values
windspeeds = leemingdata["Daily Mean Windspeed"].values[:, 0]
cloudcover = leemingdata["Daily Mean Total Cloud"].values   

# This is for daily cloud cover
cloud_cmap=mcolors.LinearSegmentedColormap.from_list('rg',["navy","cyan"], N=256) 
norm = mcolors.Normalize(vmin = cloudcover.min(), vmax = cloudcover.max())

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


scattering = ax.scatter( rainfall, pressures, windspeeds, 
                        c=norm(cloudcover),
                        cmap=cloud_cmap,
                        s=32,
                        edgecolor="black")

ax.set_xlabel("Daily Mean Visibility (dam)")
ax.set_ylabel("Daily Mean Pressure (hPa)")
ax.set_zlabel("Daily Mean Windspeed (0000-2400) (kn)")

requiredbarticks = np.round( np.linspace(0,8, 6), decimals=2)
bar = plt.colorbar(
                   mappable=scattering, 
                   ax=ax,
                   extend="both", 
                   label="Daily Mean Total Cloud (oktas)", 
                   orientation="horizontal",
                   fraction=0.046, 
                   pad=0.04)




bar.set_ticklabels(requiredbarticks)

plt.suptitle(f"Comparing daily mean visibility, daily mean pressure and daily mean windspeed in {name}, 2015", fontsize=16)


plt.show()