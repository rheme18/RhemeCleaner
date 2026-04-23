@echo off
title RhemeCleaner - Kurulum Sihirbazi
echo ======================================================
echo           RHEME CLEANER KURULUM SERVISI
echo ======================================================
echo.
echo [1] Python modulleri kontrol ediliyor...
echo.

:: Python yüklü mü kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Python bilgisayarinizda yuklu degil! 
    echo Lutfen python.org adresinden yukleyip tekrar deneyin.
    pause
    exit
)

echo [2] Gereksinimler yukleniyor (Bu biraz zaman alabilir)...
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo HATA: Yukleme sirasinda bir sorun olustu.
    pause
    exit
)

echo.
echo ======================================================
echo   KURULUM TAMAMLANDI! RhemeCleaner kullanima hazir.
echo   Programi baslatmak icin main.py'yi calistirabilirsiniz.
echo ======================================================
echo.
pause