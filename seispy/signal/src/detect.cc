#include <iostream>
#include <vector>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <Eigen/Dense>
#include <Eigen/Eigenvalues>
#include "picker.h"
#include "Python.h"
#include "numpy/arrayobject.h"

using std::vector;

//static inline double square (double x) { return x*x; }

void PyArrayToVector (PyArrayObject* arr, vector<double>& out, int n) {
    int i;
    double* p;
    out.resize(n);
    for (i = 0; i < n; i++) {
        p = (double*) PyArray_GETPTR1(arr, i);
        out[i] = *p;
    }
    return;
}

static PyObject* ppick (PyObject *dummy, PyObject *args)
{
  // Python wrapper declarations
  PyObject *arg1=NULL;
  PyArrayObject *PZ=NULL, *snr_out=NULL;
  double dt, sta, lta, k_len;

  if (!PyArg_ParseTuple(args, "Odddd", &arg1, &dt, &sta, &lta, &k_len))
  {
    return NULL;
  }
  PZ = (PyArrayObject*)PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
  if (PZ == NULL) return NULL;

  int n_sta(int(sta/dt)), n_lta(int(lta/dt));

  // Find the number of elements in the spectrum
  npy_intp *nz = PyArray_DIMS(PZ);

  // Various output related definitions for Python wrapper
  vector<double> Z;
  PyArrayToVector(PZ, Z, *nz);
  
  // Calculate STA/LTA and try to find correct trigger window
  vector<double> snr = lstalta(Z, n_sta, n_lta);
  int start, stop;
  double peak_snr;
  trigger(snr, 5.0, 2.5, 1.0, dt, start, stop, peak_snr);
  int p_pick;
  if (start == -1 || stop == -1)
  {
    p_pick = -1;
  }
  else
  {
    p_pick = start;
  }

  // Window around trial P-pick to refine through k-rate
  if (p_pick > 0)
  {
    start = p_pick - int(1.0/dt);
    stop = p_pick + int(1.0/dt);
    if (stop > snr.size()) stop = snr.size()-1;
    vector<double>::iterator it = snr.begin();
    p_pick = std::distance(it, std::max_element(it+start, it+stop));

    vector<double> kurt = kurtosis(Z, int(k_len/dt));
    start = p_pick - int(0.25/dt); 
    it = kurt.begin() + start; 
    it = max_element(it, it+int(0.25/dt)); 
    p_pick = std::distance(kurt.begin(), it);
  }
 
  // Prepare python output
  
  snr_out = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);
  double *ptr;
  for (int i = 0; i < *nz; i++)
  {
    ptr = (double*)PyArray_GETPTR1(snr_out, i);
    *ptr = snr[i];
  }
  Py_INCREF(snr_out);
  
  Py_DECREF(PZ);
  //return Py_BuildValue("fff", 0, 0, 0);
  return Py_BuildValue("ffO", p_pick*dt, peak_snr, snr_out);

}

static PyObject* detect_swave_cc (PyObject *dummy, PyObject *args)
{
    double s1_pick, s2_pick, snr_s1, snr_s2, dt, cov_len, k_len, sta, lta;
    double p_pick_dbl;
    int i, p_pick;
    vector<double> N, E, Z;

    // Python wrapper declarations
    PyObject *arg1=NULL, *arg2=NULL, *arg3=NULL;
    PyArrayObject *PZ=NULL, *PN=NULL, *PE=NULL;
    PyArrayObject *filter, *K1, *K2, *S1, *S2, *SZ;

    if (!PyArg_ParseTuple(args, "OOOdddddd", &arg1, &arg2, &arg3, &dt, &cov_len,
                          &k_len, &sta, &lta, &p_pick_dbl))
    {
        return NULL;
    }
    PZ = (PyArrayObject*)PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_IN_ARRAY);
    if (PZ == NULL) return NULL;
    PN = (PyArrayObject*)PyArray_FROM_OTF(arg2, NPY_DOUBLE, NPY_IN_ARRAY);
    if (PN == NULL) return NULL;
    PE = (PyArrayObject*)PyArray_FROM_OTF(arg3, NPY_DOUBLE, NPY_IN_ARRAY);
    if (PE == NULL) return NULL;

    p_pick = int(p_pick_dbl/dt);

    // Various output related definitions for Python wrapper
    // Find the number of elements in the spectrum
    npy_intp *nz = PyArray_DIMS(PZ);
    npy_intp *nn = PyArray_DIMS(PN);
    npy_intp *ne = PyArray_DIMS(PE);
    PyArrayToVector(PZ, Z, *nz);
    PyArrayToVector(PN, N, *nn);
    PyArrayToVector(PE, E, *ne);

    // Check that all three traces are the same length
    if ((*nz != *ne) || (*nz != *nn) || (*ne != *nn)) return NULL;
    int w_len = int(cov_len/dt);
    if (w_len > *nz) return NULL;
    vector<double> pol_fltr, cftK1(*nz), cftK2(*nz), cftS1(*nz), cftS2(*nz);

    // Begin picking algorithm & calculate polarization filter
    Polarizer polar_fltr(cov_len, dt);
    pol_fltr = polar_fltr.filter(Z, N, E);

    // Attempt to pick S-waves on both horizontals
    ShearPicker SPicker(dt, k_len, sta, lta, 5.0, 2.5, 2, p_pick, pol_fltr);
    SPicker.pick(N, s1_pick, snr_s1);
    cftS1 = SPicker.get_cftS();
    cftK1 = SPicker.get_cftK();
    SPicker.pick(E, s2_pick, snr_s2);
    cftS2 = SPicker.get_cftS();
    cftK2 = SPicker.get_cftK();

    filter = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);
    K1 = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);
    K2 = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);
    S1 = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);
    S2 = (PyArrayObject*) PyArray_SimpleNew(1, nz, NPY_DOUBLE);

    PyArray_FILLWBYTE(K1, 0);
    PyArray_FILLWBYTE(K2, 0);
    PyArray_FILLWBYTE(S1, 0);
    PyArray_FILLWBYTE(S2, 0);
    double *ptr;
    for (i = 0; i < *nz; i++) {
        ptr = (double*)PyArray_GETPTR1(K1, i);
        *ptr = cftK1[i];
        ptr = (double*)PyArray_GETPTR1(K2, i);
        *ptr = cftK2[i];
        ptr = (double*)PyArray_GETPTR1(S1, i);
        *ptr = cftS1[i];
        ptr = (double*)PyArray_GETPTR1(S2, i);
        *ptr = cftS2[i];
    }
    Py_INCREF(filter);
    Py_INCREF(K1);
    Py_INCREF(K2);
    Py_INCREF(S1);
    Py_INCREF(S2);
    Py_DECREF(PZ);
    Py_DECREF(PN);
    Py_DECREF(PE);

    return Py_BuildValue("ffffOOOO", s1_pick, s2_pick, snr_s1, snr_s2,
                         S1, S2, K1, K2);
}

static struct PyMethodDef methods[] =
{
    {"detect_swave_cc", detect_swave_cc, METH_VARARGS, "Polarization filters recursively"},
    {"ppick", ppick, METH_VARARGS, "Polarization filters recursively"},
    {NULL}
};


PyMODINIT_FUNC initdetect (void)
{
    (void)Py_InitModule("detect", methods);
    import_array();
}
