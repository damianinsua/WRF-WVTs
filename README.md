# WRF-WVTs
Weather Research and Forecasting (WRF) model with moisture tracers

----

The implementation of moisture tracers, or water vapor tracers (WVT), in a regional model, allows users to track moisture from any possible source within the simulation domain. Therefore, this tagging tool is especially appropriate for researchers interested in moisture source studies. 

Users should follow the following steps to run WRF with tracers. The described steps refer to version 4.3.3, but if you want to use version 3.8.1, you must take into account a couple of minor differences (see releases).

## Compilation

- Download WRF version 4.3.3 at https://github.com/wrf-model/WRF/releases
- Download here the model modules modified to allow moisture tracking, which are compressed within the modules_tracers_4.3.3.tar file
- Move the modules_tracers_4.3.3.tar file to the root directory of the WRF code and decompress it (tar -xvf modules_tracers_4.3.3.tar)
- Compile the WRF model as usual

## Preprocessing

The WPS program (grogrid, ungrib and metgrid) is not modified when introducing the moisture tracers. Therefore, it should be run as usual. However, a new pre-processing task is now needed before running the model. In addition to the met_em files from metgrid, you will need another NetCDF file containing the source region to be analyzed.

WRF-WVTs allows moisture tracking from 2-D and 3-D sources. A 2-D source refers to tagging moisture from surface evapotranspiration over a certain area. For its part, a 3-D source encompasses the entire atmosphere over a region of interest, or only a part of it (for example, the stratosphere), from which all exiting moisture is tagged.The NetCDF file containing the source regions must have a variable called TRMASK if you want to track moisture from a 2-D source or a variable called TRMASK3D if you want to track moisture from a 3-D source.These variables will take the value of 1 in the source region and 0 in the rest of the domain. So, for example, if you want to tagg moisture coming from the continents, the TRMASK variable should be exactly the same as the LANDMASK variable. The only difference is that the TRMASK variable must always be zero within the relaxation zone of the domain, to avoid inaccuracies since moisture is not conserved in that zone. Note that, on the contrary, the TRMASK3D variable can be 1 in this zone. In fact, if you want to track only the moisture entering through the domain boundaries, the TRMASK3D variable should take values of 1 right in the relaxation zone. Usually it will be very useful to start from the geo_em file (from geogrid) to build the file with the moisture sources. Attached is an example in Python (2Dsource.py) to build a NetCDF file containing a mask to track evaporated moisture over the continents.

Additionally, WRF-WVTs can also be used to destroy the moisture in a certain region (sink). In this case, the sink variable must be called TRMASK3D2 within the NetCDF file. Thus, at all grid points where TRMASK3D2=1 the moisture will be forced to zero (q=0).

## Running WRF

When running the model, only two additional tasks need to be performed when using the moisture tracers. First, you have to link the NetCDF file that contains the source region, which we usually call trmask_d01. Once the trmask_d01 file has been linked to the directory where the simulation will be run, the namelist.input file must be modified. Please, find below the new parameters to be added in the namelist.input file.

```
 &time_control
 io_form_auxinput8   = 2,                      ;format of the "trmask_d<domain>" file (NetCDF)
 auxinput8_inname    = "trmask_d<domain>",     ;name of the file with the source regions 

 &physics
 scalar_pblmix       = 0,     ;0 is necessary to prevent the scalar turbulent diffusion from being made twice
 tracer_pblmix       = 0,     ;0 is necessary to prevent the tracer turbulent diffusion from being made twice

 &dynamics        
 tracer_adv_opt      = 4,	    ;advection option for tracers (4 is necessary to avoid numerical errors => moist_adv_opt = 4)  
 tracer_opt          = 4,	    ;choose 4 to activate tracers
 tracer2dsource      = 1,	    ;choose 1 to activate 2D sources (0 no 2D source)
 tracer3dsource      = 0,	    ;choose 1 to activate 3D sources (0 no 3D source)
 tracer3dsink        = 0,	    ;choose 1 to activate 3D sinks (0 no 3D sink)
 ```
The previous options have been included in the README.tracers file in the run directory. You must also take into account that in order to use WRF-WVTs, for now it is mandatory to select the following parameterisations: Yonsei University PBL scheme (bl_pbl_physics=1), the WRF Single-Moment 6-class microphysics scheme (mp_physics=6) and the Kain–Fritsch convective parameterisation (cu_physics=1), although in a convective-resolving scale, tracers can also be used without the Kain–Fritsch scheme. The rest of the parameterisations, such as the land surface scheme or radiation schemes, are freely selectable.

When you have modified the namelist.input, you simply have to run the model as usual and that's it!

## Postprocessing

When you use WRF-WVTs, 13 new variables will appear in the wrfout output file. As we use the WSM6 scheme, which includes 6 moisture species, 6 moisture tracers species will also appear, called tr_qv, tr_qc,tr_qi,tr_qr,tr_qs and tr_qg (water vapor, cloud water, rain water, snow, ice and graupel tracer mixing ratios, respectively). TR_RAINC and TR_RAINNC will be the tracer convective and non convective precipitation, i.e. coming from the chosen source region. TR_SNOWNC and TR_GRAUPELNC correspond to tracer snow and graupel (solid) precipitation. The other three variables (TRQFX,tr_thum_u_phy_dt and tr_thum_v_phy_dt) were only implemented for validation purposes.
 
## Citation

You should include the following reference whenever you use the WRF-WVTs tool for research publications.

***Insua-Costa, D. and Miguez-Macho, G.***: A new moisture tagging capability in the Weather Research and Forecasting model: formulation, validation and application to the 2014 Great Lake-effect snowstorm, Earth Syst. Dynam., 9, 167–185, https://doi.org/10.5194/esd-9-167-2018, 2018.

## Contact

Feel free to contact me: damian.insuacosta@ugent.be
