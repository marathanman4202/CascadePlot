def matrix_from_xls(
    file_w_path,
    column = 0,
    xcycle = 365,
    day_of_year_start=1, 
    skip=0,
    filetype='csv',
    data_type='annual', 
    leap_yr='none', 
    read_date_column=False, 
    date_column=0,
    movingaveragevec='none',
    missing_data_flag='none'
    ):
    #Roy Haggerty, 2014
    """Reads timeseries sheet (csv, xls/xlsx, google). Returns 2-D numpy array.
    
    If using google sheet, use filetype == 'gsheet'. Make sure gspread is
    within your path.
    Need to add gspread from github, and import username and password.
    
    file_w_path -- (str) filename including path of file. If google sheet, then key.
    
    keyword arguments:
    column -- (int) column number for data (default 0)
    xcycle -- (int) how many numbers in each row (default 365)
    day_of_year_start -- (int) for a timeseries, day of year start of 2D array (default 1)
    skip -- (int) how many numbers to skip before using data (default 0)
    filetype -- (str) type of file csv, xls, gsheet. (default csv)
    data_type -- (str) type of data annual, daily (default annual)
    leap_yr -- (str) how to deal with leap years, none or remove (default none)
    read_date_column -- (bool) data contain date col True or False (default False)
    date_column -- (int) column where dates are found (default 0)
    missing_data_flag -- integer flag that identifies missing or bad data (default none)
    """
    
    import numpy as np
    import xlrd
    import pandas as pd
    from movingaverage import movingaverage
    
    if read_date_column:
        data_col_num = column - 1
    
    if filetype != 'gsheet':  # unless it is a google sheet, get filetype from windows extension
        filetype = file_w_path.rsplit('.')[-1]

    if filetype == 'csv':
        if read_date_column:
            df = pd.read_csv(file_w_path, index_col=date_column, parse_dates=[date_column])
            df = df.convert_objects(convert_numeric=True)
            df.index  = pd.to_datetime(df.index.date)  #convert to Timestamp, set time to 00
            ts = pd.Series(df.iloc[:,data_col_num],df.index)
            start_date, start_year, end_year \
                        = start_end_info(ts, skip=skip, \
                          day_of_year_start=day_of_year_start, xcycle=xcycle)
            data_yr_tmp = timeseries(ts,leap_yr=leap_yr,missing_data='bfill',
                        start_date = start_date, missing_data_flag = missing_data_flag)
            if movingaveragevec != 'none':
                data_yr_tmp = movingaverage(data_yr_tmp, movingaveragevec) 
            return start_year, end_year, data_2D(data_yr_tmp,skip,xcycle)
        else:
            data_tmp = np.array(np.genfromtxt(file_w_path, delimiter=',',skip_header=1)) # Read csv file
            data_yr_tmp = data_tmp[:,column]
            return data_2D(data_yr_tmp,skip,xcycle)
    elif filetype == 'xls':
        workbook = xlrd.open_workbook(file_w_path)
        # get 0th sheet, column, starting at 1st row
        sheetnum = 0
        rowstart = 1
        if read_date_column:
            df = pd.read_excel(file_w_path, sheetname=sheetnum, header=rowstart-1, index_col=date_column)
            df = df.convert_objects(convert_numeric=True)
            df.index  = pd.to_datetime(df.index.date) #convert to Timestamp, set time to 00
            ts = pd.Series(df.iloc[:,data_col_num],df.index)
            start_date, start_year, end_year \
                        = start_end_info(ts, skip=skip, \
                          day_of_year_start=day_of_year_start, xcycle=xcycle)
            data_yr_tmp = timeseries(ts,leap_yr=leap_yr,missing_data='bfill',
                        start_date = start_date, missing_data_flag = missing_data_flag)
            return start_year, end_year, data_2D(data_yr_tmp,skip,xcycle)
        else:
            data_yr_tmp = np.array(workbook.sheet_by_index(sheetnum).col_values(column)[rowstart:])
            return data_2D(data_yr_tmp,skip,xcycle)
    elif filetype == 'gsheet':
        import imp
        try:
            import gspread  # gspread is available at https://github.com/burnash/gspread
            ui = imp.load_source('userinfo', 'C:\\keys\\userinfo.py')
            gc = gspread.login(ui.userid,ui.pw)
            sheet = gc.open_by_key(file_w_path).sheet1
            if read_date_column:
                data_str = np.array(sheet.get_all_values())
                dates = data_str[1:,date_column].astype(str)
                df = pd.DataFrame(data_str[1:,date_column+1:],index=pd.to_datetime(dates))
                df = df.convert_objects(convert_numeric=True)
                print df.head()
                print df.index
                print data_col_num
                ts = pd.Series(df.iloc[:,data_col_num],df.index)
                data_yr_tmp = timeseries(ts,leap_yr=leap_yr,missing_data='bfill',
                            start_date = start_date, missing_data_flag = missing_data_flag)
                return start_year, end_year, data_2D(data_yr_tmp,skip,xcycle)
            else:
                data_str = np.array(sheet.get_all_values())
                data_yr_tmp = data_str[1:,column].astype(np.float)
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

def start_end_info(ts, skip=0, day_of_year_start=1, xcycle=365):
    """From pandas timeseries, return start_date, start_year, end_year
    
    ts -- pandas timeseries with Timestamp and data
    
    keyword arguments:
    xcycle -- how many numbers in each row (default 365)
    day_of_year_start -- for a timeseries, day of year start of 2D array (default 1)
    skip -- how many numbers to skip before using data (default 0)    
    
    """
    import pandas as pd
    import datetime as dt
    import constants as cst
    
    try:
        assert day_of_year_start == 1 or skip == 0
    except AssertionError:
        print 'either skip must = 0 or day_of_year_start must = 1'
        raise AssertionError()
    else:
        first_day = ts.index[0].dayofyear
        if day_of_year_start + skip < first_day:
            start_year = ts.index[0].year + 2
            start_date = pd.to_datetime(dt.datetime(start_year-1, 1, 1) + dt.timedelta(day_of_year_start - 1 + skip))
        else:
            start_year = ts.index[0].year + 1
            start_date = pd.to_datetime(dt.datetime(start_year-1, 1, 1) + dt.timedelta(day_of_year_start - 1 + skip)) ##CAREFUL HERE.  For some apps, the start_year could be start_year without subtraction of 1
    
        # fill dates for purpose of calculating num_years. tstmp contains all of the dates
        try:
           tstmp = ts.reindex(pd.date_range(ts.index[0], ts.index[-1]),method='pad')  # if there are any missing days, this will catch them
        except ValueError:
            tstmp = ts
        # need to count the damned leap years        
        leapdays=[pd.datetime(i,2,29) for i in range(1904,2017,4)] #list of leap days
        tsLD=tstmp[tstmp.index.isin(leapdays)]
        num_LD = len(tsLD)  # num of leap days
        num_years = \
            int(((tstmp[start_date:].index[-1] - tstmp[start_date:].index[0]).days-num_LD+1)/cst.days_in_yr) - 1
        end_year = start_year + num_years
           
        return start_date, start_year, end_year
        
    return start_date, start_year, end_year
    
def data_2D(data_yr_tmp,skip,xcycle):
    """ Convert column of numbers to 2D matrix
    """
    import numpy as np
        
    numdat = len(data_yr_tmp)
    if (numdat-skip)%xcycle == 0:
        data_yr = data_yr_tmp[skip:] # start at skip + 1 and go as close to end of data as possible
    else:   
        data_yr = data_yr_tmp[skip:-((numdat-skip)%xcycle)] # start at skip + 1 and go as close to end of data as possible
    data_2D = np.reshape(np.array(data_yr), (-1,xcycle)) #2D matrix of data in numpy format
    return data_2D
    
def timeseries(ts,leap_yr='none',missing_data='pad', start_date = 'none', missing_data_flag = 'none'):
    """Deal with leap years and data gaps.
    
    ts = pandas timeseries data indexed with timestamp
    leap_yr = database has leap years to deal with. Options are 'remove'
    missing_data = database has mssing data.  Options are same as methods for pandas.Series.fillna
    missing_data_flag -- integer flag for missing data
    """
    import numpy as np
    import pandas as pd
    
    try:
    #    ts = ts.reindex(pd.date_range(ts.index[0]-pd.offsets.Day(21), ts.index[-1]),method='pad')
        ts = ts.reindex(pd.date_range(ts.index[0], ts.index[-1]),method='pad')  # if there are any missing days, this will catch them
    except ValueError:
        pass
    
    if leap_yr == 'none':
        pass
    elif leap_yr == 'remove':
        leapdays=[pd.datetime(i,2,29) for i in range(1904,2017,4)] #list of leap days
        tsLD=ts[ts.index.isin(leapdays)]
        if tsLD.empty is False: 
            ts = ts[ts.index - tsLD.index]
            try:
                ts = ts[ts.index - tsLD.index]
            except ValueError:
                print '************'
                print '  A common cause of this error is duplicate date stamps'
                print '  in the data file.'
                print '************'
                raise ValueError('cannot reindex from a duplicate axis')
    else:
        print 'leap_yr contains unknown option'
        raise Exception()
    if missing_data != 'none':  ts = ts.replace(missing_data_flag,np.nan) # replace missing data with NaN
    ts = ts.fillna(method=missing_data)
    if start_date != 'none':
        ts = ts.loc[start_date:]
    data_yr_tmp = np.array(ts)
    
    return data_yr_tmp
    
