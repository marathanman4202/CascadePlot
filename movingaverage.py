def n_take_k(n,k):
    """Returns (n take k),
    the binomial coefficient.

    author: https://code.google.com/p/econpy/source/browse/trunk/pytrix/pytrix.py
    """
    n, k = int(n), int(k)
    assert (0<=k<=n), "n=%f, k=%f"%(n,k)
    k = min(k,n-k)
    c = 1
    if k>0:
        for i in xrange(k):
            c *= n-i
            c //= i+1
    return c

def movingaverage(interval, window):
    """
    Calculate a moving average and return numpy array (dimension 1)
    """
    import numpy as np
    return np.convolve(interval, window, 'same')

def movingaverage_first2D(array_2D, window_size_days, window_size_yrs):
    """
    Calculate a moving average of first window_size_yrs years over
      a window of window_size_days, and return a numpy array (dimension 1)
    """
    import numpy as np
    interval = [np.average(array_2D[0:window_size_yrs,i]) for i in range(365)]
    window = np.ones(int(window_size_days))/float(window_size_days)
    return np.convolve(interval, window, 'same')
