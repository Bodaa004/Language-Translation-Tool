import tkinter as tk
from googletrans import Translator, LANGUAGES
import customtkinter as ctk

class LanguageTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator")
        
        self.translator = Translator()
        
        self.root.resizable(True, False)    

        self.setup_gui()
        
        self.root.columnconfigure(0, weight=1)

    def setup_gui(self):
        # Title
        self.title = ctk.CTkLabel(self.root, text="Language Translator", font=("Arial",26,"bold"))   
        self.title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        
        # Input text
        self.input_text = ctk.CTkTextbox(self.root, height=100, width=500, font=("Arial",14))
        self.input_text.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        
        # Bind Enter key to translate_text function
        self.input_text.bind("<Return>", self.on_enter)
        # Bind Shift+Return key to move to next line
        self.input_text.bind("<Shift-Return>", self.insert_newline)
        
        # Translate button
        self.translate_button = ctk.CTkButton(self.root, text="Translate", font=("Arial", 14), command=self.translate_text)
        self.translate_button.grid(row=2, column=0, pady=5, sticky="ew")

        # Clear button
        self.clear_button = ctk.CTkButton(self.root, text="Clear", font=("Arial",14),command=self.clear_text)
        self.clear_button.grid(row=2, column=1, pady=5, sticky="ew")

        # Output text
        self.output_text = ctk.CTkTextbox(self.root, height=100, width=500, font=("Arial",14))
        self.output_text.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Source language
        self.src_lang_label = ctk.CTkLabel(self.root, text="Source Language:", font=("Arial",14))
        self.src_lang_label.grid(row=4, column=0, pady=5,padx=10, sticky="w")

        self.src_lang_combo = ctk.CTkComboBox(self.root, values=list(LANGUAGES.values()), state="readonly", font=("Ariel",11))
        self.src_lang_combo.grid(row=4, column=1, pady=10, sticky="ew")
        self.src_lang_combo.set("english")

        # Target language
        self.dest_lang_label = ctk.CTkLabel(self.root, text="Target Language:", font=("Arial",14))
        self.dest_lang_label.grid(row=5, column=0, pady=10,padx=10, sticky="w")

        self.dest_lang_combo = ctk.CTkComboBox(self.root, values=list(LANGUAGES.values()), state="readonly", font=("Ariel",11))
        self.dest_lang_combo.grid(row=5, column=1, pady=20, sticky="ew")
        self.dest_lang_combo.set("arabic")

        # Make components resize with window
        for i in range(2):
            self.root.columnconfigure(i, weight=1)
    
    def translate_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            return

        src_lang = self.src_lang_combo.get()
        dest_lang = self.dest_lang_combo.get()
        
        src_lang_code = [code for code, lang in LANGUAGES.items() if lang == src_lang][0]
        dest_lang_code = [code for code, lang in LANGUAGES.items() if lang == dest_lang][0]

        rtl_languages = ['ar', 'he', 'fa', 'ur', 'yi']  # List of right-to-left languages

        try:
            translation = self.translator.translate(input_text, src=src_lang_code, dest=dest_lang_code)
            self.output_text.delete("1.0", tk.END)
            if dest_lang_code in rtl_languages:
                # Access the underlying tkinter.Text widget
                tk_text_widget = self.output_text._textbox
                # Configure the text tag to align to the right
                tk_text_widget.tag_configure('right', justify='right')
                # Insert the text with right alignment
                tk_text_widget.insert("1.0", translation.text, 'right')
            else:
                self.output_text.insert(tk.END, translation.text)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def on_enter(self, event):
        self.translate_text()
        return "break"  # Prevents the default behavior of adding a new line on Enter
    
    def insert_newline(self, event):
        self.input_text.insert(tk.INSERT, '\n')
        return "break"  # Prevents the default behavior of adding a new line on Shift-Return

if __name__ == "__main__":
    root = ctk.CTk()
    app = LanguageTranslatorApp(root)
    root.mainloop()
