import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, messagebox
import customtkinter
import requests
from config import API_BASE_URL

customtkinter.set_default_color_theme("blue")
customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.title("Sentiment & Morse Client")

input_label = ttk.Label(root, text="Enter text:", background='grey10', foreground='white')
input_label.pack()

input_box = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, background='grey10', foreground='white')
input_box.pack()

output_label = customtkinter.CTkLabel(root, text="Result:")
output_label.pack()

output_box = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, state="disabled", background='grey10', foreground='white')
output_box.pack()

def show_output(text):
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", text)
    output_box.config(state="disabled")

def analyze():
    text = input_box.get("1.0", "end-1c")
    if not text.strip():
        return messagebox.showerror("Error", "Please enter some text.")
    try:
        response = requests.post(f"{API_BASE_URL}/analyze", json={"text": text})
        data = response.json()
        if response.ok:
            show_output(data)
        else:
            show_output(data.get("error", "Something went wrong."))
    except Exception as e:
        show_output(f"Error: {e}")

def morse():
    text = input_box.get("1.0", "end-1c")
    if not text.strip():
        return messagebox.showerror("Error", "Please enter some text.")
    try:
        response = requests.post(f"{API_BASE_URL}/morse", json={"text": text})
        data = response.json()
        if response.ok:
            show_output(data["morse"])
        else:
            show_output(data.get("error", "Something went wrong."))
    except Exception as e:
        show_output(f"Error: {e}")

def save_result():
    text = output_box.get("1.0", "end-1c")
    if not text.strip():
        return messagebox.showinfo("Nothing to save", "No analysis result found.")
    try:
        response = requests.post(f"{API_BASE_URL}/save", json={"content": text})
        data = response.json()
        if response.ok:
            messagebox.showinfo("Success", data.get("message", "Saved."))
        else:
            messagebox.showerror("Error", data.get("error", "Could not save."))
    except Exception as e:
        messagebox.showerror("Error", str(e))

analyze_button = customtkinter.CTkButton(root, text="Analyze Sentiment", command=analyze)
analyze_button.pack(pady=5)

morse_button = customtkinter.CTkButton(root, text="Convert to Morse", command=morse)
morse_button.pack(pady=5)

save_button = customtkinter.CTkButton(root, text="Save Result", command=save_result)
save_button.pack(pady=5)

root.mainloop()

