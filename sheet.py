import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Gears import SRTConverter  


class SRTConverterApp:
    def __init__(self, hands):
        self.hands = hands
        self.hands.title("SRT Converter")
        self.hands.geometry("460x400")
        self.hands.resizable(False, False)

        # Carpeta Origen
        self.label_input = tk.Label(self.hands, text="Select the folder containing .srt files:")
        self.label_input.pack(pady=5)

        self.entry_input = tk.Entry(self.hands, width=40)
        self.entry_input.pack()

        self.browse_input = tk.Button(self.hands, text="Browse input folder", command=self.select_input_folder)
        self.browse_input.pack(pady=5)

        # Carpeta salida
        self.label_output = tk.Label(self.hands, text="Select destination folder (optional):")
        self.label_output.pack(pady=5)

        self.entry_output = tk.Entry(self.hands, width=40)
        self.entry_output.pack()

        self.browse_output = tk.Button(self.hands, text="Browse output folder", command=self.select_output_folder)
        self.browse_output.pack(pady=5)

        # Formato de salida
        self.format_var = tk.StringVar(value="vtt")
        self.format_menu = tk.OptionMenu(self.hands, self.format_var, "vtt", "txt", "csv")
        self.format_menu.pack(pady=10)

        # Boton
        self.convert_button = tk.Button(self.hands, text="Convert files", command=self.convert_files)
        self.convert_button.pack(pady=10)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, folder)

    def convert_files(self):
        input_folder = self.entry_input.get().strip()
        output_folder = self.entry_output.get().strip()

        if not os.path.isdir(input_folder):
            messagebox.showerror("Error", "The input path is invalid.")
            return

        if output_folder and not os.path.isdir(output_folder):
            messagebox.showerror("Error", "The output path is invalid.")
            return

        output_format = self.format_var.get()
        converter = SRTConverter(input_folder, output_folder if output_folder else None)
        count = converter.convert_all(output_format)

        if count == 0:
            messagebox.showinfo("Finished", "No .srt files were found in the folder.")
        else:
            messagebox.showinfo("Conversion complete", f"{count} file(s) converted successfully.")