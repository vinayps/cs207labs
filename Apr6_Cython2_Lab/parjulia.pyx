#distutils: extra_compile_args = -fopenmp
#distutils: extra_link_args = -fopenmp
#%%cython --annotate
cimport cython
import numpy as np
cimport numpy as np
from cython.parallel cimport prange

cdef inline double norm2(double complex z) nogil:
    return z.real*z.real + z.imag*z.imag

cdef int escape(int maxiter, double complex z, double complex c) nogil:
    cdef int n=0
    while n < maxiter and norm2(z) < 4:
        z=z*z+c
        n+=1
    return n

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef run_cython_amalgamated2(int gridsize, box, double complex c, int maxiter):
    #your code here
    cdef float xstep = (box.x2 - box.x1)/(gridsize - 1.0)
    cdef float ystep = (box.y2 - box.y1)/(gridsize - 1.0)
    cdef float xstart = box.x1
    cdef float ystart = box.y1
    cdef double complex[:] zs = np.empty(gridsize*gridsize, dtype=complex)
    cdef int[:] output = np.empty(gridsize*gridsize, dtype=np.int32)
    cdef int i = 0
    cdef int j = 0
    cdef double x, y
    for i in prange(gridsize, nogil=True,
                    schedule='static', chunksize=1):
        x = xstart + i*xstep
        for j in range(gridsize):
            y = ystart + i*ystep
            zs[i] = x + i*y
            output[i] = escape(maxiter, zs[i], c)  
            i = i + 1
    return zs, output

    