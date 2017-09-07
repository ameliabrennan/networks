<<<<<<< HEAD
'''
Simple template for plotting with matplotlib. Please add to it as necessary!
In the future it may be worth designing a custom rc file, see http://matplotlib.org/users/customizing.html for example.
TODO: 2D plotting, interpolating, colour gradients, error bars, stacked hists, plotting from dataframe, ...
'''

import numpy as np
from scipy import interpolate
import matplotlib
import matplotlib.pyplot as plt
from RMIT_colours import *

#################################  The data, labels etc - these are all things you should change for your own plot  #################################

fig_dir = '/Users/....'
fig_name = 'My_name.png' # choose your file type, pdf is fine

# Some fake data
x = np.linspace(0, 10, 100)
y = np.cos(x)
z = np.sin(x)

# alternatively:
#x = [1,2,3]
#y = [6,3,7]

# For drawing some lines on the plot, these are absolute values
xline_val = 2
yline_val = 2

# For positioning some text, these are absolute values
pos_x = 0.5
pos_y = 0.3

# Titles etc
title = 'A title'
x_title = 'My x title'
y_title = 'My y title'

# Optional labels for the legend
label1 = 'dataset 1'
label2 = 'dataset 2'

# optional limits of plot
x_lims = [-1, 15]
y_lims = [-1.5, 1.5]

# manually set the tick values and labels
x_ticks = [1, 5, 10]
x_tick_labels = ['Tom', 'Dick', 'Harry']
y_ticks = []
y_tick_labels = []

#################################  Building up the plot, certain things should be included or commented, but changing things like fontsize etc should only be done if necessary, if we want to maintain consistent style!  #################################

# set up the initial figure. 'ax' confusingly refers to a specific graph within the bigger 'plt' which is the whole thing.
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)  # this sets up a specific subplot, logic is row-column-number. A single plot should be 111.
#ax1 = fig.add_subplot(211)
#ax2 = fig.add_subplot(212)

# set the main 2 colours, others are available in RMIT_colours.py.
col1 = RMIT_DarkBlue
col2 = RMIT_Red

# set universal fontsize
fontsize = 20

# define linewidth, linestyle, markerstyle, markersize, transparency
linew = 5
lines = 'solid' # 'solid', dashed', 'dotted', 'dashdot'
markers = '.' # '.' (point), 'o' (circle), 'v' (upside down triangle), '^' (upright triangle), 's' (square), '*' (star), '+' (plus), 'x' (cross), see https://matplotlib.org/api/markers_api.html for more
markersize = 200
alpha = 1.0 # set this to < 1 for transparency


# Draw the data. Any of these can be done alone, or in combination, just uncomment whichever are needed.

# simple line plot
#ax.plot(x,y, color=col1, linewidth=linew, linestyle = lines, alpha = alpha)

# scatter plot
ax.scatter(x,y, color=col1, marker = markers, s = markersize, alpha = alpha, label = label1)
ax.scatter(x,z, color=col2, marker = markers, s = markersize, alpha = alpha, label = label2)

# histogram (stacked hists are also available)
#ax.hist(y, color=col1, alpha = alpha) # bins=X, range=[1, 100]

# vertical bar graph
#ax.bar(x,y, color=col1, alpha = alpha)

# horizontal bar graph
#ax.barh(x,y, color=col1, alpha = alpha)

# a horizontal line
#ax.axhline(yline_val, color=col1, linewidth=linew, linestyle = lines, alpha = alpha)

# vertical line
#ax.axvline(xline_val, color=col1, linewidth=linew, linestyle = lines, alpha = alpha)

# fill between y-vals and 0
#ax.fill_between(x,y, color=col1, alpha = alpha)

# Add some text
ax.text(pos_x, pos_y, 'Hello!',
        horizontalalignment='left',
        verticalalignment='center',
        rotation=45,
        fontsize=fontsize,
        color=col1)

# Customise the figure
ax.set(xlim=x_lims, ylim=y_lims)
ax.xaxis.set(ticks=x_ticks, ticklabels=x_tick_labels)
ax.yaxis.set(ticks=y_ticks, ticklabels=y_tick_labels)

# set log scale if desired. Note this may not be compatible with axis labels etc. Make sure your range doesn't include 0.
#ax.set_xscale('log')
#ax.set_yscale('log')

# remove the box, leave just the axes
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# set the titles
ax.set_title(title, fontweight = 'bold', fontsize = fontsize)

ax.set(xlabel = x_title,
       ylabel = y_title)

# set font sizes to large everywhere
for item in ([ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(fontsize)

# set up the legend if needed
ax.legend(loc = 'best', frameon=False, fontsize=fontsize) # 'upper right', 'center', etc, see https://matplotlib.org/api/legend_api.html

# make sure everything fits nicely in the frame
plt.tight_layout()

# either show the plot onscreen (good for testing) or save to some folder
#plt.savefig(fig_dir + fig_name)
plt.show()
plt.close()
