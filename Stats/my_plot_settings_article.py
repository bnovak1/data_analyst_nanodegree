import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Figure size in inches
mpl.rcParams['figure.figsize'] = 3.54, 2.655

# Font size in plots
mpl.rcParams['font.size'] = 9

# legend font size
mpl.rcParams['legend.fontsize'] = 7.5

# Font size for added text
text_font_size = 8

# font
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'roman'
#mpl.rcParams['font.sans-serif'] = 'Helvetica'
mpl.rcParams['mathtext.fontset'] = 'cm'
        
# Line width in plots
mpl.rcParams['lines.linewidth'] = 0.5

# Marker size in plots
mpl.rcParams['lines.markersize'] = 3.0

# Errorbar width (points)
errbarW = 4

# Only one point in legends
mpl.rcParams['legend.numpoints'] = 1

# No box around legends, best location, change spacings
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.loc'] = 'best'
mpl.rcParams['legend.fontsize'] = 7.5
mpl.rcParams['legend.columnspacing'] = 0.5
mpl.rcParams['legend.labelspacing'] = 0.25
mpl.rcParams['legend.handletextpad'] = 0.2
mpl.rcParams['legend.handlelength'] = 1.85
mpl.rcParams['legend.handleheight'] = 0.5

# Space between tick labels and axes labels
axeslabelpad = 7

# Fraction of range edges of data should be from axes positions
datapadfraction = 0.05

# Don't output plots to screen
plt.ioff()
    

def axis_setup(axis_type):
    
    if axis_type == 'x':

        xmajticks = plt.xticks()[0]
        xmintick_len = (xmajticks[1] - xmajticks[0])/4.0
        plt.xlim(xmajticks[0] - xmintick_len, xmajticks[-1] + xmintick_len)
        
        xmajticks = plt.xticks()[0]
        xmintick_len = (xmajticks[1] - xmajticks[0])/4.0
        ml = MultipleLocator(xmintick_len); plt.axes().xaxis.set_minor_locator(ml)
    
    elif axis_type == 'y':

        ymajticks = plt.yticks()[0]
        ymintick_len = (ymajticks[1] - ymajticks[0])/4.0
        plt.ylim(ymajticks[0] - ymintick_len, ymajticks[-1] + ymintick_len)
        
        ymajticks = plt.yticks()[0]
        ymintick_len = (ymajticks[1] - ymajticks[0])/4.0
        ml = MultipleLocator(ymintick_len); plt.axes().yaxis.set_minor_locator(ml)
