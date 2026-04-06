@echo off
echo =========================================
echo    Predict Next Number - Launcher
echo =========================================

echo [1/3] Ελεγχος εγκαταστασης Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Η Python δεν βρεθηκε στο συστημα σας!
    set /p install="Θελετε να γινει αυτοματη ληψη και εγκατασταση τωρα; (Y/N): "
    if /I "%install%" NEQ "Y" (
        echo Η εγκατασταση ακυρωθηκε.
        pause
        exit /b 1
    )
    echo Γινεται ληψη της Python... (παρακαλω περιμενετε)
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
    echo Γινεται εγκατασταση... (ισως ζητηθει αδεια διαχειριστη στο παρασκηνιο)
    start /wait python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python_installer.exe
    echo.
    echo ΕΓΚΑΤΑΣΤΑΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ! Παρακαλω κλειστε αυτο το παραθυρο και ξανατρεξτε το run.bat.
    pause
    exit /b 1
)

echo [2/3] Εγκατασταση απαιτουμενων βιβλιοθηκων (Numpy)...
python -m pip install -r requirements.txt >nul 2>&1

echo [3/3] Εκκινηση εφαρμογης...
python predict_next.py