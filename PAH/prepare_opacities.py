import atpy
import numpy as np

# Define constants
m_H = 1.66053886e-24

# Define fraction of mass in each size bin
frac = {'usg':0.0586, 'vsg':0.1351, 'big':0.8063}

# Define gas-to-dust ratio
gas_to_dust = 123.6

# Loop over size range
for ir, size in enumerate(['usg', 'vsg', 'big']):

    # Read in extinction cross-section
    t_ext = np.loadtxt('input/opacity/comp_opacity_ext.out', skiprows=7,
                       dtype=[('lambda', float), ('c_ext_C', float),
                              ('c_ext_Si', float)],
                       usecols=[0,1 + ir, 4 + ir])

    # Read in absorption cross-section
    t_abs = np.loadtxt('input/opacity/comp_opacity_abs.out', skiprows=7,
                       dtype=[('lambda', float), ('c_abs_C', float),
                              ('c_abs_Si', float)],
                       usecols=[0,1 + ir, 4 + ir])
         
    # Extract wavelength
    wav = t_ext['lambda']
    
    # Extract total extinction cross-section
    c_ext = t_ext['c_ext_C'] + t_ext['c_ext_Si'] 

    # Extract total absorption cross-section
    c_abs = t_abs['c_abs_C'] + t_abs['c_abs_Si'] 
        
    # Convert from micron^2/H to cm^2/g
    c_ext *= 1.e-4**2 / m_H
    c_abs *= 1.e-4**2 / m_H
    
    # Convert from unit mass of gas to unit mass of dust. Here we are
    # converting to unit mass of the particular dust we are looking at, so
    # e.g. per unit mass of very small grains for the 'vsg' component.
    c_ext *= gas_to_dust / frac[size]
    c_abs *= gas_to_dust / frac[size]
    
    # Compute scattering cross-section
    c_sca = c_ext - c_abs
                 
    # Compute extinction opacity
    chi = c_ext

    # Write out to file
    t = atpy.Table()
    t.add_column('wav', wav)
    t.add_column('c_ext', c_ext)
    t.add_column('c_sca', c_sca)
    t.add_column('chi', chi)
    t.write('processed/opacities_%s.hdf5' % size, overwrite=True)
    