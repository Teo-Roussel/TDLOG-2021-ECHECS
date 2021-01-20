#include <pybind11/embed.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/stl_bind.h>

#include <functional>
#include <iostream>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>
#include <vector>

PYBIND11_MAKE_OPAQUE(std::vector<int>);

#include <engine.h>
#include <piece.h>
#include <damier.h>

int main()
{  
    return 0;
}
