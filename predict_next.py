import tkinter as tk
from tkinter import ttk, font
import numpy as np


def parse_numbers(text):
    """Μετατρέπει κείμενο εισόδου σε λίστα αριθμών."""
    text = text.replace(',', ' ').strip()
    if not text:
        raise ValueError("Δεν δόθηκαν αριθμοί.")

    parts = text.split()
    numbers = []
    for part in parts:
        try:
            numbers.append(float(part))
        except ValueError:
            raise ValueError(f"Μη έγκυρος αριθμός: {part!r}")

    if len(numbers) < 2:
        raise ValueError("Χρειάζονται τουλάχιστον 2 αριθμοί για πρόβλεψη.")

    return numbers


def is_arithmetic(numbers, tol=1e-6):
    diffs = np.diff(numbers)
    return len(diffs) > 0 and np.allclose(diffs, diffs[0], atol=tol, rtol=tol)


def is_geometric(numbers, tol=1e-6):
    if len(numbers) < 2:
        return False
    if any(abs(x) < tol for x in numbers[:-1]):
        return False

    ratios = [numbers[i + 1] / numbers[i] for i in range(len(numbers) - 1)]
    return np.allclose(ratios, ratios[0], atol=tol, rtol=tol)


def is_fibonacci(numbers, tol=1e-6):
    if len(numbers) < 3:
        return False
    expected = np.array(numbers[:-2]) + np.array(numbers[1:-1])
    actual = np.array(numbers[2:])
    return np.allclose(expected, actual, atol=tol, rtol=tol)


def arithmetic_prediction(numbers):
    return numbers[-1] + (numbers[-1] - numbers[-2])


def geometric_prediction(numbers):
    return numbers[-1] * (numbers[-1] / numbers[-2])


def fibonacci_prediction(numbers):
    return numbers[-1] + numbers[-2]


def fit_polynomial(numbers, degree):
    x = np.arange(len(numbers))
    y = np.array(numbers)
    coeffs = np.polyfit(x, y, degree)
    y_fit = np.polyval(coeffs, x)
    return coeffs, y_fit


def r2_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot != 0 else 1.0


def predict_with_model(numbers, degree):
    coeffs, y_fit = fit_polynomial(numbers, degree)
    next_x = len(numbers)
    prediction = np.polyval(coeffs, next_x)
    score = r2_score(numbers, y_fit)
    model_name = "Γραμμική με παλινδρόμηση" if degree == 1 else "Πολυωνυμική πρόβλεψη (βαθμού 2)"
    return prediction, score, model_name


def choose_best_model(numbers):
    if is_arithmetic(numbers):
        return arithmetic_prediction(numbers), 1.0, "Αριθμητική πρόοδος"
    if is_geometric(numbers):
        return geometric_prediction(numbers), 1.0, "Γεωμετρική πρόοδος"
    if is_fibonacci(numbers):
        return fibonacci_prediction(numbers), 1.0, "Ακολουθία τύπου Fibonacci"

    linear_pred, linear_score, _ = predict_with_model(numbers, degree=1)
    quad_pred, quad_score = linear_pred, linear_score
    if len(numbers) >= 4:
        quad_pred, quad_score, _ = predict_with_model(numbers, degree=2)

    if len(numbers) >= 4 and quad_score > linear_score + 0.02:
        return quad_pred, quad_score, "Πολυωνυμική πρόβλεψη (βαθμού 2)"

    return linear_pred, linear_score, "Γραμμική με παλινδρόμηση"


def predict_next_number(numbers):
    if len(numbers) < 2:
        raise ValueError("Χρειάζονται τουλάχιστον 2 αριθμοί για πρόβλεψη.")
    return choose_best_model(numbers)


def format_prediction(numbers, prediction, model, score):
    clean_numbers = [int(n) if n == int(n) else n for n in numbers]
    pred_str = f"{prediction:.4f}".rstrip('0').rstrip('.')

    lines = [
        "=== Πρόβλεψη επόμενου αριθμού ===",
        f"Ακολουθία: {clean_numbers}",
        f"Μέθοδος: {model}",
        f"Εμπιστοσύνη: {score:.2%}",
        f"Πρόβλεψη: {pred_str}",
    ]
    return "\n".join(lines)


def launch_gui():
    root = tk.Tk()
    root.title("Predict Next Number")
    root.geometry("560x420")  # Increased height for better spacing
    root.resizable(False, False)
    root.configure(bg="#eaf0f6")

    # --- Styling ---
    style = ttk.Style(root)
    try:
        # Use a modern theme if available (clam, alt, default, classic)
        style.theme_use("clam")
    except tk.TclError:
        # Fallback for older systems
        pass

    # Define a modern font, fallback to system default
    try:
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
    except tk.TclError:
        pass  # Font not found, use default

    # Configure widget styles
    style.configure("TFrame", background="#eaf0f6")
    style.configure("TLabel", background="#eaf0f6", padding=(0, 5))
    style.configure("TButton", padding=8, width=14)
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    # --- Main Frame ---
    frame = ttk.Frame(root, padding="20 20 20 20")
    frame.pack(fill="both", expand=True)
    frame.grid_columnconfigure(0, weight=1)

    # --- Input Widgets ---
    label = ttk.Label(frame, text="Ακολουθία αριθμών (κόμμα ή κενό):")
    label.grid(row=0, column=0, sticky="w")

    seq_var = tk.StringVar(value="2 4 6 8")
    seq_entry = ttk.Entry(frame, textvariable=seq_var, font=("Segoe UI", 11))
    seq_entry.grid(row=1, column=0, sticky="we", pady=(5, 20))
    seq_entry.focus()

    # Δημιουργία μενού δεξιού κλικ (Context Menu)
    def create_context_menu(widget, readonly=False):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Αντιγραφή", command=lambda: widget.event_generate("<<Copy>>"))
        if not readonly:
            menu.add_command(label="Αποκοπή", command=lambda: widget.event_generate("<<Cut>>"))
            menu.add_command(label="Επικόλληση", command=lambda: widget.event_generate("<<Paste>>"))

        def show_menu(event):
            menu.tk_popup(event.x_root, event.y_root)

        widget.bind("<Button-3>", show_menu)  # Κλήση με δεξί κλικ

    create_context_menu(seq_entry, readonly=False)

    # --- Result Area ---
    result_text = tk.Text(frame, height=10, bg="white", fg="#333333",
                          padx=10, pady=10, relief="solid", bd=1,
                          font=("Consolas", 10), wrap="word")
    result_text.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
    result_text.config(state="disabled")

    create_context_menu(result_text, readonly=True)

    # Επιδιόρθωση συντομεύσεων (Ctrl+C/V/X) όταν το πληκτρολόγιο είναι στα Ελληνικά
    for key, action in [("Greek_psi", "<<Copy>>"), ("Greek_omega", "<<Paste>>"), ("Greek_chi", "<<Cut>>"),
                        ("Greek_PSI", "<<Copy>>"), ("Greek_OMEGA", "<<Paste>>"), ("Greek_CHI", "<<Cut>>")]:
        try:
            root.bind(f"<Control-{key}>", lambda e, a=action: e.widget.event_generate(a))
        except tk.TclError:
            pass

    def set_result(message):
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, message)
        result_text.config(state="disabled")

    def predict_action(event=None):
        try:
            numbers = parse_numbers(seq_var.get())
            prediction, score, model = predict_next_number(numbers)
            set_result(format_prediction(numbers, prediction, model, score))
        except Exception as exc:
            set_result(f"Σφάλμα: {exc}")

    # --- Buttons ---
    buttons_frame = ttk.Frame(frame)
    buttons_frame.grid(row=3, column=0, sticky="we")

    predict_button = ttk.Button(buttons_frame, text="Πρόβλεψη", command=predict_action, style="Accent.TButton")
    predict_button.pack(side="left", padx=(0, 10))

    examples = [
        "2 4 6 8",          # Αριθμητική
        "3, 6, 12, 24",     # Γεωμετρική
        "0 1 1 2 3 5 8",    # Fibonacci
        "1 4 9 16 25",      # Τετραγωνική (Πολυωνυμική)
    ]
    example_idx = 0

    def show_next_example():
        nonlocal example_idx
        seq_var.set(examples[example_idx])
        example_idx = (example_idx + 1) % len(examples)

    example_button = ttk.Button(buttons_frame, text="Παραδείγματα", command=show_next_example)
    example_button.pack(side="left", padx=(0, 10))

    close_button = ttk.Button(buttons_frame, text="Κλείσιμο", command=root.destroy)
    close_button.pack(side="right")

    seq_entry.bind("<Return>", predict_action)

    # --- Center the window on screen ---
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


def main():
    launch_gui()


if __name__ == "__main__":
    main()
