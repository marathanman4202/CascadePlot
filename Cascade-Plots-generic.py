# scripts  by Roy Haggerty for generation of Cascade Plot and 
# associated strip charts bottom and right. 
# Based on code written by Roy Haggerty for Willamette Water 2100
# project, funded by US National Science Foundation, 
# grant # EAR-1039192.
# Some code written by Owen Haggerty, summer, 2014.
# 
# Reference as:
# Haggerty, R. (2014), Python script for generation of cascade plots and 
#   associated strip charts 
#
# Python 2.7
# Dependencies & libraries that need to be installed:
#    numpy
#    matplotlib
#    xlrd
#
#  

########################################################################################
########################################################################################
########################################################################################

def cascade(
            file_model_csv,             #the name of the reference file
            column,
            title,                      #the title of the graph to be generated
            graph_name_png,             #path & name of output png file
            data_type = 'default',      #the type of data
            Display = False,            #whether the graph is to be displayed(True) or saved as a PNG file(False)
            ):
                
    """
    Make a cascade plot and associated side & bottom graphs to show time series
    of discharge.  Shade some of the lines with range of possible values for
    alternative scenarios.
    """
    
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime
    import matplotlib as mpl
    import constants as cst   # constants.py contains constants used here
    import matplotlib.gridspec as gridspec
    from   mpl_toolkits.axes_grid1 import make_axes_locatable
    from matrix_from_xls import matrix_from_xls
    
    np.set_printoptions(precision=3) 

# Set parameters and plot information here:
    start_year = 1960
    end_year = 2013
    num_years = end_year - start_year + 1
    

#       Collect data for plotting from csv file:
    data_2D = matrix_from_xls(
            file_model_csv,column,cst.days_in_yr,0
            )
        
    data_set_rhs_3 = process_data_rhs( 
            data_2D, num_years, data_type, start_year, end_year 
            )

    data_early, data_mid, data_late = process_data_bottom(
            data_2D, num_years, data_type, start_year, end_year
            )
          
    ylabel2, ylabel4 \
        = get_labels(
            data_2D, num_years, data_type, start_year, end_year
            )

      
    ##########################################################
    #   Prepare the figure "canvas"                          #
    ##########################################################

    if data_type == 'default':
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],256)
    elif data_type == 'other':
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white',(0.9,0.1,0.1)],256)
    else:
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],256)
        
    fig = plt.figure(1, figsize=(10,8))
    width_ratios=[3.5, 1.1]
    height_ratios = [4., 1.5]
    wspace = 0.1     # horizontal space btwn figs
    hspace = 0.08     # vertical space btwn figs
    
    ###### Figure canvas left side
    gs1 = gridspec.GridSpec(2, 2, width_ratios=width_ratios,
                            height_ratios=height_ratios,
                            wspace = wspace)
        
    gs1.update(left=0.1, right = 1.1, wspace=wspace, hspace = hspace)
    
    ##########################################################
    #   Prep the first plot (cascade)                        #
    ##########################################################

    ax = fig.add_subplot(gs1[0,0])
    p = plt.imshow(data_2D, origin='lower', cmap = cmap1, aspect='auto',                     # with revised color ramp
                  extent=[cst.day_of_year_start, 365 + cst.day_of_year_start - 1 , start_year, end_year]) 
    month_labels(ax)
    ax.set_ylabel('$Water \, Year$', fontsize=14)
    ticks=np.arange(2020,2100,10)
    plt.yticks(ticks, fontsize=14)
#    plt.title(title2,fontsize=12)  # could put a subtitle above cascade plot
    plt.suptitle(title, fontsize = 18)
#    props = dict(boxstyle='round', facecolor='wheat', alpha=0.85, lw=0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.04, aspect=20)
    plt.colorbar(p,cax=cax).set_label(ylabel2)

    ##########################################################
    #   Prep the bottom strip                                #
    ##########################################################
    
    ax4 = fig.add_subplot(gs1[1,0], aspect = 'auto', sharex=ax)
    ax4.plot(range(cst.day_of_year_start, 365 + cst.day_of_year_start),
             data_early, color="0.62", lw=1.5)
    ax4.plot(range(cst.day_of_year_start, 365 + cst.day_of_year_start),
             data_mid, color="0.32", lw=1.5)
    ax4.plot(range(cst.day_of_year_start, 365 + cst.day_of_year_start),
             data_late, color="0.", lw=1.5)
    month_labels(ax4)
    ax4.set_xlabel('$Month \, of \, Year$', fontsize=14)
    ax4.set_ylabel(ylabel4, fontsize=14)
    ax4.legend(('Early', 'Mid', 'Late'),
               loc='best',frameon=False, fontsize=12)

#   Uncomment this to set a limit on y axis:
#    ax4.set_ylim(0, 50)
        
    divider2 = make_axes_locatable(ax4)
    cax2 = divider2.append_axes("right", size="5%", pad=0.01)
    cax2.axis('off')
    cax2.set_visible(False)
    max_yticks = 5
    yloc = plt.MaxNLocator(max_yticks)
    ax4.yaxis.set_major_locator(yloc)
    plt.colorbar(cax=cax2)
    
    ##########################################################
    #   Prep the right side figure canvas                    #
    #   Generate parameters common to one or both plots      #
    ##########################################################
    
    gs2 = gridspec.GridSpec(2, 2, width_ratios=width_ratios,
                            height_ratios=height_ratios)
        
    gs2.update(left=0.35, right = 0.94, wspace=wspace, hspace = hspace)
    
    max_xticks = 2
    y = range(start_year,end_year)

    ##########################################################
    #   Prep the right-hand strip chart                      #
    ##########################################################

    ax5 = fig.add_subplot(gs2[0,1], aspect = 'auto', sharey=ax)

    xloc = plt.MaxNLocator(max_xticks)
    ax5.xaxis.set_major_locator(xloc)
    plt.ylim(start_year,end_year)
    ax5.yaxis.tick_right()
    plt.yticks(ticks, fontsize=14)
    if data_type == 'default':
        print np.shape(data_set_rhs_3)
        print num_years
        ax5.plot(data_set_rhs_3, range(start_year,end_year+1), color="0.35", lw=1.5)
        plt.xlabel('$Avg \, Q$ [m$^{\t{3}}$/s]', fontsize = 14)
        
    else:
        print 'data_type undefined for right-hand-side plotting'
        raise Exception
        
    xloc = plt.MaxNLocator(max_xticks)
    ax5.xaxis.set_major_locator(xloc)
    plt.ylim(start_year,end_year)
    ax5.yaxis.tick_right()
    plt.yticks(ticks, fontsize=14)

    ###################################################################
    #   Add metadata text box in lower right, citing figure details   #
    ###################################################################
    textstr = 'Default plot\n' \
              + ' Graph generated on ' + str(datetime.date.today()) 
    props = dict(boxstyle='round', facecolor='white', alpha=0.5, lw=0.)

    ax4.text(1.03, -0.2, textstr, transform=ax.transAxes, fontsize=6,
            verticalalignment='top', bbox=props)

    ##########################################################
    #   Save or display the plots                            #
    ##########################################################

    if Display:
        plt.show()
    else:
        plt.savefig(graph_name_png, format="png", dpi=300)
    plt.close(1)

#   End of script for cascade plots


########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
    
#  Supporting functions


def process_data_rhs(data_2D, num_yrs,  \
        data_type, start_year, end_year):
    """
    Process dat needed for plotting
    """

    import numpy as np
    from movingaverage import movingaverage, n_take_k

    ##########################################################
    # Assemble the data needed on the right-hand-side plot.  #
    # This may differ with data_type, but details will need  #
    # to be defined here.      nnnnnn                        #
    ##########################################################
    data_set_rhs_3 = np.empty([1])

    if data_type == 'default':        
        yearly_avg = [np.mean(data_2D[i,:]) for i in range(num_yrs)]  
        averaging_window = 7
        window_raw = np.array([])
        window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
        window = window_raw / np.sum(window_raw)  # normalized weights
        yearly_avg = movingaverage(
            yearly_avg[:averaging_window] + yearly_avg + yearly_avg[-averaging_window:],
            window)[averaging_window:-averaging_window]
        data_set_rhs_3 = yearly_avg
    else:
        print 'data_type is undefined in process_data function'
        raise Exception
        
    return data_set_rhs_3
    

def get_labels(
        data_2D, num_yrs, data_type, start_year, end_year
        ):
    """
    Provide labels and titles for plotting
    """
    
    ylabel2 = ''
    ylabel4 = ''

    if data_type == 'default' :
        
        ylabel2 = '$Default \,$ [m$^{\t{3}}$/s]'
        ylabel4 = '$Default longer (Q)\,$ [m$^{\t{3}}$/s]'
                  
    else:
        print 'data_type not defined in get_labels function'
        raise Exception

    return ylabel2, ylabel4


def process_data_bottom(
            data_2D, num_yrs, data_type, start_year, end_year
            ):
    """
    Returns 3 data sets for plotting on bottom strip
    """
    
    import numpy as np
    from movingaverage import movingaverage, n_take_k
    
    ##########################################################
    #   Prep the data for the bottom strip                   #
    ##########################################################
    
    averaging_window = 31
    window_raw = np.array([])
    window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
    window = window_raw / np.sum(window_raw)  # normalized weights

    # Calculate moving averages (using binomial filter - in movingaverage).
    # Prepend and append half of averaging window to data window so that moving average at early
    #   and late time are correct.

    data_early = movingaverage([np.mean(data_2D[0:19,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[0:19,i]) for i in range(365)] +
                               [np.mean(data_2D[0:19,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
    data_mid   = movingaverage([np.mean(data_2D[20:39,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[20:39,i]) for i in range(365)] +
                               [np.mean(data_2D[20:39,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
    data_late  = movingaverage([np.mean(data_2D[40:,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[40:,i]) for i in range(365)] +
                               [np.mean(data_2D[40:,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
                               
    return data_early, data_mid, data_late       
    
def month_labels (axys):
    """
    Place month labels on horizontal axis.  This is a little tricky,
       so I found some code on the web and modified it.
    """
    from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
    import matplotlib.dates as dates
    import matplotlib.ticker as ticker

    axys.xaxis.set_major_locator(dates.MonthLocator())
    axys.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
    axys.xaxis.set_major_formatter(ticker.NullFormatter())
    axys.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    for tick in axys.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')
    return

def BoxPlot(axys, variable):
    """
    Create and plot the boxes for the box-and-whisker plot
    """
    import matplotlib.pyplot as plt
#    import numpy as np
    variableT = variable.T
#    col = (0.6,0.6,1.)  # light blue in rgb
    col = (0.6, 0.6, 0.6) # light gray in rgb
    positions=range(2015,2096,10)
    box = axys.boxplot(variableT, vert=False,positions=positions,widths=9.2,
                       whis=2,sym='',patch_artist=True)
    plt.setp(box['boxes'], color=col)
    colors = [col]*9
    for patch, colors in zip(box['boxes'], colors):
        patch.set_facecolor(colors)
    for cap in box['caps']:
        cap.set(linewidth = 0)
    for whisker in box['whiskers']:
        whisker.set_linestyle('solid')
        whisker.set_linewidth(1)
    return

def check_if_empty(element):
    if element == '':
        return False
    else:
        return True
        
def paths(master_file):
    import xlrd
    Path_book = xlrd.open_workbook(master_file)
    Reference_path = tuple(Path_book.sheet_by_index(0).col_values(8))[7]
    write_path = tuple(Path_book.sheet_by_index(0).col_values(8))[8]
    return Reference_path, write_path


########################################################################################
########################################################################################
########################################################################################

######################################################
#####   SCRIPT TO GENERATE THE PLOTS             #####
######################################################
"""
 This script generates a set of plots by first reading in the names of files
 and associated parameters from an xls file.  That file is called
 "master file.xls"
"""
# kwargs:
#   data_type = 'default' (default)

import constants as cst   # constants.py contains constants used here
import xlrd
# NAME OF MASTER FILE:
master_file = 'master file.xls'
path_data, path_write = paths(master_file)
import metadata

# Read a parameter file in xls format.
cascade_plot_params = xlrd.open_workbook(master_file)
file_model_csv = cascade_plot_params.sheet_by_index(0).col_values(0)[1:]        # name of data file for plot
file_name_list = list(file_model_csv)
# Remove any names that are empty
file_name_list = filter(check_if_empty, file_name_list)
total_number_of_plots = len(file_name_list)

column = cascade_plot_params.sheet_by_index(0).col_values(1)[1:total_number_of_plots+1]                 
title = cascade_plot_params.sheet_by_index(0).col_values(2)[1:total_number_of_plots+1]                 # title for plot
ToBePlotted = cascade_plot_params.sheet_by_index(0).col_values(3)[1:total_number_of_plots+1]           # make this plot? True or False
Display_v = cascade_plot_params.sheet_by_index(0).col_values(4)[1:total_number_of_plots+1]             # Display plot on screen (True) or as png file (False)\
data_type_v = cascade_plot_params.sheet_by_index(0).col_values(5)[1:total_number_of_plots+1]           # type of data
graph_name_v = cascade_plot_params.sheet_by_index(0).col_values(6)[1:total_number_of_plots+1]           # type of data

# Make the plots.
plot_number = -1
for file in file_name_list: 
    plot_number += 1
    if ToBePlotted[plot_number]:
        file_name_ToBeUsed = path_data + file_name_list[plot_number]
        graph_name = path_write + graph_name_v[plot_number]
        col_num = int(column[plot_number])
        cascade(
            file_name_ToBeUsed,
            col_num,
            title[plot_number],
            graph_name,
            Display = Display_v[plot_number],
            data_type = data_type_v[plot_number],
            )
