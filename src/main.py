import glob
from datetime import datetime
from pathlib import Path
import geopandas as gpd
from dateutil.relativedelta import relativedelta

from utils.config_reader import read_config
from core.reader import read_netcdf

from apps.extract_csv import export_csv
from apps.visualize import plot_map  # nanti
from apps.thiessen_analysis import polygon_thiesen


def run_pipeline(mode="extract"):
    # ========================
    # konfigurasi
    # ========================
    config = read_config("config/input.txt")

    start_date = datetime.strptime(config.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(config.get("end_date"), "%Y-%m-%d")



    # ========================
    # menentukan extent
    # ========================
    if config.get("path_shp") and config.get("path_shp") != "None":
        gdf = gpd.read_file(config.get("path_shp"))

        if gdf.crs is None:
            raise ValueError("Shapefile tidak memiliki CRS")

        if gdf.crs.to_string() != "EPSG:4326":
            gdf = gdf.to_crs(epsg=4326)

        minx, miny, maxx, maxy = gdf.total_bounds
        extent = [minx-0.1, maxx+0.15, miny-0.15, maxy+0.1]

    else:
        extent = [
            float(config.get("min_lon")),
            float(config.get("max_lon")),
            float(config.get("min_lat")),
            float(config.get("max_lat"))
        ]

    # ========================
    # Baca file NetCDF
    # ========================
    all_nc_files = glob.glob(str(Path(config.get("path_nc")) / "*.nc"))
    current = start_date.replace(day=1)
    required_months = []

    while current <= end_date:
        required_months.append(current.strftime("%Y_%m"))
        current += relativedelta(months=1)
    
    list_nc_files = []

    for ym in required_months:
        matched_file = next(
            (f for f in all_nc_files if f"{ym}.nc" in Path(f).name),
            None
        )
        if matched_file is None:
            continue  # Skip if the file for the month is not found
        list_nc_files.append(matched_file)

    if not list_nc_files:
        raise FileNotFoundError("Tidak ada file NetCDF yang ditemukan untuk rentang tanggal yang diberikan.")


    data_subset, times, XX_subset, YY_subset = read_netcdf(list_nc_files, start_date, end_date, extent=extent)
    if data_subset is None or times is None:
        raise ValueError("Tidak ada data yang ditemukan dalam rentang tanggal yang diberikan.")



    # ========================
    # MODE CONTROL
    # ========================
    if mode == "extract":
        export_csv(data_subset, times, XX_subset, YY_subset, config.get("path_out"), config)

    elif mode == "visualize":

        plot_map(data_subset, times, XX_subset, YY_subset, config)

    elif mode == 'thiessen':
        export_csv(data_subset, times, XX_subset, YY_subset, config.get("path_out"), config)
        polygon_thiesen(config)

    elif mode == "all":
        export_csv(data_subset, times, XX_subset, YY_subset, config.get("path_out"), config)
  
        plot_map(data_subset, times, XX_subset, YY_subset, config)
        polygon_thiesen(config)
