import numpy as np
import scipy.signal


def cross_correlate(template, test):
    nsamp = len(template)
    shape = (test.size - nsamp + 1, nsamp)
    rolling = np.lib.stride_tricks.as_strided(
        test,
        shape=shape,
        strides=(test.itemsize, test.itemsize)
    )
    norm = np.sqrt(np.sum(np.square(template))) \
         * np.sqrt(np.sum(np.square(rolling), axis=1))
    cc = scipy.signal.correlate(test, template, mode='valid') / norm
    return (cc)
