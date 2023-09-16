import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")

X = [1,2,3,4,5,6,7,8,9,10]
Y = [5,6,2,3,13,4,1,2,4,8]
Z = [2,3,3,3,5,7,9,11,9,10]

scattering = ax.scatter(X,Y,Z, c="r", marker="o", edgecolor="black", s=32)

ax.set_xlabel("x-axis")
ax.set_ylabel("y-axis")
ax.set_zlabel("z-axis")

plt.show()