Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   Predict Next Number - Launcher" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`n[1/3] Έλεγχος εγκατάστασης Python..."
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Η Python δεν βρέθηκε στο σύστημά σας!" -ForegroundColor Yellow
    $install = Read-Host "Θέλετε να γίνει αυτόματη λήψη και εγκατάσταση τώρα; (Y/N)"
    if ($install -notmatch "^[Yy]$") {
        Write-Host "Η εγκατάσταση ακυρώθηκε." -ForegroundColor Red
        Read-Host "Πατήστε Enter για έξοδο..."
        exit
    }
    Write-Host "Γίνεται λήψη της Python..." -ForegroundColor Cyan
    $installer = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe" -OutFile $installer
    Write-Host "Γίνεται εγκατάσταση... (ίσως ζητηθεί άδεια διαχειριστή)" -ForegroundColor Cyan
    Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0" -Wait
    Remove-Item $installer
    Write-Host "`nΕΓΚΑΤΑΣΤΑΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ! ΠΑΡΑΚΑΛΩ ΚΛΕΙΣΤΕ ΑΥΤΟ ΤΟ ΠΑΡΑΘΥΡΟ ΚΑΙ ΞΑΝΑΤΡΕΞΤΕ ΤΟ SCRIPT." -ForegroundColor Green
    Read-Host "Πατήστε Enter για έξοδο..."
    exit
}

Write-Host "[2/3] Εγκατάσταση απαιτούμενων βιβλιοθηκών (Numpy)..."
python -m pip install -r requirements.txt | Out-Null

Write-Host "[3/3] Εκκίνηση εφαρμογής..." -ForegroundColor Green
python predict_next.py