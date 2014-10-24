def matrix_from_xls(file_w_path,column,xcycle,skip,filetype='csv'):
    """
    Reads sheet (excel, google, csv) file and produces 2-D matrix
    Returns 2D numpy array
    
    file_w_path = filename and location of file. If google sheet, then key
    column = column number for data
    xcycle = how many numbers in each row
    skip = how many numbers to skip before starting to read data
    filetype = type of file
    """
    import numpy as np
    import xlrd
    
    if filetype != 'gsheet':  # unless it is a google sheet, get filetype from windows extension
        filetype = file_w_path.rsplit('.')[-1]

    if filetype == 'csv':
        data_tmp = np.array(np.genfromtxt(file_w_path, delimiter=',',skip_header=1)) # Read csv file
        data_yr_tmp = data_tmp[:,column]
    elif filetype == 'xls':
        workbook = xlrd.open_workbook(file_w_path)
        # get 0th sheet, column, starting at 1st fow
        sheetnum = 0
        rowstart = 1
        data_yr_tmp = np.array(workbook.sheet_by_index(sheetnum).col_values(column)[rowstart:])
    elif filetype == 'gsheet':
        import imp
        import sys
        sys.path.append('c:\\code\\gspread\\')  # location of gspread module
        import gspread  # gspread is available at https://github.com/burnash/gspread
        ui = imp.load_source('userinfo', 'C:\\keys\\userinfo.py')
        gc = gspread.login(ui.userid,ui.pw)
        sheet = gc.open_by_key(file_w_path).sheet1
        data_str = np.array(sheet.get_all_values())
        data_yr_tmp = data_str[1:,column].astype(np.float)

    numdat = len(data_yr_tmp)
    data_yr = data_yr_tmp[skip:-((numdat-skip)%xcycle)] # start at skip + 1 and go as close to end of data as possible
    data_2D = np.reshape(np.array(data_yr), (-1,xcycle)) #2D matrix of data in numpy format
    
    
    return data_2D
