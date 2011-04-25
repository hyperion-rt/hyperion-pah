import glob
import os

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

np.seterr(all='ignore')

from hyperion.util.functions import filename2hdf5
from hyperion.dust import SimpleSphericalDust, prepare_emiss

for dustfile in glob.glob(os.path.join('input/', '*')):
    print "Processing %s" % dustfile
    dustfile_out = filename2hdf5(dustfile)
    d = SimpleSphericalDust(dustfile)
    d.optical_properties._extrapolate(1.e-3, 1.e7)
    d.write('dust_files/' + os.path.basename(dustfile_out))
    d.plot('dust_files/' + os.path.basename(dustfile_out).replace('.hdf5', '.png'))
