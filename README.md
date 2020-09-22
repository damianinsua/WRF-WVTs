# WRF-WVTs
Weather Research and Forecasting (WRF) model with moisture tracers

----

The implementation of moisture tracers, or water vapor tracers (WVT), in a regional model, allows users to track moisture from any possible source within the simulation domain. Therefore, this tagging tool is especially appropriate for researchers interested in moisture source studies. 

Users should follow the following steps to run WRF with tracers.

## Compilation

- Download WRF version 3.8.1 at http://www2.mmm.ucar.edu/wrf/users/download/get_sources.html
- Download here the model modules modified to allow moisture tracking, which are compressed within the modules_tracers_3.8.1.tar file
- Move the modules_tracers_3.8.1.tar file to the root directory of the WRF code and decompress it (tar -cvf modules_tracers_3.8.1.tar)
- Compile the WRF model as usual

## Preprocessing

The WPS program (grogrid, ungrib and metgrid) is not modified when introducing the moisture tracers. Therefore, it should be run as usual.However, a new pre-processing task is now needed before running the model. In addition to the met_em files from metgrid, you will need another NetCDF file containing the source region to be analyzed.

WRF-WVTs allows moisture tracking from 2-D and 3-D sources. A 2-D source refers to tagging moisture from surface evapotranspiration over a certain area. For its part, a 3-D source encompasses the entire atmosphere over a region of interest, or only a part of it (for example, the stratosphere), from which all exiting moisture is tagged.The NetCDF file containing the source regions must have a variable called TRMASK2D if you want to track moisture from a 2-D source or a variable called TRMASK3D if you want to track moisture from a 3-D source.These variables will take the value of 1 in the source region and 0 in the rest of the domain. So, for example, if you want to tagg moisture coming from the continents, the TRMASK2D variable should be exactly the same as the LANDMASK variable. The only difference is that the TRMASK2D variable must always be zero within the relaxation zone of the domain, to avoid inaccuracies since moisture is not conserved in that zone. Usually it will be very useful to start from the geo_em file (from geogrid) to build the file with the moisture sources. Attached is an example in Python to build a NetCDF file containing a mask to track evaporated moisture over the continents.

Additionally, WRF-WVTs can also be used to destroy the moisture in a certain region (sink). In this case, the sink variable must be called TRMASK3D2 within the NetCDF file. Thus, at all grid points where TRMASK3D2=1 the moisture will be forced to zero (q=0).

## Running WRF

When running the model, only two additional tasks need to be performed when using the moisture tracers. First, you have to link the NetCDF file that contains the source region, which we usually call trmask_d01. Once the trmask_d01 file has been linked to the directory where the simulation will be run, the namelist.input file must be modified. Below are the new parameters to be added in the namelist.input file.

```
 &time_control
 io_form_auxinput8                   = 2,	                  ;format of "trmask_d<domain>" file
 auxinput8_inname                    = "trmask_d<domain>",	;file with tracers masks 

 &physics
 scalar_pblmix                       = 0,	                  ;0 is necessary to prevent the scalar turbulent diffusion from being made twice
 tracer_pblmix                       = 0,	                  ;0 is necessary to prevent the tracer turbulent diffusion from being made twice

 &dynamics        
 tracer_adv_opt                      = 4,	                  ;advection option for tracers (4 is necessary to avoid numerical errors => moist_adv_opt = 4)  
 tracer_opt                          = 3,	                  ;choose 3 to activate tracers
 tracer2dsource		                   = 1,	                  ;choos 1 to activate 2D sources (0 no 2D source)
 tracer3dsource		                   = 0,	                  ;choos 1 to activate 3D sources (0 no 3D source)
 tracer3dsink		                     = 0,	                  ;choos 1 to activate 3D sinks (0 no 3D sink)
 tracerBCndown                       = 0,	                  ;choos 1 to activate tracers boundary conditions (when a ndown has been done for a nested domain)
 ```
