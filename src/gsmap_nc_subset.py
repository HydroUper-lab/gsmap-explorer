import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset


def extract_subset(nc_file, lat_min, lat_max, lon_min, lon_max, var_name="precipitation"):
    """
    Extract subset data dari file netCDF (GSMap)
    """

    ds = Dataset(nc_file, "r")

    # biasanya variable di GSMap
    lats = ds.variables["lat"][:]
    lons = ds.variables["lon"][:]
    times = ds.variables["time"][:]

    data = ds.variables[var_name][:]  # (time, lat, lon)

    # filter index
    lat_idx = np.where((lats >= lat_min) & (lats <= lat_max))[0]
    lon_idx = np.where((lons >= lon_min) & (lons <= lon_max))[0]

    subset = data[:, lat_idx, :][:, :, lon_idx]

    # convert ke dataframe
    rows = []
    for t in range(subset.shape[0]):
        for i, lat_i in enumerate(lat_idx):
            for j, lon_j in enumerate(lon_idx):
                rows.append({
                    "time": times[t],
                    "lat": float(lats[lat_i]),
                    "lon": float(lons[lon_j]),
                    "value": float(subset[t, i, j])
                })

    df = pd.DataFrame(rows)

    ds.close()
    return df


def save_to_csv(df, out_file):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    df.to_csv(out_file, index=False)
