#!/usr/bin/env python

# -----------------------------------------------------------------------------
#  Copyright (C) 2012 Bradley Froehle

#  Distributed under the terms of the GNU General Public License. You should
#  have received a copy of the license along with this program. If not,
#  see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

from setuptools import Extension, setup
from pathlib import Path
import numpy as np
from numpy.distutils import system_info

# distmesh._distance_functions needs LAPACK
lapack_info = system_info.get_info("lapack_opt", 0)
# See ('https://github.com/nipy/nipy/blob/'
#      '91fddffbae25a5ca3a5b35db2a7c605b8db9014d/nipy/labs/setup.py#L44')
if "libraries" not in lapack_info:
    lapack_info = system_info.get_info("lapack", 0)

# ext_modules[0].libraries.extend(lapack_info["libraries"])
# ext_modules[0].library_dirs.extend(lapack_info["library_dirs"])
if "include_dirs" in lapack_info:
    lapack_inc = lapack_info["include_dirs"]
else:
    lapack_inc = []

print("Lapack libraries are : {}".format(lapack_info["libraries"]))
print("Lapack library dirs are : {}".format(lapack_info["library_dirs"]))

# Build list of cython extensions
setup(
    ext_modules=[
        Extension(
            name="distmesh._distance_functions",
            sources=[str(Path("distmesh", "_distance_functions.pyx"))],
            depends=[Path("distmesh", "src", "distance_functions.c")],
            include_dirs=[np.get_include()] + lapack_inc,
            libraries=lapack_info["libraries"],
            library_dirs=lapack_info["library_dirs"],
        ),
    ]
)
