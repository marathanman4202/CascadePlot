def compare_rows(a,row):
    """take numpy array a and compare to row row
    Return new numpy array of same size as a containing 0's and 1's
    0's indicate element of a was greater than corresponding element of row
    1's indicate element of a was less than corresponding element of row"""

    import numpy as np
    from scipy import stats
    
    (number_rows,number_cols) = np.shape(a)
    
    b = np.zeros_like(a)
    for i in range(number_rows):
        b[i,:] = a[i,:] - row[:]
    b = stats.threshold(b, threshmin=0, newval=-1)
    b = stats.threshold(b, threshmax=0, newval=0)
    b = -1*b
    return b