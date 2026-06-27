import datetime

from netCDF4 import Dataset, num2date
import numpy as np


def read_netcdf(file_path_list, start_date=None, end_date=None):
    times_all = []
    data_all = []
    for file_path in file_path_list:
        with Dataset(file_path, 'r') as nc:
            time_var = nc.variables['time']
            times = num2date(
            time_var[:],
            units=time_var.units,
            calendar=getattr(time_var, 'calendar', 'standard'))
            
            times = np.array([datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
                for t in times
            ])

            # times = np.array(times)  # Convert to numpy array for easier slicing
            min_time = np.min(times)
            max_time = np.max(times)

            data = nc.variables['precipitation'][:,:,:]
            mask = np.ones(data.shape[0], dtype=bool)

            if start_date is not None:
                mask &= (times >= start_date)
            if end_date is not None:
                mask &= (times <= end_date)

            if not np.any(mask):
                continue  
            times_all.append(times[mask])
            data_all.append(data[mask, :, :])

    if len (times_all) == 0:
        return np.array([]), np.array([])
    
    times_all = np.concatenate(times_all)
    data_all = np.concatenate(data_all, axis=0)

    sort_idx = np.argsort(times_all)
    times_all = times_all[sort_idx]
    data_all = data_all[sort_idx, :, :]

    unique_times, unique_idx = np.unique(times_all, return_index=True)
    unique_data = data_all[unique_idx, :, :]
    
    return unique_data, unique_times


def spatialsubset_netcdf(data,extent):
    """
    extent: [min_lon, max_lon, min_lat, max_lat]
    """
    XX = np.arange(90.05, 150.06, 0.1) 
    YY = np.arange(15.05, -15.06, -0.1) 

    min_lon, max_lon, min_lat, max_lat = extent
    lon_mask = (XX >= min_lon) & (XX <= max_lon)
    lat_mask = (YY >= min_lat) & (YY <= max_lat)

    data = data[:, lat_mask, :][:, :, lon_mask]

    return data, XX[lon_mask], YY[lat_mask]
