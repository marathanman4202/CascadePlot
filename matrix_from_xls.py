def matrix_from_xls(file_w_path,column,xcycle,skip,filetype='csv'):
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
    """
    
    import numpy as np
    import xlrd
    
    if filetype != 'gsheet':  # unless it is a google sheet, get filetype from windows extension
        filetype = file_w_path.rsplit('.')[-1]

    if filetype == 'csv':
        data_tmp = np.array(np.genfromtxt(file_w_path, delimiter=',',skip_header=1)) # Read csv file
        data_yr_tmp = data_tmp[:,column]
        return data_2D(data_yr_tmp,skip,xcycle)
    elif filetype == 'xls':
        workbook = xlrd.open_workbook(file_w_path)
        # get 0th sheet, column, starting at 1st fow
        sheetnum = 0
        rowstart = 1
        data_yr_tmp = np.array(workbook.sheet_by_index(sheetnum).col_values(column)[rowstart:])
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
            return data_2D(data_yr_tmp,skip,xcycle)

def data_2D(data_yr_tmp,skip,xcycle):
    """
    Convert column of numbers to 2D matrix
    """
    import numpy as np
    numdat = len(data_yr_tmp)
    if ((numdat-skip)%xcycle + 1) == 1:
        data_yr = data_yr_tmp[skip:] # start at skip + 1 and go as close to end of data as possible
    else:   
        data_yr = data_yr_tmp[skip:-((numdat-skip)%xcycle + 1)] # start at skip + 1 and go as close to end of data as possible
    print -((numdat-skip)%xcycle + 1)
    data_2D = np.reshape(np.array(data_yr), (-1,xcycle)) #2D matrix of data in numpy format
    return data_2D
    