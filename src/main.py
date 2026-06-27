
import glob
from datetime import datetime
from pathlib import Path
import geopandas as gpd

from utils.config_reader import read_config
from core.reader import read_netcdf, spatialsubset_netcdf

from apps.extract_csv import export_csv
# from apps.visualize import plot_map  # nanti


def run_pipeline(mode="extract"):
    # ========================
    # konfigurasi
    # ========================
    config = read_config("config/input.txt")

    start_date = datetime.strptime(config.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(config.get("end_date"), "%Y-%m-%d")

    # ========================
    # Baca file NetCDF
    # ========================
    list_nc_files = glob.glob(str(Path(config.get("path_nc")) / "*.nc"))
    data, times = read_netcdf(list_nc_files, start_date, end_date)

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
        extent = [minx, maxx, miny, maxy]

    else:
        extent = [
            float(config.get("min_lon")),
            float(config.get("max_lon")),
            float(config.get("min_lat")),
            float(config.get("max_lat"))
        ]

    # ========================
    # subset data spasial
    # ========================
    data_subset, XX_subset, YY_subset = spatialsubset_netcdf(data, extent)

    # ========================
    # MODE CONTROL
    # ========================
    if mode == "extract":
        export_csv(data_subset, times, XX_subset, YY_subset, config.get("path_out"))

    elif mode == "visualize":
        print("Mode visualize belum dibuat")
        # plot_map(data_subset, XX_subset, YY_subset)

    elif mode == "all":
        export_csv(data_subset, times, XX_subset, YY_subset, config.get("path_out"))
        print("Mode visualize belum dibuat")
        # plot_map(data_subset, XX_subset, YY_subset)
