# WRF-WVTs
Weather Research and Forecasting (WRF) model with moisture tracers

----

The implementation of moisture tracers, or water vapor tracers (WVT), in a regional model, allows users to track moisture from any possible source within the simulation domain. Therefore, this tagging tool is especially appropriate for researchers interested in moisture source studies. 

Users should follow the following steps to run WRF with tracers.

### Compilation

- Download WRF version 3.8.1 at http://www2.mmm.ucar.edu/wrf/users/download/get_sources.html
- Download here the model modules modified to allow moisture tracking, which are compressed within the modules_tracers_3.8.1.tar file
- Move the modules_tracers_3.8.1.tar file to the root directory of the WRF code and decompress it (tar -cvf modules_tracers_3.8.1.tar)
- Compile the WRF model as usual

### Preprocessing

The WPS program (grogrid, ungrib and metgrid) is not modified when introducing the moisture tracers. Therefore, it should be run as usual.However, a new pre-processing task is now needed before running the model. In addition to the met_em files from metgrid, you will need another NetCDF file containing the source region to be analyzed.

WRF-WVTs allows moisture tracking from 2-D and 3-D sources. A 2-D source refers to tagging moisture from surface evapotranspiration over a certain area. For its part, a 3-D source encompasses the entire atmosphere over a region of interest, or only a part of it (for example, the stratosphere), from which all exiting moisture is tagged.The NetCDF file containing the source regions must have a variable called TRMASK2D if you want to track moisture from a 2-D source or a variable called TRMASK3D if you want to track moisture from a 3-D source.These variables will take the value of 1 in the source region and 0 in the rest of the domain. So, for example, if you want to tagg moisture coming from the continents, the TRMASK2D variable should be exactly the same as the LANDMASK variable. The only difference is that the TRMASK2D variable must always be zero within the relaxation zone of the domain, to avoid inaccuracies since moisture is not conserved in that zone. Usually it will be very useful to start from the geo_em file (from geogrid) to build the file with the moisture sources. Here is an example in Python to build a NetCDF file containing a mask to track evaporated moisture over the continents.

``` p
#!/usr/bin/python
# 2D-binary Tacer Mask Generator

######################################################
Grid_Information_File = 'geo_em.d01.nc'            ###
w_e_points = 1415                                  ###
s_n_points = 361	                               ###
tiempos = 1                                        ###
data_time_step_hours = 3                           ###
dx = 20000                                         ###
dy = 20000                                         ###
######################################################

import sys,os

Data = sys.argv[1]
Fecha = '%s_00:00:00'%Data 

import numpy as np
from netCDF4 import Dataset
import time, sys, datetime

# NetCDF file name!!!
dataset = Dataset('trmask','w', format = 'NETCDF3_CLASSIC')

Time = dataset.createDimension('Time', None)
south_north = dataset.createDimension('south_north', s_n_points)
west_east = dataset.createDimension('west_east', w_e_points)
DateStrLen = dataset.createDimension('DateStrLen', len(Fecha))

XLAT = dataset.createVariable('XLAT',np.float32,('south_north','west_east',))
XLONG = dataset.createVariable('XLONG',np.float32,('south_north','west_east',))
TRMASK = dataset.createVariable('TRMASK',np.float32,('Time','south_north','west_east',))
Times = dataset.createVariable('Times','S1',('Time','DateStrLen',))

# Atributos Propios
TRMASK.FieldType = 104
TRMASK.MemoryOrder = "XYZ" 
TRMASK.description = "Tracers Source Mask (1 FOR SOURCE)"
TRMASK.units = ""
TRMASK.stagger = ""
TRMASK.coordinates = "XLONG XLAT"

XLAT.FieldType = 104
XLAT.MemoryOrder = "XY "
XLAT.description = "LATITUDE SOUTH IS NEGATIVE"
XLAT.units = "degree_north"
XLAT.stagger = ""

XLONG.FieldType = 104
XLONG.MemoryOrder = "XY "
XLONG.description = "LONGITUDE WEST IS NEGATIVE"
XLONG.units = "degree_east"
XLONG.stagger = ""

# Atributos Globales
dataset.TITLE = 'Tracers Moisture Sources Mask Definition'
dataset.START_DATE = Fecha
dataset.MMINLU = 'USGS'
dataset.NUM_LAND_CAT = 24

Grid_Information = Dataset(Grid_Information_File)

LAT        = Grid_Information.variables['XLAT_M'][0,:]
LON        = Grid_Information.variables['XLONG_M'][0,:]
LANDMASK   = Grid_Information.variables['LANDMASK'][0,:]
LAKE_DEPTH = Grid_Information.variables['LAKE_DEPTH'][0,:]

for i in range(LAT.shape[0]):
	for j in range(LAT.shape[1]):
		XLAT[i,j] = LAT[i,j]
	
for i in range(LON.shape[0]) :
	for j in range(LON.shape[1]):
		XLONG[i,j] = LON[i,j]

for t in range(tiempos):
	TRMASK[t,:,:] = 0

###############################################################################################################
# Code to create trmask_ta                                                                                  ###
                                                                                                            ###
for i in range(TRMASK.shape[1]) :                                                                           ###
	for j in range(TRMASK.shape[2]) :                                                                       ###
		if LAT[i,j]>=0. and LAT[i,j]<=23.43693:                                                             ###
			TRMASK[:,i,j] = 1                                                                               ###
                                                                                                            ###                 
###############################################################################################################

for m in range(len(Fecha)):
      aux=Fecha
      Times[0,m] = aux[m]
			
dataset.close()

os.system('mkdir %s'%Data)
os.system('mv trmask %s'%Data)
```
