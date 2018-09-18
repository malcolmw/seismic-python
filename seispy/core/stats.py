import numpy as np
import scipy
import scipy.stats


def magnitude_completeness_OK93(M, thresh=0.99, nmin=200):
    """
    Fits an exponentially-modified Gaussian distribution to vector M
    and returns the perecent-point function for a specified threshold.
    """
    if len(M) < nmin:
        return(np.nan)
    K, loc, scale = scipy.stats.exponnorm.fit(M)
    mu, sigma = loc, scale
    lamda = 1./(K*sigma)
    gaussian = scipy.stats.norm(loc=(mu+lamda*sigma**2), scale=sigma)
    # This methodology is deprecated; it underestimates Mc
    # return(scipy.stats.norm(loc=loc, scale=scale).ppf(thresh))
    return(gaussian.ppf(thresh))


def fit_fmd_OK93(M):
    """
    Returns best-fitting exponentially-modified Gaussian distribution
    for vector M.
    """
    return(scipy.stats.exponnorm(*scipy.stats.exponnorm.fit(M)))
