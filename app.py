import tkinter as tk
from tkinter import ttk
from odoo_generator import OdooModuleGenerator

class ModuleGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Odoo Module Generator")
        self.geometry("400x400")

        self.module_info = {'name': '', 'version': '', 'category': '', 'summary': '', 'dependencies': ''}
        self.models = []

        self.main_menu = MainMenu(self)
        self.module_info_screen = ModuleInfo(self)
        self.model_info_screen = ModelInfo(self)
        self.review_screen = Review(self)
        self.result_screen = Result(self)
        self.help_screen = Help(self)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_screen()
        self.main_menu.pack(fill="both", expand=True)

    def show_module_info(self):
        self.clear_screen()
        self.module_info_screen.pack(fill="both", expand=True)

    def show_model_info(self):
        self.clear_screen()
        self.model_info_screen.pack(fill="both", expand=True)

    def show_review(self):
        self.update_review_screen()
        self.clear_screen()
        self.review_screen.pack(fill="both", expand=True)

    def show_result(self, message):
        self.clear_screen()
        self.result_screen.set_message(message)
        self.result_screen.pack(fill="both", expand=True)

    def show_help(self):
        self.clear_screen()
        self.help_screen.pack(fill="both", expand=True)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def generate_module(self):
        generator = OdooModuleGenerator(self.module_info['name'])
        generator.model_names = [model['name'] for model in self.models]
        generator.model_fields = {model['name']: {field['name']: field['type']} for model in self.models}
        result_message = generator.generate_module()
        self.show_result(result_message)

    def update_review_screen(self):
        self.review_screen.update_widgets()


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Odoo Module Generator", font=("Arial", 18)).pack(pady=10)
        tk.Button(self, text="Start", command=self.master.show_module_info).pack(pady=5)
        tk.Button(self, text="Help", command=self.master.show_help).pack(pady=5)
        tk.Button(self, text="Exit", command=self.master.quit).pack(pady=5)


class ModuleInfo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Module Information", font=("Arial", 18)).pack(pady=10)
        
        tk.Label(self, text="Module Name:").pack(anchor="w")
        self.module_name_entry = tk.Entry(self)
        self.module_name_entry.pack(fill="x")
        
        tk.Label(self, text="Version:").pack(anchor="w")
        self.module_version_entry = tk.Entry(self)
        self.module_version_entry.pack(fill="x")
        
        tk.Label(self, text="Category:").pack(anchor="w")
        self.module_category_entry = tk.Entry(self)
        self.module_category_entry.pack(fill="x")
        
        tk.Label(self, text="Summary:").pack(anchor="w")
        self.module_summary_entry = tk.Entry(self)
        self.module_summary_entry.pack(fill="x")
        
        tk.Label(self, text="Dependencies (comma separated):").pack(anchor="w")
        self.module_dependencies_entry = tk.Entry(self)
        self.module_dependencies_entry.pack(fill="x")
        
        tk.Button(self, text="Next", command=self.save_and_next).pack(pady=10)
    
    def save_and_next(self):
        self.master.module_info = {
            'name': self.module_name_entry.get(),
            'version': self.module_version_entry.get(),
            'category': self.module_category_entry.get(),
            'summary': self.module_summary_entry.get(),
            'dependencies': self.module_dependencies_entry.get(),
        }
        self.master.show_model_info()


class ModelInfo(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Model Information", font=("Arial", 18)).pack(pady=10)

        self.models = []

        tk.Button(self, text="Add Model", command=self.add_model_screen).pack(pady=5)
        tk.Button(self, text="Next", command=self.master.show_review).pack(pady=10)

    def add_model_screen(self):
        new_model_window = tk.Toplevel(self)
        new_model_window.title("Add Model")

        frame = tk.Frame(new_model_window)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Model Name:").pack(anchor="w")
        model_name_entry = tk.Entry(frame)
        model_name_entry.pack(fill="x")

        fields = []

        def add_field_screen():
            new_field_window = tk.Toplevel(new_model_window)
            new_field_window.title("Add Field")

            frame = tk.Frame(new_field_window)
            frame.pack(padx=10, pady=10)

            tk.Label(frame, text="Field Name:").pack(anchor="w")
            field_name_entry = tk.Entry(frame)
            field_name_entry.pack(fill="x")

            tk.Label(frame, text="Field Type:").pack(anchor="w")
            field_type_entry = tk.Entry(frame)
            field_type_entry.pack(fill="x")

            def save_field():
                field_name = field_name_entry.get()
                field_type = field_type_entry.get()
                fields.append({"name": field_name, "type": field_type})
                new_field_window.destroy()

            tk.Button(frame, text="Save Field", command=save_field).pack(pady=10)

        tk.Button(frame, text="Add Field", command=add_field_screen).pack(pady=5)

        def save_model():
            model_name = model_name_entry.get()
            self.master.models.append({"name": model_name, "fields": fields})
            new_model_window.destroy()

        tk.Button(frame, text="Save Model", command=save_model).pack(pady=10)


class Review(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.module_info_frame = tk.Frame(self)
        self.module_info_frame.pack(pady=10)
        
        self.models_frame = tk.Frame(self)
        self.models_frame.pack(pady=10)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        tk.Button(self.buttons_frame, text="Confirm", command=self.master.generate_module).pack(side="left", padx=5)
        tk.Button(self.buttons_frame, text="Back", command=self.master.show_model_info).pack(side="left", padx=5)

    def update_widgets(self):
        for widget in self.module_info_frame.winfo_children():
            widget.destroy()
        for widget in self.models_frame.winfo_children():
            widget.destroy()

        tk.Label(self.module_info_frame, text="Review and Confirm", font=("Arial", 18)).pack(pady=10)
        
        tk.Label(self.module_info_frame, text=f"Module Name: {self.master.module_info['name']}").pack(anchor="w")
        tk.Label(self.module_info_frame, text=f"Version: {self.master.module_info['version']}").pack(anchor="w")
        tk.Label(self.module_info_frame, text=f"Category: {self.master.module_info['category']}").pack(anchor="w")
        tk.Label(self.module_info_frame, text=f"Summary: {self.master.module_info['summary']}").pack(anchor="w")
        tk.Label(self.module_info_frame, text=f"Dependencies: {self.master.module_info['dependencies']}").pack(anchor="w")
        
        for model in self.master.models:
            tk.Label(self.models_frame, text=f"Model Name: {model['name']}").pack(anchor="w")
            for field in model["fields"]:
                tk.Label(self.models_frame, text=f"  Field Name: {field['name']}, Field Type: {field['type']}").pack(anchor="w")


class Result(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.message_label = tk.Label(self, text="", font=("Arial", 18))
        self.message_label.pack(pady=10)
        tk.Button(self, text="Main Menu", command=self.master.show_main_menu).pack(pady=10)
        tk.Button(self, text="Exit", command=self.master.quit).pack(pady=5)

    def set_message(self, message):
        self.message_label.config(text=message)


class Help(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Help/Documentation", font=("Arial", 18)).pack(pady=10)
        tk.Label(self, text="Instructions on how to use the Odoo Module Generator...").pack(pady=5)
        tk.Button(self, text="Back", command=self.master.show_main_menu).pack(pady=10)


if __name__ == "__main__":
    app = ModuleGeneratorApp()
    app.mainloop()
