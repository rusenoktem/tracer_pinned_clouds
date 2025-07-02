import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.patches import Arc  # Import Arc from patches
from matplotlib import cm
import matplotlib.image as mpimg
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

# Image display functions
def display_imagepair(x, y1,y2, img_path1,img_path2, title, txt1,txt2, x_pos1,x_pos2, xlm, ylm):
    ax1 = fig.add_axes([x, y1, 0.35, 0.22])
    display_image(ax1,img_path1,txt1,x_pos1,xlm,ylm)
    ax1.set_title(title)
    ax2 = fig.add_axes([x, y2, 0.35, 0.22])
    display_image(ax2,img_path2,txt2,x_pos2,xlm,ylm)
    
# Image display functions
def display_image(ax, img_path, txt, x_pos, xlm, ylm):
    img = mpimg.imread(img_path)
    ax.imshow(img)
    ax.axis('off')
    sc1 = (xlm[1]-xlm[0])*.02
    sc2 = (xlm[1]-xlm[0])*.05
    ax.set_xlim(xlm)
    ax.set_ylim(ylm)
    ax.invert_yaxis()  # Correct the upside-down issue
    ax.text(x_pos[0], x_pos[1], 'x', color='white', fontsize=8, fontweight='bold')
    ax.text(xlm[0]+sc1, ylm[0]+sc2, txt, color='white', fontsize=7)
    ax.set_aspect('equal')        
    
def overlay(tm, xv, yv, xb, yb, xlbl, ylbl, camxy, pp, ws):
    c_N = 18
    # Define the color space
    cspace = colors.cspace
    
    hist, xedges, yedges = np.histogram2d(xv, yv, bins=[xb, yb])
    data = hist.T * 100 #/ 1.99 #np.sum(hist)
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
    cb.ax.set_yticklabels([f"{math.floor(x * mxv*1e-3):.0f}" for x in np.linspace(0, 1, 4)])
    cb.set_label(r'$\mathrm{ \times 10^3 \ [km^{-2}]}$', fontsize=8)

    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.scatter(camxy[:, 0], camxy[:, 1], colors.ptsz, c=colors.cam, marker='o')
    plt.scatter(0, 0, colors.ptsz, c=colors.amf, marker='o')
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
  
    plt.quiver(c[0], c[1], ws[0], ws[1], angles='xy', scale_units='xy', scale=1/sc, color='black', width=0.004)

def overlay_height(tm, xv, yv, xb, yb, xlbl, ylbl, camxy, pp):
    c_N = 18
    # Define the color space
    cspace = colors.cspace
    
    hist, xedges, yedges = np.histogram2d(xv, yv, bins=[xb, yb])
    data = hist.T * 100 #/ 1.77 #np.sum(hist)
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
    cb.ax.set_yticklabels([f"{round(x * mxv*1e-4):.0f}" for x in np.linspace(0, 1, 4)])
    cb.set_label(r'$\mathrm{ \times 10^4 \ [km^{-2}]}$', fontsize=8)

    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.scatter(camxy[:, 1], np.zeros_like(camxy[:, 1]), colors.ptsz, c=colors.cam, marker='o')
    plt.scatter(0, 0, colors.ptsz, c=colors.amf, marker='o')
    #plt.scatter(0, 0, 21, edgecolors='black', facecolors='none', marker='o')
    plt.scatter(pp[:, 1], np.zeros_like(pp[:, 1]), colors.ptsz, c=colors.plants, alpha=0.8)
    #plt.scatter(pp[:, 1], np.zeros_like(pp[:, 1]), 15, edgecolors='black', facecolors='none', marker='o')
    
# Load data
camxy = np.array([[11.91, 2.664],
                  [11.81, 1.525]])

ppxy = np.array([[1.255, -4.9214],
                 [-0.485, -5.23]])


# Setup figure
fig = plt.figure(figsize=(7, 5))

# Subplot (a)

im1 = '../Data/houstereocamaS5.a1.20220513.121400.jpg'
im2 = '../Data/houstereocamaS5.a1.20220513.122900.jpg'
display_imagepair(0.05,0.75,0.5,im1,im2,'(a) 13 May 2022','7:14 LT','7:29 LT',np.array([779.5, 1418]),np.array([1950, 1225]),np.array([600, 2200]),np.array([1000, 1600]))

# Subplot (b)
im1 = '../Data/houstereocamaS5.a1.20220622.115300.jpg'
im2 = '../Data/houstereocamaS5.a1.20220622.120000.jpg'
display_imagepair(0.55,0.75,0.5,im1,im2, '(b) 22 June 2022','6:53 LT','7:00 LT',np.array([631, 1389]),np.array([856, 1308]),np.array([300, 1100]),np.array([1260, 1560]))

# Subplot (c)
mat = scipy.io.loadmat('../Data/plume20220513.mat')  
data = mat['data']
tmI = mat['tmI']

ax1 = fig.add_axes([0.05, 0.15, 0.38, 0.28])
# Replace with your actual overlay function
overlay(tmI,data[:, 4] * 1e-3, data[:, 5] * 1e-3,np.arange(-3, 10.1, 0.1), np.arange(-6, 3.9 + 0.1, 0.1), 'to East [km]', 'to North [km]', camxy,ppxy,np.array([4.6435027,6.3912349]))
ax1.set_aspect('equal')
ax1.set_xlim([-2, 12.2])
ax1.set_ylim([-6, 4])
#ax1.set_title('7:00-8:59 LT',fontsize=10)
#ax3.set_title('(c) 13 May 2022, 0700-0859 LT')

# Subplot (d)
mat = scipy.io.loadmat('../Data/plume20220622.mat')  
data = mat['data']
tmI = mat['tmI']

ax2 = fig.add_axes([0.55, 0.15, 0.38, 0.3])
overlay_height(tmI, data[:, 5] * 1e-3, data[:, 6] * 1e-3,
               np.arange(-6, 4, 0.1), np.arange(0, 3.9 + 0.1, 0.1),
               'to North [km]', 'height [km]', camxy, ppxy)  
ax2.set_aspect('equal')
ax2.set_xlim([-6, 3])
ax2.set_ylim([-0.1, 6])
#ax2.set_title('Composite over 6:30-8:16 LT',fontsize=10)

#plt.show()
plt.savefig('../fig6.png', dpi=300, bbox_inches='tight')
