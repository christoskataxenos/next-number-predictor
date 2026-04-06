import tkinter as tk
import customtkinter as ctk
import numpy as np


# --- Ρυθμίσεις Πολυγλωσσίας (Multilingual) ---
current_lang = "en"

translations = {
    "en": {
        "err_no_nums": "No numbers provided.",
        "err_invalid_num": "Invalid number: ",
        "err_min_nums": "At least 2 numbers are required for prediction.",
        "mod_arithmetic": "Arithmetic progression",
        "mod_geometric": "Geometric progression",
        "mod_fibonacci": "Fibonacci-like sequence",
        "mod_linear": "Linear regression",
        "mod_poly": "Polynomial prediction (degree 2)",
        "res_title": "=== Next Number Prediction ===",
        "res_seq": "Sequence:",
        "res_method": "Method:",
        "res_conf": "Confidence:",
        "res_pred": "Prediction:",
        "gui_title": "Predict Next Number",
        "gui_prompt": "Number sequence (comma or space):",
        "gui_btn_predict": "Predict",
        "gui_btn_examples": "Examples",
        "gui_btn_close": "Close",
        "gui_btn_lang": "Ελληνικά",
        "gui_ctx_copy": "Copy",
        "gui_ctx_cut": "Cut",
        "gui_ctx_paste": "Paste",
        "gui_err_prefix": "Error: "
    },
    "el": {
        "err_no_nums": "Δεν δόθηκαν αριθμοί.",
        "err_invalid_num": "Μη έγκυρος αριθμός: ",
        "err_min_nums": "Χρειάζονται τουλάχιστον 2 αριθμοί για πρόβλεψη.",
        "mod_arithmetic": "Αριθμητική πρόοδος",
        "mod_geometric": "Γεωμετρική πρόοδος",
        "mod_fibonacci": "Ακολουθία τύπου Fibonacci",
        "mod_linear": "Γραμμική με παλινδρόμηση",
        "mod_poly": "Πολυωνυμική πρόβλεψη (βαθμού 2)",
        "res_title": "=== Πρόβλεψη επόμενου αριθμού ===",
        "res_seq": "Ακολουθία:",
        "res_method": "Μέθοδος:",
        "res_conf": "Εμπιστοσύνη:",
        "res_pred": "Πρόβλεψη:",
        "gui_title": "Πρόβλεψη Επόμενου Αριθμού",
        "gui_prompt": "Ακολουθία αριθμών (κόμμα ή κενό):",
        "gui_btn_predict": "Πρόβλεψη",
        "gui_btn_examples": "Παραδείγματα",
        "gui_btn_close": "Κλείσιμο",
        "gui_btn_lang": "English",
        "gui_ctx_copy": "Αντιγραφή",
        "gui_ctx_cut": "Αποκοπή",
        "gui_ctx_paste": "Επικόλληση",
        "gui_err_prefix": "Σφάλμα: "
    }
}

def get_text(key):
    """Επιστρέφει το μεταφρασμένο κείμενο με βάση την τρέχουσα γλώσσα."""
    return translations[current_lang].get(key, key)


def parse_numbers(text):
    """Μετατρέπει κείμενο εισόδου σε λίστα αριθμών."""
    text = text.replace(',', ' ').strip()
    if not text:
        raise ValueError(get_text("err_no_nums"))

    parts = text.split()
    numbers = []
    for part in parts:
        try:
            numbers.append(float(part))
        except ValueError:
            raise ValueError(f"{get_text('err_invalid_num')}{part!r}")

    if len(numbers) < 2:
        raise ValueError(get_text("err_min_nums"))

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
    model_name = get_text("mod_linear") if degree == 1 else get_text("mod_poly")
    return prediction, score, model_name


def choose_best_model(numbers):
    if is_arithmetic(numbers):
        return arithmetic_prediction(numbers), 1.0, get_text("mod_arithmetic")
    if is_geometric(numbers):
        return geometric_prediction(numbers), 1.0, get_text("mod_geometric")
    if is_fibonacci(numbers):
        return fibonacci_prediction(numbers), 1.0, get_text("mod_fibonacci")

    linear_pred, linear_score, _ = predict_with_model(numbers, degree=1)
    quad_pred, quad_score = linear_pred, linear_score
    if len(numbers) >= 4:
        quad_pred, quad_score, _ = predict_with_model(numbers, degree=2)

    if len(numbers) >= 4 and quad_score > linear_score + 0.02:
        return quad_pred, quad_score, get_text("mod_poly")

    return linear_pred, linear_score, get_text("mod_linear")


def predict_next_number(numbers):
    if len(numbers) < 2:
        raise ValueError(get_text("err_min_nums"))
    return choose_best_model(numbers)


def format_prediction(numbers, prediction, model, score):
    clean_numbers = [int(n) if n == int(n) else n for n in numbers]
    pred_str = f"{prediction:.4f}".rstrip('0').rstrip('.')

    lines = [
        get_text("res_title"),
        f"{get_text('res_seq')} {clean_numbers}",
        f"{get_text('res_method')} {model}",
        f"{get_text('res_conf')} {score:.2%}",
        f"{get_text('res_pred')} {pred_str}",
    ]
    return "\n".join(lines)


def launch_gui():
    # --- Αρχικοποίηση CustomTkinter ---
    ctk.set_appearance_mode("light")  # Μόνο Light Mode όπως ζητήθηκε
    ctk.set_default_color_theme("blue")  # Μοντέρνο μπλε θέμα

    root = ctk.CTk()
    root.title(get_text("gui_title"))
    root.geometry("600x480")
    root.resizable(False, False)

    # --- Fonts ---
    primary_font = ("Segoe UI", 13)
    header_font = ("Segoe UI", 15, "bold")
    mono_font = ("Consolas", 12)

    # --- Main Container ---
    main_frame = ctk.CTkFrame(root, corner_radius=15)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Input Section ---
    label = ctk.CTkLabel(main_frame, text=get_text("gui_prompt"), font=header_font)
    label.pack(anchor="w", padx=20, pady=(20, 5))

    seq_var = tk.StringVar(value="2 4 6 8")
    seq_entry = ctk.CTkEntry(main_frame, textvariable=seq_var, font=primary_font, height=40, corner_radius=10)
    seq_entry.pack(fill="x", padx=20, pady=(0, 20))
    seq_entry.focus()

    # --- Result Area ---
    result_text = ctk.CTkTextbox(main_frame, height=180, font=mono_font, corner_radius=10, border_width=1)
    result_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    result_text.configure(state="disabled")

    # --- Context Menu (Δεξί Κλικ) ---
    def create_context_menu(widget, readonly=False):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label=get_text("gui_ctx_copy"), command=lambda: widget.event_generate("<<Copy>>"))
        if not readonly:
            menu.add_command(label=get_text("gui_ctx_cut"), command=lambda: widget.event_generate("<<Cut>>"))
            menu.add_command(label=get_text("gui_ctx_paste"), command=lambda: widget.event_generate("<<Paste>>"))

        def show_menu(event):
            menu.tk_popup(event.x_root, event.y_root)

        widget.bind("<Button-3>", show_menu)

    create_context_menu(seq_entry._entry, readonly=False) # CTkEntry has a hidden standard entry inside
    create_context_menu(result_text, readonly=True)

    # Επιδιόρθωση συντομεύσεων (Ctrl+C/V/X) για ελληνικά πληκτρολόγια
    for key, action in [("Greek_psi", "<<Copy>>"), ("Greek_omega", "<<Paste>>"), ("Greek_chi", "<<Cut>>"),
                        ("Greek_PSI", "<<Copy>>"), ("Greek_OMEGA", "<<Paste>>"), ("Greek_CHI", "<<Cut>>")]:
        try:
            root.bind(f"<Control-{key}>", lambda e, a=action: e.widget.event_generate(a))
        except tk.TclError:
            pass

    def set_result(message):
        result_text.configure(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, message)
        result_text.configure(state="disabled")

    def predict_action(event=None):
        try:
            numbers = parse_numbers(seq_var.get())
            prediction, score, model = predict_next_number(numbers)
            set_result(format_prediction(numbers, prediction, model, score))
        except Exception as exc:
            set_result(f"{get_text('gui_err_prefix')}{exc}")

    # --- Buttons Section ---
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

    predict_button = ctk.CTkButton(buttons_frame, command=predict_action, text=get_text("gui_btn_predict"), 
                                   font=header_font, height=40, corner_radius=10)
    predict_button.pack(side="left", padx=(0, 10), expand=True, fill="x")

    examples = ["2 4 6 8", "3, 6, 12, 24", "0 1 1 2 3 5 8", "1 4 9 16 25"]
    example_idx = 0

    def show_next_example():
        nonlocal example_idx
        seq_var.set(examples[example_idx])
        example_idx = (example_idx + 1) % len(examples)

    example_button = ctk.CTkButton(buttons_frame, command=show_next_example, text=get_text("gui_btn_examples"),
                                    font=primary_font, height=40, corner_radius=10, fg_color="#607D8B", hover_color="#455A64")
    example_button.pack(side="left", padx=(0, 10))

    # --- Bottom Controls ---
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    bottom_frame.pack(fill="x", padx=20, pady=(0, 10))

    def toggle_language():
        global current_lang
        current_lang = "el" if current_lang == "en" else "en"
        update_texts()

    lang_button = ctk.CTkButton(bottom_frame, command=toggle_language, text=get_text("gui_btn_lang"),
                                font=primary_font, height=35, corner_radius=10, fg_color="transparent", 
                                border_width=1, text_color=("#333333", "#DCE4EE"), border_color=("#A9A9A9", "#2A2D2E"))
    lang_button.pack(side="left")

    close_button = ctk.CTkButton(bottom_frame, command=root.destroy, text=get_text("gui_btn_close"),
                                 font=primary_font, height=35, corner_radius=10, fg_color="#f44336", hover_color="#d32f2f")
    close_button.pack(side="right")

    def update_texts():
        root.title(get_text("gui_title"))
        label.configure(text=get_text("gui_prompt"))
        predict_button.configure(text=get_text("gui_btn_predict"))
        example_button.configure(text=get_text("gui_btn_examples"))
        close_button.configure(text=get_text("gui_btn_close"))
        lang_button.configure(text=get_text("gui_btn_lang"))

    update_texts()
    seq_entry.bind("<Return>", predict_action)

    # --- Center the window ---
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
