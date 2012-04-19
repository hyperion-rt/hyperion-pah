import glob
import os

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

np.seterr(all='ignore')

from hyperion.dust import TTsreDust

for dustfile in glob.glob(os.path.join('input/', '*')):
    print "Processing %s" % dustfile
    d = TTsreDust(dustfile)
    d.optical_properties._extrapolate(1.e-3, 1.e7)
    d.emissivities.set_lte(d.optical_properties, n_temp=100, temp_min=0.1, temp_max=1600.)
    d.write('dust_files_lite/' + os.path.basename(dustfile).replace('.par', '_lite.hdf5'))
    d.plot('dust_files_lite/' + os.path.basename(dustfile).replace('.par', '_lite.png'))
