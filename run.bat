@echo off
echo ==========================
echo   PILIH MODE PROGRAM
echo ==========================
echo 1. Extract CSV
echo 2. Visualisasi
echo 3. Hujan Regional (Thiessen)
echo 4. Semua
echo.

set /p choice=Pilih opsi (1/2/3/4): 

if "%choice%"=="1" (
    echo Menjalankan mode EXTRACT...
    python run.py --mode extract
) else if "%choice%"=="2" (
    echo Menjalankan mode VISUALIZE...
    python run.py --mode visualize
) else if "%choice%"=="3" (
    echo Menjalankan mode THIESSEN...
    python run.py --mode thiessen
) else if "%choice%"=="4" (
    echo Menjalankan mode ALL...
    python run.py --mode all
) else (
    echo Pilihan tidak valid!
)

pause
