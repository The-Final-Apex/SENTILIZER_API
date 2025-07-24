import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import customtkinter
import requests
from config import API_BASE_URL, API_KEY

# Appearance
customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

# === Root window ===
root = customtkinter.CTk()
root.title("Sentiment & Morse API Client")
root.geometry("700x600")

# === Headers for requests ===
HEADERS = {"x-api-key": API_KEY}

# === Widgets ===
input_label = ttk.Label(root, text="Enter your text:", background="grey10", foreground="white")
input_label.pack(pady=(10, 0))

input_box = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, background="grey10", foreground="white")
input_box.pack(padx=10, pady=5, fill="x")

output_label = customtkinter.CTkLabel(root, text="Output:")
output_label.pack(pady=(10, 0))

output_box = scrolledtext.ScrolledText(root, height=12, wrap=tk.WORD, background="grey10", foreground="white", state="disabled")
output_box.pack(padx=10, pady=5, fill="x")

# === Helpers ===
def show_output(text):
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", text)
    output_box.config(state="disabled")

def get_input_text():
    return input_box.get("1.0", "end-1c").strip()

def make_request(endpoint, payload):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload, headers=HEADERS)
        if response.ok:
            return response.json()
        return {"error": response.json().get("error", "Something went wrong.")}
    except Exception as e:
        return {"error": str(e)}

# === API actions ===
def analyze():
    text = get_input_text()
    if not text:
        return messagebox.showerror("Error", "Please enter some text.")
    result = make_request("/analyze", {"text": text})
    show_output(result)

def analyze_all():
    text = get_input_text()
    if not text:
        return messagebox.showerror("Error", "Please enter some text.")
    result = make_request("/analyze_all", {"text": text})
    show_output(result)

def morse():
    text = get_input_text()
    if not text:
        return messagebox.showerror("Error", "Please enter some text.")
    result = make_request("/morse", {"text": text})
    show_output(result.get("morse", result))

def translate():
    text = get_input_text()
    if not text:
        return messagebox.showerror("Error", "Please enter some text.")
    target = translate_lang_entry.get().strip()
    if not target:
        return messagebox.showerror("Error", "Please enter target language (e.g. 'en', 'fr').")
    result = make_request("/translate", {"text": text, "target": target})
    show_output(result)

def save_result():
    text = output_box.get("1.0", "end-1c").strip()
    if not text:
        return messagebox.showinfo("Nothing to save", "No analysis result found.")
    result = make_request("/save", {"content": text})
    if "message" in result:
        messagebox.showinfo("Success", result["message"])
    else:
        messagebox.showerror("Error", result.get("error", "Failed to save."))

# === Buttons ===
button_frame = customtkinter.CTkFrame(root)
button_frame.pack(pady=10)

customtkinter.CTkButton(button_frame, text="Analyze Sentiment", command=analyze).grid(row=0, column=0, padx=5, pady=5)
customtkinter.CTkButton(button_frame, text="Analyze + Clean", command=analyze_all).grid(row=0, column=1, padx=5, pady=5)
customtkinter.CTkButton(button_frame, text="Morse Code", command=morse).grid(row=0, column=2, padx=5, pady=5)
customtkinter.CTkButton(button_frame, text="Save Result", command=save_result).grid(row=0, column=3, padx=5, pady=5)

# === Translation Input ===
translate_frame = customtkinter.CTkFrame(root)
translate_frame.pack(pady=5)

translate_label = customtkinter.CTkLabel(translate_frame, text="Translate to (e.g. 'en'):")
translate_label.pack(side="left", padx=5)

translate_lang_entry = customtkinter.CTkEntry(translate_frame, width=80)
translate_lang_entry.pack(side="left", padx=5)

customtkinter.CTkButton(translate_frame, text="Translate", command=translate).pack(side="left", padx=5)

# === Run ===
root.mainloop()

