import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
import numpy as np
from datetime import timedelta


def plot_map(data, times, XX, YY, config=None, extent=None):

    # ========================
    # SUBSET EXTENT (optional)
    # ========================
    if extent is not None:
        min_lon, max_lon, min_lat, max_lat = extent

        lon_mask = (XX >= min_lon) & (XX <= max_lon)
        lat_mask = (YY >= min_lat) & (YY <= max_lat)

        data = data[:, lat_mask, :][:, :, lon_mask]
        XX = XX[lon_mask]
        YY = YY[lat_mask]

    # ========================
    # GRID
    # ========================
    XX_mesh, YY_mesh = np.meshgrid(XX, YY)
    projection = ccrs.PlateCarree()

    # ========================
    # TIMEZONE
    # ========================
    wilayah_waktu = config.get("wilayah_waktu")
    if wilayah_waktu == "WIB":
        time_offset = 7
    elif wilayah_waktu == "WITA":
        time_offset = 8
    elif wilayah_waktu == "WIT":
        time_offset = 9
    else:
        time_offset = 0

    # ========================
    # OUTPUT
    # ========================
    output_dir = Path(config.get("path_out")) / "visualization_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ========================
    # PREPROCESS DATA
    # ========================
    data = data.copy()

    # hanya buang nilai negatif (0 masih valid hujan)
    data[data <= 0] = np.nan

    # ========================
    # COLOR SCALE GLOBAL
    # ========================
    if np.all(np.isnan(data)):
        vmin, vmax = 0, 1
    else:
        vmin = np.nanmin(data)
        vmax = np.nanmax(data)

    # ========================
    # COLORMAP (dengan NaN)
    # ========================
    cmap = plt.get_cmap("Blues").copy()
    cmap.set_bad(color="lightgray")  # warna untuk area tanpa data

    # ========================
    # LOOP PLOTTING
    # ========================
    for i, time in enumerate(times):

        fig = plt.figure(figsize=(12, 7))
        ax = plt.axes(projection=projection)

        ax.set_extent([XX.min(), XX.max(), YY.min(), YY.max()])

        # ========================
        # PLOT DATA
        # ========================
        im = ax.pcolormesh(
            XX_mesh,
            YY_mesh,
            data[i, :, :],
            transform=projection,
            cmap=cmap,
            shading='auto',
            vmin=vmin,
            vmax=vmax
        )

        # ========================
        # COLORBAR
        # ========================
        cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.03)
        cbar.set_label("Hujan (mm/jam)", fontsize=10)

        # ========================
        # MAP FEATURES
        # ========================
        ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
        ax.add_feature(cfeature.BORDERS, linestyle=":")
        ax.add_feature(cfeature.LAND, facecolor="lightyellow", alpha=0.5)
        ax.add_feature(cfeature.OCEAN, facecolor="lightblue", alpha=0.3)

        # ========================
        # GRIDLINES
        # ========================
        gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
        gl.top_labels = False
        gl.right_labels = False

        # ========================
        # TIME
        # ========================
        adjusted_time = time + timedelta(hours=time_offset)
        strftime_time = adjusted_time.strftime("%Y-%m-%d %H:%M")



        # ========================
        # JIKA DATA KOSONG
        # ========================
        if np.all(np.isnan(data[i])):
            ax.text(
                0.5, 0.5, "No Data",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=14,
                color="red",
                weight="bold"
            )

        # ========================
        # TITLE (HARUS DI LUAR IF)
        # ========================
        fig.suptitle(
            f"Intensitas Hujan (mm/jam)\n{strftime_time} ({wilayah_waktu})",
            fontsize=12,
            weight="bold"
        )


        # ========================
        # SAVE
        # ========================
        plt.savefig(
            output_dir / f"precip_{i:03d}.png",
            dpi=150,
        )

        plt.close()

    print(f"✅ Visualisasi tersimpan di: {output_dir}")