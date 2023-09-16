import numpy as np
from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
plt.style.use('dark_background')
fig, ax1 = plt.subplots(subplot_kw={'projection': '3d'})

# In a 3D bar chart, you're going to have some finite number of bars - let's say 10 bars.
# Here's how the bars are plotted:
# Each bar is going to have to start somewhere on the xyz plane. Your initial x,y,z coordinates will mark the BEGINNING point of each bar
# Each bar will have a dx,dy and dz. The dx states how wide the bar will be, the dy states how thick the bar will be and dz how tall

# Let's create a 3x3 bar chart, so that it's in a square formation, with each bar having a square cross-section

# The first 3 bars will have the same x coordinate, then the next 3, then the next 3
x = 2*np.repeat(np.arange(3), 3)

# However the y-coordinates will constantly be changing mod 3, so we need to use concatenation for this
y = 2*np.concatenate( [np.arange(3)] * 3 )
z = np.zeros(9)

dx = np.ones(9)
dy = np.ones(9)
dz = 7*np.ones(9)

print(x)
print(y)



the_bars = ax1.bar3d(x,y,z,dx,dy,dz, color=["red","green","blue","yellow","orange","pink","purple","brown","grey"])

plt.show()