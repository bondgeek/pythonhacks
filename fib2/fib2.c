#include <Python.h>

// function definition, returning a PyObject
//
static PyObject *
fib (PyObject *self, PyObject *args)
{
int a = 0, b = 1, c, n;

if (!PyArg_ParseTuple(args, "i", &n))
    return NULL;

PyObject *list = PyList_New(0);

while(b < n){
    PyList_Append(list, PyInt_FromLong(b));
    c = a+b;
    a = b;
    b = c;
    }

return list;
}

PyMethodDef methods[] = {
    {"fib", fib, METH_VARARGS, "Returns a fibonacci sequence"},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initfib()
{
    (void) Py_InitModule("fib", methods);
}

