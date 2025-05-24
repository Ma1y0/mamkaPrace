import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

import pandas as pd

from lib import transform_table


class ExcelFileSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Výběr Excel souborů")
        self.root.geometry("750x900")
        self.root.minsize(750, 900)

        self.selected_files = []

        self.create_widgets()

    def create_widgets(self):
        # Define fonts
        title_font = ctk.CTkFont(size=26, weight="bold")
        label_font = ctk.CTkFont(size=18)
        button_font = ctk.CTkFont(size=18)

        # Title label
        title_label = ctk.CTkLabel(
            self.root, text="Výběr Excel souborů", font=title_font
        )
        title_label.pack(pady=16)

        # Instructions label
        instructions = ctk.CTkLabel(
            self.root, text="Vyberte jeden nebo více Excel souborů (*.xls)", font=label_font
        )
        instructions.pack(pady=10)

        # Button to select files
        select_button = ctk.CTkButton(
            self.root, text="Vybrat Excel soubory", command=self.select_files, font=button_font
        )
        select_button.pack(pady=20, padx=20)

        # Frame for the listbox and scrollbar
        list_frame = ctk.CTkFrame(self.root)
        list_frame.pack(fill=ctk.BOTH, expand=True, padx=24, pady=14)

        # Listbox to display selected files
        self.file_listbox = ctk.CTkTextbox(
            list_frame, height=8, width=60, state="disabled", font=label_font
        )
        self.file_listbox.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Button frame for bottom buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(fill=ctk.X, pady=14)

        # Remove selected file button
        remove_button = ctk.CTkButton(
            button_frame, text="Odebrat poslední", command=self.remove_selected, font=button_font
        )
        remove_button.pack(side=ctk.LEFT, padx=38, pady=10)

        # Clear all button
        clear_button = ctk.CTkButton(
            button_frame, text="Vymazat vše", command=self.clear_files, font=button_font
        )
        clear_button.pack(side=ctk.LEFT, padx=38, pady=10)

        # Process button
        process_button = ctk.CTkButton(
            button_frame, text="Zpracovat soubory", command=self.process_files, font=button_font
        )
        process_button.pack(side=ctk.RIGHT, padx=38, pady=10)

    def update_listbox(self):
        self.file_listbox.configure(state="normal")
        self.file_listbox.delete("1.0", ctk.END)
        for i, file_path in enumerate(self.selected_files):
            self.file_listbox.insert(ctk.END, f"{i+1}. {os.path.basename(file_path)}\n")
        self.file_listbox.configure(state="disabled")

    def select_files(self):
        file_types = [
            ("Excel soubory", "*.xls"),
        ]
        new_files = filedialog.askopenfilenames(
            title="Vyberte Excel soubory", filetypes=file_types
        )
        if new_files:
            for file_path in new_files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            self.update_listbox()

    def remove_selected(self):
        if self.selected_files:
            self.selected_files.pop()
            self.update_listbox()

    def clear_files(self):
        self.selected_files = []
        self.update_listbox()

    def process_files(self):
        if not self.selected_files:
            messagebox.showinfo(
                "Nebyly vybrány žádné soubory", "Vyberte alespoň jeden Excel soubor."
            )
            return

        save_path = filedialog.asksaveasfilename(
            title="Uložit jako",
            defaultextension=".xlsx",
            filetypes=[("Excel soubor", "*.xlsx")],
            initialfile="output.xlsx"
        )
        if not save_path:
            return  # User cancelled

        try:
            processed_files = [transform_table(i) for i in self.selected_files]
            big_table = pd.concat(processed_files, ignore_index=True)
            big_table.to_excel(save_path, index=False)
            messagebox.showinfo(
                "Zpracováno",
                f"Úspěšně zpracováno {len(processed_files)} souborů.\n\nVýsledek uložen jako {os.path.basename(save_path)}",
            )
        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba: {e}")


def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = ExcelFileSelector(root)
    root.mainloop()


if __name__ == "__main__":
    main()
