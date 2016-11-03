#include <Python.h>
#include <float.h>
#include <vector>
#include <stdlib.h>

static PyObject *
grid_search(PyObject *self, PyObject *args)
{
    PyObject* locator;
    PyObject* origin;
    PyObject* grid;
    PyObject* arrivals;
    int ir0 = -1;
    int itheta0 = -1;
    int iphi0 = -1;
    int r_lb, r_ub, theta_lb, theta_ub, phi_lb, phi_ub;
    int r_range, theta_range, phi_range;
    int r_stride, theta_stride, phi_stride;
    int nr, ntheta, nphi;
    int i, ir, itheta, iphi, iarr;
    int narr;
    double best_fit = 999999.9;
    double tt;
    double ot;
    double misfit;
    double r;
    double t0 = -1.0;
    std::vector<double> arrival_times;
    std::vector<double> travel_times;
    std::vector<double> origin_times;
    std::vector<double> residuals;
    bool last_iteration = false;

    if ( !PyArg_ParseTuple(args, "OO",
                                  &locator,
                                  &origin) )
        return NULL;
    grid = PyObject_GetAttrString(locator, "grid");
    nr = (int) PyInt_AsLong(PyDict_GetItemString(grid, "nr"));
    ntheta = (int) PyInt_AsLong(PyDict_GetItemString(grid, "ntheta"));
    nphi = (int) PyInt_AsLong(PyDict_GetItemString(grid, "nphi"));
    arrivals = PyObject_GetAttrString(origin, "arrivals");
    narr = (int) PyTuple_Size(arrivals);
    for (iarr = 0; iarr < narr; iarr++){
        arrival_times.push_back(
           PyFloat_AsDouble(
              PyObject_GetAttrString(
                 PyObject_GetAttrString(
                    PyTuple_GetItem(arrivals, iarr),
                    "time"),
                 "timestamp"
              )
           )
        );
    }
    r_lb = 0;
    r_ub = nr;
    r_stride = 2;
    theta_lb = 0;
    theta_ub = ntheta;
    theta_stride = 8;
    phi_lb = 0;
    phi_ub = nphi;
    phi_stride = 8;
    while (true){
        for (ir = r_lb; ir < r_ub; ir += r_stride){
            for (itheta = theta_lb; itheta < theta_ub; itheta += theta_stride){
                for (iphi = phi_lb; iphi < phi_ub; iphi += phi_stride){
                    travel_times.clear();
                    origin_times.clear();
                    residuals.clear();
                    for (iarr = 0; iarr < narr; iarr++){
                        tt = PyFloat_AsDouble(
                                PyObject_CallMethod(locator,
                                                    "_get_node_tt",
                                                    "Oiii",
                                                    PyTuple_GetItem(arrivals, iarr),
                                                    ir,
                                                    itheta,
                                                    iphi
                                )
                             );
                        travel_times.push_back(tt);
                        origin_times.push_back(arrival_times[iarr] - tt);
                    }
                    ot = 0.0;
                    for (i = 0; i < (int) origin_times.size(); i++){
                        ot += origin_times[i];
                    }
                    ot /= origin_times.size();
                    for (i = 0; i < (int) narr; i++){
                        r = arrival_times[i] -(ot + travel_times[i]);
                        r = (r > 0) ? r : -r;
                        residuals.push_back(r);
                    }
                    misfit = 0.0;
                    for (i = 0; i < residuals.size(); i++){
                        misfit += residuals[i];
                    }
                    if (misfit < best_fit){
                        best_fit = misfit;
                        ir0 = ir;
                        itheta0 = itheta;
                        iphi0 = iphi;
                        t0 = ot;
                    }
                }
            }
        }
        if (r_stride == 1 && theta_stride == 1 && phi_stride == 1){
            if (last_iteration){break;}
            last_iteration = true;
            r_lb = (0 > (ir0 - 10)) ? 0 : (ir0 - 10);
            r_ub = (nr < (ir0 + 10)) ? nr : (ir0 + 10);
            theta_lb = (0 > (itheta0 - 10)) ? 0 : (itheta0 - 10);
            theta_ub = (ntheta < (itheta0 + 10)) ? ntheta : (itheta0 + 10);
            phi_lb = (0 > (iphi0 - 10)) ? 0 : (iphi0 - 10);
            phi_ub = (nphi < (iphi0 + 10)) ? nphi : (iphi0 + 10);
        }
        r_stride = (r_stride / 2 > 0) ? r_stride / 2 : 1;
        theta_stride = (theta_stride / 2 > 0) ? theta_stride / 2    : 1;
        phi_stride = (phi_stride / 2 > 0) ? phi_stride / 2 : 1;
        r_range = (r_ub - r_lb) / 4;
        theta_range = (theta_ub - theta_lb) / 4;
        phi_range = (phi_ub - phi_lb) / 4;
        r_lb = (0 > (ir0 - r_range)) ? 0 : (ir0 - r_range);
        r_ub = (nr < (ir0 + r_range)) ? nr : (ir0 + r_range);
        theta_lb = (0 > (itheta0 - theta_range)) ? 0 : (itheta0 - theta_range);
        theta_ub = (ntheta < (itheta0 + theta_range)) ? ntheta : (itheta0 + theta_range);
        phi_lb = (0 > (iphi0 - phi_range)) ? 0 : (iphi0 - phi_range);
        phi_ub = (nphi < (iphi0 + phi_range)) ? nphi : (iphi0 + phi_range);
    }
    Py_DECREF(grid);
    return Py_BuildValue("iiif", ir0, itheta0, iphi0, t0);
}

static PyMethodDef AccelerateModuleMethods[] = {
    {"grid_search", (PyCFunction)grid_search, METH_VARARGS | METH_KEYWORDS,
     "This is a grid search function."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initaccelerate(void)
{
    (void) Py_InitModule("accelerate", AccelerateModuleMethods);
}