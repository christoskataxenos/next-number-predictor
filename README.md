# 🔮 Next Number Predictor

A Python tool that identifies mathematical patterns in a sequence and predicts the next value using regression and progression models.

---

## 🇬🇧 English Guide

### What this app does
The sequence predictor takes a string of numbers and attempts to find the underlying rule. It handles everything from simple arithmetic offsets to complex quadratic curves, providing a prediction with a confidence score (R²).

### How it works
The tool evaluates the input against five distinct mathematical models in order of complexity:
1.  **Arithmetic Progression**: Checks for a constant difference between terms.
2.  **Geometric Progression**: Checks for a constant ratio between terms.
3.  **Fibonacci-like Sequence**: Verifies if each term is the sum of the previous two.
4.  **Linear Regression**: Fits a straight line ($y = mx + b$) using `numpy.polyfit`.
5.  **Polynomial Prediction (Degree 2)**: Fits a quadratic curve ($y = ax^2 + bx + c$) for non-linear growth.

It calculates the R² score for the statistical models and selects the one with the highest confidence.

### Installation & Running
**Prerequisites:** Python 3.8+ and `numpy`.

1.  **Clone and Install:**
    ```bash
    git clone https://github.com/christoskataxenos/next-number-predictor.git
    cd next-number-predictor
    pip install -r requirements.txt
    ```
2.  **Run:**
    ```bash
    python predict_next.py
    ```

---

## 🇬🇷 Ελληνικός Οδηγός

### Τι κάνει η εφαρμογή
Αυτή η εφαρμογή αναλύει ακολουθίες αριθμών και προβλέπει την επόμενη τιμή. Εντοπίζει αυτόματα το μαθηματικό πρότυπο που διέπει τη σειρά, από απλές προόδους μέχρι σύνθετες παραβολικές καμπύλες.

### Πώς λειτουργεί
Η εφαρμογή αξιολογεί τα δεδομένα μέσω πέντε μοντέλων:
1.  **Αριθμητική Πρόοδος**: Αναζήτηση σταθερής διαφοράς.
2.  **Γεωμετρική Πρόοδος**: Αναζήτηση σταθερού λόγου.
3.  **Ακολουθία Fibonacci**: Έλεγχος αν κάθε όρος είναι το άθροισμα των δύο προηγούμενων.
4.  **Γραμμική Παλινδρόμηση**: Προσαρμογή ευθείας γραμμής μέσω `numpy`.
5.  **Πολυωνυμική Πρόβλεψη (2ου βαθμού)**: Προσαρμογή τετραγωνικής καμπύλης για μη γραμμική αύξηση.

Το σύστημα επιλέγει το μοντέλο με το υψηλότερο σκορ εμπιστοσύνης (R²).

### Εγκατάσταση & Εκτέλεση
**Προαπαιτούμενα:** Python 3.8+ και `numpy`.

1.  **Λήψη και Εγκατάσταση:**
    ```bash
    git clone https://github.com/christoskataxenos/next-number-predictor.git
    cd next-number-predictor
    pip install -r requirements.txt
    ```
2.  **Εκτέλεση:**
    ```bash
    python predict_next.py
    ```

---
*Based on the original logic by [thecretanguy](https://github.com/thecretanguy/next-number-predictor).*
