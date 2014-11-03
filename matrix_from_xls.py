def matrix_from_xls(
    file_w_path,
    column,
    xcycle,
    day_of_year_start=1, 
    start_year = 2000,
    skip=0,
    filetype='csv',
    data_type='annual', 
    leap_yr='none', 
    read_date_column=False, 
    date_column=0):
    #Roy Haggerty, 2014
    """
    Reads sheet (excel, google, csv) file and produces 2-D matrix
    Returns 2D numpy array
    
    If using google sheet, use filetype == 'gsheet'. Make sure gspread is
    within your path.
    Need to add gspread from github, and import username and password.
    
    file_w_path = filename and location of file. If google sheet, then key
    column = column number for data
    xcycle = how many numbers in each row
    skip = how many numbers to skip before starting to read data
    filetype = type of file (kwarg). Default is csv.
    leap_yr = database has leap years to deal with.  Options are 'remove'.
    """
    
    import numpy as np
    import xlrd
    import pandas as pd
    import datetime as dt
    
    try:
        assert day_of_year_start == 1 or skip == 0
    except AssertionError:
        print 'either skip must = 0 or day_of_year_start must = 1'
        raise AssertionError()
    else:
        if day_of_year_start == 1:
            skip_rows_by_date = False
            start_date = start_date = dt.datetime(start_year-1, 1, 1) ##CAREFUL HERE.  For some apps, the start_year could be start_year without subtraction of 1
        else:
            skip_rows_by_date = True
            start_date = dt.datetime(start_year-1, 1, 1) + dt.timedelta(day_of_year_start - 1) ##CAREFUL HERE.  For some apps, the start_year could be start_year without subtraction of 1
    
    if read_date_column:
        data_col_num = column - date_column - 1
    
    if filetype != 'gsheet':  # unless it is a google sheet, get filetype from windows extension
        filetype = file_w_path.rsplit('.')[-1]

    if filetype == 'csv':
        if read_date_column:
            df = pd.read_csv(file_w_path, index_col=date_column, parse_dates=[date_column])
            df = df.convert_objects(convert_numeric=True)
            ts = pd.Series(df.iloc[:,data_col_num],df.index)
            data_yr_tmp = timeseries(ts,leap_yr=leap_yr,missing_data='bfill',
                        skip_rows_by_date = skip_rows_by_date,
                        start_date = start_date)
        else:
            data_tmp = np.array(np.genfromtxt(file_w_path, delimiter=',',skip_header=1)) # Read csv file
            data_yr_tmp = data_tmp[:,column]
        return data_2D(data_yr_tmp,skip,xcycle)
    elif filetype == 'xls':
        workbook = xlrd.open_workbook(file_w_path)
        # get 0th sheet, column, starting at 1st fow
        sheetnum = 0
        rowstart = 1
        data_yr_tmp = np.array(workbook.sheet_by_index(sheetnum).col_values(column)[rowstart:])
        if read_date_column:
            dates = np.array(workbook.sheet_by_index(sheetnum).col_values(date_column)[rowstart:])
            return data_2D(data_yr_tmp,skip,xcycle)
        else:
            pass
        return data_2D(data_yr_tmp,skip,xcycle)
    elif filetype == 'gsheet':
        import imp
        try:
            import gspread  # gspread is available at https://github.com/burnash/gspread
            ui = imp.load_source('userinfo', 'C:\\keys\\userinfo.py')
            gc = gspread.login(ui.userid,ui.pw)
            sheet = gc.open_by_key(file_w_path).sheet1
            data_str = np.array(sheet.get_all_values())
            data_yr_tmp = data_str[1:,column].astype(np.float)
            if read_date_column:
                dates = data_str[1:,date_column].astype(str)
            else:
                pass
            return data_2D(data_yr_tmp,skip,xcycle)
        except ImportError:
            print '\nGSPREAD library is not available.'
            print 'make sure gspread is loaded and placed in the path'
            print 'see gspread docs at https://github.com/burnash/gspread\n'
            raise ImportError()
        except gspread.exceptions.SpreadsheetNotFound:
            print '\nGOOGLE sheet not found'
            print 'check google key\n'
            raise gspread.exceptions.SpreadsheetNotFound()
        except gspread.exceptions.AuthenticationError:
            print '\nLOGIN to google failed. Make sure your username'
            print 'and password are correctly provided.\n'
            raise gspread.exceptions.AuthenticationError()
        except IndexError:
            print '\nSOMETHING appears to be wrong with spreadsheet or requested column\n'
            raise IndexError()
        except ValueError:
            print '\nEXPECTING float in spreadsheet but found other variable type\n'
            raise ValueError(float)
        except:
            print 'unknown error importing gspread module or reading data'
            raise Exception()
        else:
            return data_2D(data_yr_tmp,skip,xcycle)  # Not sure if this is needed here

def data_2D(data_yr_tmp,skip,xcycle):
    """
    Convert column of numbers to 2D matrix
    """
    import numpy as np
        
    numdat = len(data_yr_tmp)
    if (numdat-skip)%xcycle == 0:
        data_yr = data_yr_tmp[skip:] # start at skip + 1 and go as close to end of data as possible
    else:   
        data_yr = data_yr_tmp[skip:-((numdat-skip)%xcycle)] # start at skip + 1 and go as close to end of data as possible
    data_2D = np.reshape(np.array(data_yr), (-1,xcycle)) #2D matrix of data in numpy format
    return data_2D
    
def timeseries(ts,leap_yr='none',missing_data='pad',
               skip_rows_by_date = False, start_date = 'none'):
    """
    Deal with leap years and data gaps.
    
    ts = pandas timeseries data indexed with timestamp
    leap_yr = database has leap years to deal with. Options are 'remove'
    missing_data = database has mssing data.  Options are same as methods for pandas.Series.fillna
    """
    import numpy as np
    import pandas as pd
    
    ts = ts.reindex(pd.date_range(ts.index[0]-pd.offsets.Day(21), ts.index[-1]),method='pad')
    
    if leap_yr == 'none':
        pass
    elif leap_yr == 'remove':
        leapdays=leapdays=[pd.datetime(i,2,29) for i in range(1904,2017,4)] #list of leap days
        tsLD=ts[ts.index.isin(leapdays)]
        if tsLD.empty is False: 
            ts = ts[ts.index - tsLD.index]
    else:
        print 'leap_yr contains unknown option'
        raise Exception()
    ts = ts.fillna(method=missing_data)
    if start_date != 'none':
        ts = ts[start_date:]
    data_yr_tmp = np.array(ts)
    
    return data_yr_tmp