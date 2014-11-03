# scripts  by Roy Haggerty for generation of Cascade Plot and 
# associated strip charts bottom and right. 
# Based on code written by Roy Haggerty for Willamette Water 2100
# project, funded by US National Science Foundation, 
# grant # EAR-1039192.
# Some code written by Owen Haggerty, summer, 2014.
# 
# Reference as:
# Haggerty, R. (2014), CascadePlot: A Python script for generation of 
#    cascade plots and associated strip charts, 
#    https://github.com/marathanman4202/CascadePlot
#
# Python 2.7
# Dependencies & libraries that need to be installed:
#    numpy
#    matplotlib
#    xlrd
#    gspread
#  

########################################################################################
########################################################################################
########################################################################################

def project_specifications(
        rows_of_input_data_to_skip=0, annual_data='True', leap_yr='none',\
        read_date_column=False, date_column = 0
        ):
    """
    Set parameters and plot information for specific project
    
    start_year = first year of data (could be water year)
    end_year = last year of data (could be water year)
    day_of_year_start = first day of year to be plotted
    annual_data = if data are yearly.  Default = True
    leap_yr = option to treat leap-year. Default = none
    """
    import constants as cst   # constants.py contains constants used here
    start_year = 2004
    end_year = 2013
    day_of_year_start = cst.day_of_year_oct1
        
    read_date_column = True
    date_column = 0
    leap_yr = 'remove'
    
    return \
    start_year, end_year, day_of_year_start, \
    rows_of_input_data_to_skip,\
    annual_data, leap_yr, read_date_column, date_column
    

def get_labels(
        data_2D, num_yrs, data_type, metadata_txt
        ):
    """
    Provide labels, text, and titles for plotting
    """
    import datetime

    if data_type == 'default' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Text$'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Text$ [units]'
        subtitle = ''
     
    elif data_type == 'precip' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Ann \, Precip\,$ [mm]'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg \, Daily \,$ [mm]'
        subtitle = ''
                  
    elif data_type == 'meanT' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Ann\,mean\,T\,$ [$^{\circ}\mathrm{C}$]'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg\,mean\,T\,$ [$^{\circ}\mathrm{C}$]'
        subtitle = ''
                  
    elif data_type == 'minT' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Ann\,min\,T\,$ [$^{\circ}\mathrm{C}$]'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg\,min\,T\,$ [$^{\circ}\mathrm{C}$]'
        subtitle = ''
                  
    elif data_type == 'maxT' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Ann\,max\,T\,$ [$^{\circ}\mathrm{C}$]'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg\,max\,T\,$ [$^{\circ}\mathrm{C}$]'
        subtitle = ''
                  
    elif data_type == 'discharge' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Avg \, Q$ [m$^{\t{3}}$/s]'
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg \, Q$ [m$^{\t{3}}$/s]'
        subtitle = ''

    elif data_type == 'chem' :
        bottom_label = '$Month \, of \, Year$'
        right_xlabel = '$Avg \,$ '
        cascade_ylabel = '$Year$'
        bottom_ylabel = '$Avg \,$'
        subtitle = ''
                  
    else:
        print data_type, ' data_type not defined in get_labels function'
        raise Exception
    
    # Metadata for bottom right corner
    metadata_bottomright = metadata_txt +  '\n' \
          + 'HJA NSF grant DEB-0832652 and' +  '\n' \
          + 'Roy Haggerty NSF grant EAR-1417603' + '\n'\
          + 'Graph generated on ' + str(datetime.date.today()) 

    return bottom_label, right_xlabel, cascade_ylabel, bottom_ylabel, \
            subtitle, metadata_bottomright

def cascade(
            file_model_csv,             #the name of the reference file
            column,
            title,                      #the title of the graph to be generated
            graph_name_png,             #path & name of output png file
            metadata_txt,
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
    import matplotlib as mpl
    import constants as cst   # constants.py contains constants used here
    import matplotlib.gridspec as gridspec
    from   mpl_toolkits.axes_grid1 import make_axes_locatable
    from matrix_from_xls import matrix_from_xls
    
    np.set_printoptions(precision=3) 

# Set parameters and plot information for specific project:
    start_year, end_year, day_of_year_start, \
    rows_of_input_data_to_skip,\
    annual_data, leap_yr, read_date_column, date_column \
    = project_specifications()
    
    num_years = end_year - start_year + 1

#   Collect data for plotting from csv or other spreadsheet files:
    data_2D = matrix_from_xls(
            file_model_csv, column,cst.days_in_yr, 
            day_of_year_start = day_of_year_start,
            start_year = start_year,
            skip = rows_of_input_data_to_skip, 
            leap_yr = leap_yr,
            read_date_column = read_date_column, 
            date_column = date_column
            )

### UNIT CONVERSION:   
#    data_2D = data_2D*cst.cfs_to_m3 
    
    data_set_rhs = process_data_rhs( 
            data_2D, num_years, data_type, start_year, end_year 
            )
            
    data_early, data_mid, data_late = process_data_bottom(
            data_2D, num_years, data_type, start_year, end_year
            )
        
    bottom_label, right_xlabel, cascade_ylabel, bottom_ylabel, \
        subtitle, textstr  \
        = get_labels(
            data_2D, num_years, data_type, metadata_txt
            )
     
    ##########################################################
    #   Prepare the figure "canvas"                          #
    ##########################################################

    if data_type == 'default' or data_type == 'precip':
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],256)
    elif data_type == 'minT' or data_type == 'maxT' or data_type =='meanT':
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white',(0.9,0.1,0.1)],256)
    else:
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],256)
        
    fig = plt.figure(1, figsize=(10,8))
    width_ratios=[3.5, 1.7]
    height_ratios = [4., 1.5]
    wspace = 0.4     # horizontal space btwn figs
    hspace = 0.12     # vertical space btwn figs
    
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
                  extent=[day_of_year_start, 365 + day_of_year_start - 1 , start_year, end_year]) 
    month_labels(ax)
    ax.set_ylabel(cascade_ylabel, fontsize=14)
    if (end_year-start_year)/10 > 5:
        tick_sep_yrs = 10
    elif (end_year-start_year)/10 <= 5:
        tick_sep_yrs = 5
    if (end_year - start_year)<12:
        tick_sep_yrs = 1
    plt.ticklabel_format(axis='y',style='plain',useOffset=False)
    ticks=np.arange(start_year,end_year,tick_sep_yrs)
    plt.yticks(ticks, fontsize=14)
    plt.title(subtitle,fontsize=12)  # could put a subtitle above cascade plot
    plt.suptitle(title, fontsize = 18)
#    props = dict(boxstyle='round', facecolor='wheat', alpha=0.85, lw=0)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.04, aspect=20)
    plt.colorbar(p,cax=cax).set_label(bottom_ylabel)

    ##########################################################
    #   Prep the bottom strip                                #
    ##########################################################
    
    ax4 = fig.add_subplot(gs1[1,0], aspect = 'auto', sharex=ax)
    ax4.plot(range(day_of_year_start, 365 + day_of_year_start),
             data_early, color="0.62", lw=1.5)
    ax4.plot(range(day_of_year_start, 365 + day_of_year_start),
             data_mid, color="0.32", lw=1.5)
    ax4.plot(range(day_of_year_start, 365 + day_of_year_start),
             data_late, color="0.", lw=1.5)
    month_labels(ax4)
    ax4.set_xlabel(bottom_label, fontsize=14)
    ax4.set_ylabel(bottom_ylabel, fontsize=14)
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
    max_xticks = 3

    ##########################################################
    #   Prep the right-hand strip chart                      #
    ##########################################################

    ax5 = fig.add_subplot(gs2[0,1], aspect = 'auto', sharey=ax)

    xloc = plt.MaxNLocator(max_xticks)
    ax5.xaxis.set_major_locator(xloc)
    ax5.yaxis.tick_right()
    plt.yticks(ticks, fontsize=14)
    if data_type == 'default' or\
       data_type == 'precip' or\
       data_type == 'meanT' or\
       data_type == 'minT' or\
       data_type == 'maxT' or\
       data_type == 'discharge' or\
       data_type == 'chem':
        ax5.plot(data_set_rhs, range(start_year,end_year+1), color="0.35", lw=1.5)
        plt.xlabel(right_xlabel, fontsize = 14)
        
    else:
        print data_type, ' data_type not defined in bottom strip chart (ax5) area'
        raise Exception
        
    xloc = plt.MaxNLocator(max_xticks)
    ax5.xaxis.set_major_locator(xloc)
    plt.ylim(start_year,end_year)
    ax5.yaxis.tick_right()
    plt.yticks(ticks, fontsize=14)

    ###################################################################
    #   Add metadata text box in lower right, citing figure details   #
    ###################################################################
    props = dict(boxstyle='round', facecolor='white', alpha=0.5, lw=0.)

    ax4.text(1.05, -0.2, textstr, transform=ax.transAxes, fontsize=6,
            verticalalignment='top', bbox=props)
    textatr = '\n\n\n Generated with $Cascade plot$ by Roy Haggerty, 2014'
    ax4.text(1.15, -0.5, textatr, transform=ax.transAxes, fontsize=6,
            verticalalignment='top', bbox=props, alpha=0.2)

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
    data_set_rhs = np.empty([1])

    averaging_window = 3
    window_raw = np.array([])
    window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
    window = window_raw / np.sum(window_raw)  # normalized weights
    if data_type == 'default' or\
       data_type == 'discharge' or\
       data_type == 'meanT' or\
       data_type == 'chem':        
        yearly_avg = [np.mean(data_2D[i,:]) for i in range(num_yrs)]  
        yearly_avg = movingaverage(
            yearly_avg[:averaging_window] + yearly_avg + yearly_avg[-averaging_window:],
            window)[averaging_window:-averaging_window]
        data_set_rhs = yearly_avg
        
    elif data_type == 'minT':
        yearly_min = [np.min(data_2D[i,:]) for i in range(num_yrs)]  
        yearly_min = movingaverage(
            yearly_min[:averaging_window] + yearly_min + yearly_min[-averaging_window:],
            window)[averaging_window:-averaging_window]
        data_set_rhs = yearly_min
    
    elif data_type == 'maxT':      
        yearly_max = [np.max(data_2D[i,:]) for i in range(num_yrs)]  
        yearly_max = movingaverage(
            yearly_max[:averaging_window] + yearly_max + yearly_max[-averaging_window:],
            window)[averaging_window:-averaging_window]
        data_set_rhs = yearly_max
               
    elif data_type == 'precip':
        precip_sum = list(np.sum(data_2D,axis=1)) 
        precip_sum = movingaverage(
            precip_sum[:averaging_window] + precip_sum + precip_sum[-averaging_window:],
            window)[averaging_window:-averaging_window]
        data_set_rhs = precip_sum
        
    else:
        print data_type, ' data_type not defined in process_data function'
        raise Exception
        
    return data_set_rhs
    

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
    
    averaging_window = 51
    window_raw = np.array([])
    window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
    window = window_raw / np.sum(window_raw)  # normalized weights

    # Calculate moving averages (using binomial filter - in movingaverage).
    # Prepend and append half of averaging window to data window so that moving average at early
    #   and late time are correct.

    one_third = (end_year - start_year)/3
    two_thirds = 2*(end_year - start_year)/3

    data_early = movingaverage([np.mean(data_2D[0:one_third,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[0:one_third,i]) for i in range(365)] +
                               [np.mean(data_2D[0:one_third,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
    data_mid   = movingaverage([np.mean(data_2D[one_third+1:two_thirds,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[one_third+1:two_thirds,i]) for i in range(365)] +
                               [np.mean(data_2D[one_third+1:two_thirds,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
    data_late  = movingaverage([np.mean(data_2D[two_thirds+1:,i]) for i in range(365-averaging_window/2 , 364)] +
                               [np.mean(data_2D[two_thirds+1:,i]) for i in range(365)] +
                               [np.mean(data_2D[two_thirds+1:,i]) for i in range(0 , averaging_window/2)],
                               window)[averaging_window/2 : 365+averaging_window/2]
                               
    return data_early, data_mid, data_late       
    
def month_labels (axys):
    """
    Place month labels on horizontal axis.  This is a little tricky,
       so I found some code on the web and modified it.
    """
#    from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid
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

def check_if_empty(element):
    if element == '':
        return False
    else:
        return True
        
def paths(master_file):
    '''
    Reads in path data from master_file
    '''
    import xlrd
    Path_book = xlrd.open_workbook(master_file)
    Reference_path = tuple(Path_book.sheet_by_index(0).col_values(9))[7]
    write_path = tuple(Path_book.sheet_by_index(0).col_values(9))[8]
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

#import constants as cst   # constants.py contains constants used here
import xlrd
# NAME OF MASTER FILE:
master_file = 'master file.xls'
path_data, path_write = paths(master_file)

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
graph_name_v = cascade_plot_params.sheet_by_index(0).col_values(6)[1:total_number_of_plots+1]          # type of data
metadata_v = cascade_plot_params.sheet_by_index(0).col_values(7)[1:total_number_of_plots+1]            # metadata credit info

# Make the plots.
plot_number = -1
for file in file_name_list: 
    plot_number += 1
    if ToBePlotted[plot_number]:
        file_name_ToBeUsed = path_data + file_name_list[plot_number]
        graph_name = path_write + graph_name_v[plot_number]
        col_num = int(column[plot_number])
        metadata_txt = str(metadata_v[plot_number])
        cascade(
            file_name_ToBeUsed,
            col_num,
            title[plot_number],
            graph_name,
            metadata_txt,
            Display = Display_v[plot_number],
            data_type = data_type_v[plot_number],
            )
