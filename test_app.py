import unittest
from unittest.mock import patch
import tkinter as tk
from app import ModuleGeneratorApp

class TestModuleGeneratorApp(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Tkinter application
        self.app = ModuleGeneratorApp()
        self.app.withdraw()  # Hide the main window during tests

    def tearDown(self):
        self.app.destroy()  # Ensure the application is destroyed after each test

    def test_initial_state(self):
        # Test the initial state of the application
        self.assertEqual(self.app.title(), "Odoo Module Generator")
        self.assertEqual(len(self.app.winfo_children()), 7)  # Adjust the expected number of initial children

    def test_navigate_to_module_info(self):
        # Simulate button click to navigate to Module Info screen
        self.app.main_menu.children['!button'].invoke()  # Click "Start" button
        self.assertEqual(len(self.app.winfo_children()), 7)  # Adjust the expected number of children
        self.assertIsInstance(self.app.module_info_screen, tk.Frame)

    def test_enter_module_info(self):
        # Simulate entering module info and clicking "Next"
        self.app.main_menu.children['!button'].invoke()  # Click "Start" button
        module_info = self.app.module_info_screen

        # Simulate entering data into the entry fields
        module_info.module_name_entry.insert(0, 'test_module')
        module_info.module_version_entry.insert(0, '1.0')
        module_info.module_category_entry.insert(0, 'Uncategorized')
        module_info.module_summary_entry.insert(0, 'Test summary')
        module_info.module_dependencies_entry.insert(0, 'base')

        # Click "Next" button
        module_info.children['!button'].invoke()
        
        self.assertEqual(self.app.module_info['name'], 'test_module')
        self.assertEqual(self.app.module_info['version'], '1.0')
        self.assertEqual(self.app.module_info['category'], 'Uncategorized')
        self.assertEqual(self.app.module_info['summary'], 'Test summary')
        self.assertEqual(self.app.module_info['dependencies'], 'base')
        self.assertIsInstance(self.app.model_info_screen, tk.Frame)

    def test_add_model(self):
        # Simulate adding a model
        self.app.main_menu.children['!button'].invoke()  # Click "Start" button
        self.app.module_info_screen.children['!button'].invoke()  # Click "Next" button after entering module info

        model_info = self.app.model_info_screen

        # Open Add Model window
        model_info.children['!button'].invoke()  # Click "Add Model" button
        add_model_window = model_info.winfo_children()[1]
        model_name_entry = add_model_window.winfo_children()[0].winfo_children()[1]
        model_name_entry.insert(0, 'test_model')  # Enter model name

        # Add a field to the model
        add_model_window.winfo_children()[0].winfo_children()[2].invoke()  # Click "Add Field" button
        add_field_window = add_model_window.winfo_children()[0].winfo_children()[2]
        field_name_entry = add_field_window.winfo_children()[0].winfo_children()[1]
        field_type_entry = add_field_window.winfo_children()[0].winfo_children()[3]
        field_name_entry.insert(0, 'field_name')  # Enter field name
        field_type_entry.insert(0, 'Char')  # Enter field type
        add_field_window.winfo_children()[0].winfo_children()[4].invoke()  # Click "Save Field" button

        # Save the model
        add_model_window.winfo_children()[0].winfo_children()[5].invoke()  # Click "Save Model" button

        self.assertEqual(len(self.app.models), 1)
        self.assertEqual(self.app.models[0]['name'], 'test_model')
        self.assertEqual(len(self.app.models[0]['fields']), 1)
        self.assertEqual(self.app.models[0]['fields'][0]['name'], 'field_name')
        self.assertEqual(self.app.models[0]['fields'][0]['type'], 'Char')

    def test_generate_module(self):
        # Simulate the complete workflow to generate a module
        self.app.main_menu.children['!button'].invoke()  # Click "Start" button
        self.app.module_info_screen.children['!button'].invoke()  # Click "Next" button after entering module info
        self.app.model_info_screen.children['!button2'].invoke()  # Click "Next" button to review screen

        # Click "Confirm" button on the review screen
        self.app.review_screen.children['!button'].invoke()
        result_screen = self.app.result_screen

        self.assertIn("Module", result_screen.message_label.cget("text"))

if __name__ == '__main__':
    unittest.main()
