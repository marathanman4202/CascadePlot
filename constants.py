# constants.py
"""
File containing constants to be used in various WW2100 graphics scripts.
"""
import datetime
import math

day_of_year_apr1 = 91
day_of_year_oct1 = 274
day_of_year_aug15 = 227
Jan1_1900 = datetime.date(1900,1,1)
Jan1_2010 = datetime.date(2010,1,1)
cfs_to_m3 = 0.0283168   #Cubic feet per second to cubic meters per second
F_to_C = 1.0/1.8        #Fahrenheit to Celcius
in_to_mm = 25.4         #Inches to milimeters
acft_to_m3 = 1233.48
acftperday_to_m3s = acft_to_m3/86400.
Willamette_Basin_area = 29728.*1.e6  # m2
Willamette_Basin_area_at_PDX = 11200.*math.pow(5280.*.3048,2) #11200 sq mi @ PDX
seconds_in_yr = 86400.*365.25

def paths():
    import xlrd
    Path_book = xlrd.open_workbook('master file.xls')
    Reference_path = tuple(Path_book.sheet_by_index(0).col_values(14))[7]
    Auxilliary_path = tuple(Path_book.sheet_by_index(0).col_values(14))[8]
    write_path = tuple(Path_book.sheet_by_index(0).col_values(14))[9]
    return Reference_path, Auxilliary_path, write_path

path_data, path_auxilliary_files, path_write = paths()
import metadata
