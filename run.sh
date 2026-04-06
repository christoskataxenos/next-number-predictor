#!/bin/bash

echo "========================================="
echo "   Predict Next Number - Launcher"
echo "========================================="

echo "[1/3] Έλεγχος εγκατάστασης Python..."
if ! command -v python3 &> /dev/null; then
    echo "Η Python3 δεν βρέθηκε στο σύστημά σας!"
    read -p "Θέλετε να γίνει αυτόματη εγκατάσταση τώρα; (Y/n): " install
    if [[ "$install" != "Y" && "$install" != "y" && "$install" != "" ]]; then
        echo "Η εγκατάσταση ακυρώθηκε."
        exit 1
    fi
    
    echo "Γίνεται εγκατάσταση της Python3... (ενδέχεται να ζητηθεί ο κωδικός σας)"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-tk
    elif command -v brew &> /dev/null; then
        brew install python
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip python3-tkinter
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python python-pip tk
    else
        echo "Δεν βρέθηκε υποστηριζόμενος package manager. Παρακαλώ εγκαταστήστε χειροκίνητα."
        exit 1
    fi
    echo "Η εγκατάσταση ολοκληρώθηκε!"
fi

echo "[2/3] Εγκατάσταση απαιτούμενων βιβλιοθηκών (Numpy)..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1 || pip3 install -r requirements.txt > /dev/null 2>&1

echo "[3/3] Εκκίνηση εφαρμογής..."
python3 predict_next.py || python predict_next.py