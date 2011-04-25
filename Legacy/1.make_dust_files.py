import glob
import os

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

np.seterr(all='ignore')

from hyperion.dust import SimpleSphericalDust

for dustfile in glob.glob(os.path.join('input/', '*')):
    print "Processing %s" % dustfile
    d = SimpleSphericalDust(dustfile)
    d.optical_properties._extrapolate(1.e-3, 1.e7)
    d.write('dust_files/' + os.path.basename(dustfile).replace('.par', '.hdf5'))
    d.plot('dust_files/' + os.path.basename(dustfile).replace('.par', '.png'))
