import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.patches import Arc  # Import Arc from patches
from matplotlib import cm
import scipy.io

class Colors:
    def __init__(self):
        self.plants = np.array([0.1, 0.1, 0.7])
        self.plantsnorth = np.array([0.8, 0.8, 0.2])
        self.amf = np.array([0.2, 0.8, 0.2])
        self.cam = np.array([1, 0, 0])
        self.ptsz = 21
        self.cspace = np.vstack([np.ones((1, 4)), 
   [0.125, 1.0, 0.875 ,1], 
    [0.0, 1.0, 1.0 ,1],
    [0.0, 0.875, 1.0, 1],
    [0.0, 0.75, 1.0, 1],
    [0.5, 1.0, 0.5 ,1],
    [0.625, 1.0, 0.375, 1],
    [0.75, 1.0, 0.25, 1],
    [0.875, 1.0, 0.125, 1],
    [1.0, 1.0, 0.0 ,1],
    [1.0, 0.875, 0.0 ,1],
    [1.0, 0.75, 0.0 ,1],
    [1.0, 0.625, 0.0, 1],
    [1.0, 0.5, 0.0 ,1],
    [1.0, 0.375, 0.0 ,1],
    [1.0, 0.25, 0.0, 1],
    [1.0, 0.125, 0.0 ,1],
    [1.0, 0.0, 0.0, 1],
    [0.875, 0.0, 0.0 ,1],
    [0.75, 0.0, 0.0 ,1]
])

colors = Colors()

# Replace with actual function to get colors if needed
def manuscript_marker_colors():
    return colors

def overlay(tm, xv, yv, xb, yb, xlbl, ylbl, camxy, pp, ws):
    c_N = 18
    # Define the color space
    cspace = colors.cspace
    
    hist, xedges, yedges = np.histogram2d(xv, yv, bins=[xb, yb])
    data = hist.T * 100 #/ 24.73 #np.sum(hist)
    I, J = np.nonzero(data)
    mxv = np.max(data)
    minv = 0
    c = np.round((data[I, J] - minv) * c_N / (mxv - minv)).astype(int)

    # Scatter plot with cspace colormap
    scatter = plt.scatter(xb[J], yb[I], 11, c=cspace[c], marker='s')

    # Create a Normalize object for scaling
    norm = Normalize(vmin=0, vmax=1)

    # Colorbar with custom colormap (ListedColormap)
    cb = plt.colorbar(plt.cm.ScalarMappable(cmap=ListedColormap(cspace), norm=norm), ax=plt.gca(), ticks=np.linspace(0, 1, 4))
    cb.ax.set_yticklabels([f"{round(x * mxv*1e-5):.0f}" for x in np.linspace(0, 1, 4)])
    cb.set_label(r'$\mathrm{ \times 10^5 \ [km^{-2}]}$', fontsize=10)

    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.scatter(camxy[:, 0], camxy[:, 1], colors.ptsz, c=colors.cam, marker='o')
    #plt.scatter(camxy[:, 0], camxy[:, 1], 23, edgecolors='black', facecolors='none', marker='o')

    plt.scatter(0, 0, colors.ptsz, c=colors.amf, marker='o')
    #plt.scatter(0, 0, 23, edgecolors='black', facecolors='none', marker='o')
    plt.scatter(pp[:, 0], pp[:, 1], colors.ptsz, c=colors.plants, alpha=0.8)
    
    # Optional wind arrows
    c = np.array([9, -3.5])
    radius = 5  # Radius of the hemicircle
    angle_start = 0  # Starting angle of the arc (in degrees)
    angle_end = 180  # Ending angle of the arc (in degrees)
    sc = 0.2
    
    # Create an Arc (half circle)
    hemicircle = Arc(c, 2*sc*radius, 2*sc*radius, angle=0, theta1=angle_start, theta2=angle_end, color='black', linestyle='-', linewidth=2)

    # Add the hemicircle to the plot via the axes object
    ax1.add_patch(hemicircle)  # Use ax1 to add the patch
    
    for wind in ws:
        plt.quiver(c[0], c[1], wind[0], wind[1], angles='xy', scale_units='xy', scale=1/sc, color='black', width=0.004)

def overlay_height(tm, xv, yv, xb, yb, xlbl, ylbl, camxy, pp):
    c_N = 18
    # Define the color space
    cspace = colors.cspace
    
    hist, xedges, yedges = np.histogram2d(xv, yv, bins=[xb, yb])
    data = hist.T * 100 #/ 24.73 #np.sum(hist)
    I, J = np.nonzero(data)
    mxv = np.max(data)
    minv = 0
    c = np.round((data[I, J] - minv) * c_N / (mxv - minv)).astype(int)

    # Scatter plot with cspace colormap
    scatter = plt.scatter(xb[J], yb[I], 11, color=cspace[c], marker='s')

    # Create a Normalize object for scaling
    norm = Normalize(vmin=0, vmax=1)

    # Colorbar with custom colormap (ListedColormap)
    cb = plt.colorbar(plt.cm.ScalarMappable(cmap=ListedColormap(cspace), norm=norm), ax=plt.gca(), ticks=np.linspace(0, 1, 4))
    cb.ax.set_yticklabels([f"{round(x * mxv*1e-5):.0f}" for x in np.linspace(0, .98, 4)])
    cb.set_label(r'$\mathrm{ \times 10^5\ [km^{-2}]}$', fontsize=10)

    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.scatter(camxy[:, 1], np.zeros_like(camxy[:, 1]), colors.ptsz, c=colors.cam, marker='o')
    plt.scatter(0, 0, colors.ptsz, c=colors.amf, marker='o')
    #plt.scatter(0, 0, 21, edgecolors='black', facecolors='none', marker='o')
    plt.scatter(pp[:, 1], np.zeros_like(pp[:, 1]), colors.ptsz, c=colors.plants, alpha=0.8)
    #plt.scatter(pp[:, 1], np.zeros_like(pp[:, 1]), 15, edgecolors='black', facecolors='none', marker='o')
    
# Load data
mat = scipy.io.loadmat('../Data/plume_all.mat')  # adjust path as needed
data_all = mat['data_all']
ws = mat['ws']

camxy = np.array([[11.91, 2.664],
                  [11.81, 1.525]])

ppxy = np.array([[1.255, -4.9214],
                 [-0.485, -5.23]])

# Filter data
ind = np.where((data_all[:, 6] > -5550) & (data_all[:, 5] > -1900))
data_all = data_all[ind]

# Setup figure
fig = plt.figure(figsize=(6, 6))

# Subplot (a)
ax1 = fig.add_axes([0.15, 0.59, 0.73, 0.37])
overlay(data_all[:, 0], data_all[:, 5] * 1e-3, data_all[:, 6] * 1e-3,
        np.arange(-3, 10.1, 0.1), np.arange(-6, 3.9 + 0.1, 0.1),
        'to East [km]', 'to North [km]', camxy, ppxy, ws)
ax1.set_aspect('equal')
ax1.set_xlim([-2, 12.2])
ax1.set_ylim([-6, 4])
ax1.set_title('(a)')

# Subplot (b)
ax2 = fig.add_axes([0.15, 0.08, 0.73, 0.37])
overlay_height(data_all[:, 0], data_all[:, 6] * 1e-3, data_all[:, 7] * 1e-3,
               np.arange(-6, 3.9 + 0.1, 0.1), np.arange(0, 3.9 + 0.1, 0.1),
               'to North [km]', 'height [km]', camxy, ppxy)  
ax2.set_aspect('equal')
ax2.set_xlim([-6, 3])
ax2.set_ylim([-0.1, 6])
#ax2.set_aspect(9 / 6)
ax2.set_title('(b)')

#plt.show()
plt.savefig('../fig5.png', dpi=300, bbox_inches='tight')
