import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import MultiPoint, box
from shapely import voronoi_polygons
import pandas as pd
import geopandas as gpd
from pathlib import Path
from matplotlib import pyplot as plt
from pyproj import Geod


# # import testing
# import sys
# import os
# sys.path.append(os.path.abspath("D:/OneDrive/5_Code/2_Code_Automation/gsmap-explorer/src"))
# from utils.config_reader import read_config



geod = Geod(ellps="WGS84")

def geodesic_area(poly):
    area, _ = geod.geometry_area_perimeter(poly)
    return abs(area)


def polygon_thiesen (config):
    path_koordinat = Path(config.get("path_out")) / "csv_output" / "koordinat.csv"
    df_koordinat = pd.read_csv(path_koordinat)
    points_name = df_koordinat['name'].values
    points = df_koordinat[['lon', 'lat']].values
    path_hujan = Path(config.get("path_out")) / "csv_output" / "hujan_grid.csv"

    df_hujan = pd.read_csv(path_hujan, index_col=0, parse_dates=True)
    path_shp = Path(config.get("path_shp"))
    subdas = gpd.read_file(path_shp)
    if subdas.crs is None:
        subdas = subdas.set_crs("EPSG:4326")
    elif subdas.crs.to_epsg() != 4326:
        subdas = subdas.to_crs("EPSG:4326")
    bounds = subdas.total_bounds
    das_field = config.get("das_field")

    print ("polygon thiesen processing...")

    mp = MultiPoint(points)
    vor = voronoi_polygons(mp, extend_to=box(*bounds))


    thiessen = gpd.GeoDataFrame(
        {
            "station": points_name
        },
        geometry=list(vor.geoms),
        crs=subdas.crs
    )


    thiessen = gpd.overlay(
        thiessen,
        subdas[[das_field, "geometry"]],
        how="intersection"
    )

    
    thiessen = thiessen.sort_values(
        by=[das_field, "station"]
    ).reset_index(drop=True)

    
    thiessen["area_m2"] = thiessen.geometry.apply(
        geodesic_area
    )


    sub_das_values = thiessen[das_field].unique()
    results = []
    df_hujan = df_hujan.sort_index()


    areal_dict = {}

    for sub_das in sub_das_values:

        print(f"Processing sub-das: {sub_das}")

        thiessen_subdas = (
            thiessen[thiessen[das_field] == sub_das]
            .sort_values("station")
            .reset_index(drop=True)
        )

        stations = thiessen_subdas["station"].values

        hujan_subdas = df_hujan[stations]

        area = thiessen_subdas["area_m2"].values

        area_rain = (
            hujan_subdas.mul(area, axis=1)
            .sum(axis=1)
            / area.sum()
        )

        areal_dict[sub_das] = area_rain

    df_areal = pd.DataFrame(
        areal_dict,
        index=df_hujan.index
    )

    df_areal_daily = df_areal.resample("D").sum()
    df_areal_monthly = df_areal.resample("ME").sum()
    df_max_daily_yearly = df_areal_daily.resample("YE").max()


    df_areal.to_csv(Path(config.get("path_out")) / "csv_output" / "hujan_area_hourly.csv")
    df_areal_daily.to_csv(Path(config.get("path_out")) / "csv_output" / "hujan_area_daily.csv")
    df_areal_monthly.to_csv(Path(config.get("path_out")) / "csv_output" / "hujan_area_monthly.csv")
    df_max_daily_yearly.to_csv(Path(config.get("path_out")) / "csv_output" / "hujan_max_daily_yearly.csv")








# ## testing

# config = read_config("config/input.txt")
# polygon_thiesen(config)