# 🌧️ GSMaP Explorer

A desktop-based GSMaP rainfall data processing and visualization tool focused on Indonesia.

---

## 🌍 Description

**GSMaP Explorer** is a desktop-based application designed to process and analyze GSMaP rainfall data in NetCDF (`.nc`) format.

Users can download GSMaP datasets from the HESLab-UPER data portal:

🔗 https://www.heslab-uper.com/riset-data/data/data-hujan-iklim/data-hujan-satelit-indonesia

After downloading the data, users can process it locally on their computer. The application supports rainfall visualization, spatial subsetting, and data export to CSV.

The current implementation is focused on rainfall data over Indonesia.

---

## 🇮🇩 Deskripsi

**GSMaP Explorer** adalah aplikasi berbasis desktop yang digunakan untuk pengolahan dan analisis data curah hujan GSMaP dalam format NetCDF (`.nc`).

Data GSMaP dapat diunduh melalui portal data HESLab-UPER:

🔗 https://www.heslab-uper.com/riset-data/data/data-hujan-iklim/data-hujan-satelit-indonesia

Setelah data diunduh, data dapat diolah secara lokal di komputer pengguna, termasuk visualisasi peta hujan, subset wilayah, dan ekspor data ke CSV.

Aplikasi ini difokuskan pada wilayah Indonesia.

---

## ✨ Features

- Processing GSMaP NetCDF rainfall data  
- Rainfall map visualization  
- Spatial subsetting based on extent or shapefile  
- Export rainfall data to CSV  

---

## 🧰 Fitur

- Pengolahan data curah hujan GSMaP (NetCDF)  
- Visualisasi peta distribusi hujan  
- Subset wilayah berdasarkan extent atau shapefile  
- Ekspor data ke format CSV  

---

## ⚙️ Installation

Install dependencies using one of the following methods:


```bash
pip install -r requirements.txt


conda env update -n base -f environment.yml

## ✅ Usage
✅ Step 1 – Prepare Data
Download GSMaP NetCDF (.nc) data from:
🔗 https://www.heslab-uper.com/riset-data/data/data-hujan-iklim/data-hujan-satelit-indonesia

✅ Step 2 – Configure Input
config/input.txt

✅ Step 3 – Run the Program
🔹 Option 1 (Windows)
    run.bat
🔹 Option 2 (CLI)
    python run.py --mode extract
    Available modes:
    🔹  extract → Export rainfall data to CSV
    🔹  visualize → Generate rainfall maps
    🔹  all → Run both