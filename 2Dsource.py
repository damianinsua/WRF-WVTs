#!/usr/bin/python
# 2D-binary Tacer Mask Generator

######################################################
Grid_Information_File = 'geo_em.d01.nc'            ### path where the geo_em file is located
w_e_points = 199                                   ### number of grid cells in the west-east direction
s_n_points = 199	                               ### number of grid cells in the south-north direction
######################################################

import sys,os
import numpy as np
from netCDF4 import Dataset
import time, sys, datetime

# Enter the start date of your simulation (1985-10-12, for example)
Date = sys.argv[1] 
Fecha = '%s_00:00:00'%Date 

# NetCDF file name
dataset = Dataset('trmask_d01','w', format = 'NETCDF3_CLASSIC')

# Create dataset
Time = dataset.createDimension('Time', None)
south_north = dataset.createDimension('south_north', s_n_points)
west_east = dataset.createDimension('west_east', w_e_points)
DateStrLen = dataset.createDimension('DateStrLen', len(Fecha))

XLAT = dataset.createVariable('XLAT',np.float32,('south_north','west_east',))
XLONG = dataset.createVariable('XLONG',np.float32,('south_north','west_east',))
TRMASK = dataset.createVariable('TRMASK',np.float32,('Time','south_north','west_east',))
Times = dataset.createVariable('Times','S1',('Time','DateStrLen',))

# Attributes
TRMASK.FieldType = 104
TRMASK.MemoryOrder = "XY" 
TRMASK.description = "Tracer Source Mask (1 FOR SOURCE)"
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

dataset.TITLE = 'Tracer Moisture Sources Mask Definition'
dataset.START_DATE = Fecha
#You must modify the following attributes if you use other sources for land use, such as USGS
dataset.MMINLU = "MODIFIED_IGBP_MODIS_NOAH"
dataset.NUM_LAND_CAT = 21

# Read geo_em file and get useful variables
Grid_Information = Dataset(Grid_Information_File)

LAT        = Grid_Information.variables['XLAT_M'][0,:]
LON        = Grid_Information.variables['XLONG_M'][0,:]
LANDMASK   = Grid_Information.variables['LANDMASK'][0,:]

# Initialize variables
XLAT[:]=np.copy(LAT[:])
XLONG[:]=np.copy(LON[:])
TRMASK[:] = 0

for m in range(len(Fecha)):
      aux=Fecha
      Times[0,m] = aux[m]

###############################################################################################################
# Code to create the moisture source region                                                                 ###
                                                                                                            ###
TRMASK[0,:]=np.copy(LANDMASK[:])                                                                            ###
#Avoid relaxation zone                                                                                      ###
TRMASK[0,0:5,:]=0                                                                                           ###
TRMASK[0,:,0:5]=0                                                                                           ###
TRMASK [0,195:200,:]=0                                                                                      ###
TRMASK[0,:,195:200]=0                                                                                       ###    
###############################################################################################################

dataset.close()

