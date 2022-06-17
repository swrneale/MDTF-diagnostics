
import numpy as np
import matplotlib.pyplot as mp
import xarray as xr
import datetime as dt
#from dateutil.relativedelta import relativedelta


import cartopy.crs as ccrs
import pandas as pd
import metpy as mpy
import dask as ds
xr.__version__

### To Import My Functions ###
import vert_prof_func as mypy
import vert_prof_case_desc as mycase
import importlib




importlib.reload(mypy) # Required because I am constantly editing scam_func.py
importlib.reload(mycase) # Required because I am constantly editing scam_func.py


''''' Which case to use '''''

case_desc = []

''' ##### REVERT EXPERIMENTS ##### '''

pref_out = 'cam6_revert_test'
#case_desc = np.array(['C6','C5','rC5now','rUW','rUWp','rMG1','rC5p','rC5pm','rZMc','rZMp','rpfrac','rCE2i']) ; pref_out = 'revert'
#case_desc = ['rCE2i','rUW','rSB','rC5p','rM3','rclm4']
#case_desc = ['rCE2i','rUW','rSB','rC5p','rM3','rclm4']
#case_desc = ['rZMp','rpfrac']
#case_desc = ['rTMS']
#case_desc = ['rpremit']
#case_desc = ['rGW']
#case_desc = ['rnohertz']
#case_desc = ['rM3']

#case_desc = ['C6','rC5','rCE2i','rUW','rMG1','rC5p','rZMc','rZMp','rpfrac','rTMS','rGW'] 
## Do not have. -- 'rZMc','rZmp','rpfrac','rTMS','rGW']
case_desc = ['C6','rC5','rCE2i','rUW','rMG1','rC5p','rZMc','rZMp','rpfrac','rTMS','rGW'] 


#case_desc = ['C6','rC5'] ; pref_out = 'test'   

nrevert = len(case_desc)
case_type = ['cam6_revert']*nrevert



''' ##### SETTINGS INCLUDING ENSEMBLES ###### '''

#pref_out = 'lens1_test'    
#nens = 3

#case_desc = ['CE1.E%01d'%(itt) for itt in range(1,nens+1)]
#case_type  = ['lens1']*nens

#case_desc = ['C6.E%01d'%(itt) for itt in range(1,nens+1)]
#case_type  = ['c6_amip']*nens



''' ###### REANAL+ABOVE MODEL SIMS ######## '''

#pref_out = 'c5_amip_reanal_era5'
#pref_out = 'cam56_ERA5'

#case_reanal = ['ERA5','ERAI','CFSR','MERRA2','JRA25'] 
#type_reanal = ['reanal','reanal','reanal','reanal','reanal']

case_reanal = ['MERRA2'] 
type_reanal = ['reanal']


reanal_climo = True # Grab climo. values for mean, Nino and nina events for reanalysis only

#case_desc = np.array(case_reanal)
#case_type = np.array(type_reanal)


case_desc = np.array(case_desc+case_reanal)
case_type = np.array(case_type+type_reanal)


case_desc = np.array(case_desc)
case_type = np.array(case_type)


#case_desc = np.flip(case_desc)
#case_type = np.flip(case_type)







## INDIVIDUAL CASE SETTINGS/ADDITIONS ##

''''' Which nino SST region '''''
nino_region = 'nino34'




''' SEASON '''

seas_mons = np.array(["Jan","Feb","Dec"])

clim_anal = False

''''' Years for the analysis '''''

years_data = (1979,2005) # Year range of history files to read AND either 'climo' one file or 'tseries' many files


''' REGIONAL SPECS (LAT/LON/LEV) '''

#lats_in = -10. ; latn_in = 5.
#lonw_in = 150. ; lone_in = 220.
ppmin = 50. ; ppmax = 1000.



''''' Variable description '''''

var_cam = 'OMEGA'
ldiv = False # Calculate divergence from OMEGA if var_Cam = OMEGA




''''' Directory Information '''''

dir_croot = '/glade/p/cgd/amp/people/hannay/amwg/climo/' # Directories with climo files
dir_hroot = '/glade/p/cgd/amp/amwg/runs/' # Run firectories with history files

dir_proot = '/glade/u/home/rneale/python/python-figs/vert_proc/'
dir_obs = '/glade/p/cesm/amwg/amwg_data/obs_data/'



## Variables ##

var_desc = {}

var_desc['DTCOND'] = ['dT/dt Total',86400.,1., -5.,5.,-2.,2.,'K/day']
var_desc['DCQ']    = ['dq/dt Total',86400*1000.,1., -4.,4.,-4.,4.,'g/kg/day']
var_desc['ZMDT']   = ['dT/dt Convection',86400., 1.,-5.,5.,-2.,2.,'K/day']
var_desc['ZMDQ']   = ['dq/dt Convection',86400.*1000., 1.,-4.,4.,-4.,4.,'g/kg/day']
var_desc['MPDT']   = ['dT/dt Microphysics',86400./1004., 1.,-5.,5.,-2.,2.,'K/day']
var_desc['STEND_CLUBB'] = ['dT/dt turbulence',86400./1004., 1. ,-2.,8.,-2.,8.,'K/day']


var_desc['OMEGA'] = ['OMEGA',-1., -1., -0.06,0.06,-0.06,0.06,'pa/s']
var_desc['DIV'] = ['Divergence',1., 100./86400., -0.0004,0.0004,-0.0004,0.0004,'s^-1']
var_desc['T'] = ['Temperature',1., 1., -10.,10.,-10.,10.,'K']
var_desc['Q'] = ['Specific Humidity',1000., 1000., 0.,20.,-5.,5.,'g/kg']
var_desc['U'] = ['Zonal Wind',1., 1., -60.,60.,-10.,10.,'m/s']



''''' Named Regions '''''

reg_names = {}

#### RBN Original Locations ####
#reg_names['Nino Wet'] = ['C. Pacific Nino Wet',-10,0.,160.,210]  # Core of nino precip signal
reg_names['WP Dry']   = ['West Pac. Nino Dry.',-5.,10.,120.,150]  # Core of W. Pacific signal
#reg_names['Conv U']   = ['Convergence Min',25,50.,160,190]       # Core of RWS convergence min.
#reg_names['CE Pac']   = ['East Pacific ITCZ',5,10.,220,270]       # Core of RWS convergence min.

#### Anna Locations ####

#reg_names['Nino Wet'] = ['C. Pacific Nino Wet',-10,0.,160.,220]  # Core of nino precip signal
#reg_names['WP Dry']   = ['West Pac. Nino Dry.',0.,15.,110.,150]  # Core of W. Pacific signal
#reg_names['Conv U']   = ['Convergence Min',25,40.,150,200]       # Core of RWS convergence min.


#1. positive precipitation anomalies -equatorial central Pacific : 160E-140W; 10S-EQ (Main tropical forcing)
#2. Divergence anomalies subtropical North Pacific: 150E-160W; 25-40N (RWS generation region)
#3. Negative precipitation anomalies western Pacific: 110E-150E; EQ-15N (Additional contribution to RWS) 

# Include observations? #
lobs = False

# Pressure info.

p_levs = np.arange(ppmin,ppmax,50.)



#sim_names = cam_revert_list()
#sim_names = cam_vres_list()
#sim_names = mycase.cam_reanal_list()
sim_names = mycase.mdtf_case_list()




## Specify data frames ##
print(reg_names)
reg_df = pd.DataFrame.from_dict(reg_names, orient='index',columns=['long_name','lat_s','lat_n','lon_w','lon_e'])
var_df = pd.DataFrame.from_dict(var_desc, orient='index',columns=['long_name','vscale','ovscale','xmin','xmax','axmin','axmax','vunits'])

display(reg_df)
print()
display(var_df)

reg = list(reg_names.keys())[0]

reg_s = reg_df.loc[reg]['lat_s'] ; reg_n = reg_df.loc[reg]['lat_n']
reg_w = reg_df.loc[reg]['lon_w'] ; reg_e = reg_df.loc[reg]['lon_e']
 

nmnths = seas_mons.size
ncases = case_desc.size
nregions = reg_df.index.size

xmin = var_df.loc[var_cam]['xmin'] ; xmax=var_df.loc[var_cam]['xmax']
axmin = var_df.loc[var_cam]['axmin'] ; axmax=var_df.loc[var_cam]['axmax']                     
vunits = var_df.loc[var_cam]['vunits'] 
var_text = var_df.loc[var_cam]['long_name']   
var_pname = var_cam

if ldiv and var_cam == 'OMEGA':
    var_pname = 'DIV'
    var_text = var_df.loc[var_pname]['long_name']     
    vunits = var_df.loc[var_pname]['vunits'] 
    xmin = var_df.loc[var_pname]['xmin'] ; xmax=var_df.loc[var_pname]['xmax']
    axmin = var_df.loc[var_pname]['axmin'] ; axmax=var_df.loc[var_pname]['axmax']                
    

#%matplotlib inline
#ds.config.set({"array.slicing.split_large_chunks": True})
