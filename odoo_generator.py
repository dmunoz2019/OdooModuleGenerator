import os

class DirectoryManager:
    def __init__(self, module_name):
        self.module_name = module_name

    def create_directory_structure(self):
        os.makedirs(os.path.join(self.module_name, 'models'), exist_ok=True)
        os.makedirs(os.path.join(self.module_name, 'views'), exist_ok=True)
        os.makedirs(os.path.join(self.module_name, 'security'), exist_ok=True)

class FileManager:
    def __init__(self, module_name):
        self.module_name = module_name

    def write_file(self, path, content):
        with open(path, 'w') as f:
            f.write(content)

class InitFileBuilder:
    def __init__(self, module_name, model_names):
        self.module_name = module_name
        self.model_names = model_names

    def build_module_init(self):
        content = 'from . import models\n'
        FileManager(self.module_name).write_file(os.path.join(self.module_name, '__init__.py'), content)

    def build_models_init(self):
        content = ''.join([f'from . import {model_name}\n' for model_name in self.model_names])
        FileManager(self.module_name).write_file(os.path.join(self.module_name, 'models', '__init__.py'), content)

class ManifestBuilder:
    def __init__(self, module_name, model_names):
        self.module_name = module_name
        self.model_names = model_names

    def build_manifest(self):
        manifest_content = f"""
{{
    'name': '{self.module_name}',
    'version': '1.0',
    'category': 'Category',
    'summary': 'Summary',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
"""
        for model_name in self.model_names:
            manifest_content += f"        'views/{model_name}_views.xml',\n"
        manifest_content += """    ],
    'installable': True,
    'application': True,
}}
"""
        FileManager(self.module_name).write_file(os.path.join(self.module_name, '__manifest__.py'), manifest_content)

class ModelBuilder:
    def __init__(self, module_name, model_name, fields):
        self.module_name = module_name
        self.model_name = model_name
        self.fields = fields

    def build_model_file(self):
        fields_str = ''.join([f"    {field_name} = fields.{field_type}(string='{field_name.capitalize()}')\n" for field_name, field_type in self.fields.items()])
        model_content = f"""
from odoo import fields, models

class {self.model_name.capitalize()}(models.TransientModel):
    \"\"\"This model is used for {self.model_name.replace('_', ' ')}.\"\"\"
    _name = '{self.model_name}'
    _description = "{self.model_name.replace('_', ' ').capitalize()}"

{fields_str}
"""
        FileManager(self.module_name).write_file(os.path.join(self.module_name, 'models', f'{self.model_name}.py'), model_content)

class ViewBuilder:
    def __init__(self, module_name, model_name, fields):
        self.module_name = module_name
        self.model_name = model_name
        self.fields = fields

    def build_view_file(self):
        fields_str = ''.join([f"                    <field name='{field_name}'/>\n" for field_name in self.fields.keys()])
        view_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="{self.model_name}_view_form" model="ir.ui.view">
        <field name="name">{self.model_name}.view.form</field>
        <field name="model">{self.model_name}</field>
        <field name="priority" eval="8"/>
        <field name="arch" type="xml">
            <form string="{self.model_name.replace('_', ' ').capitalize()}">
                <group>
{fields_str}                </group>
                <footer>
                    <button name="action_confirm" string="Confirm" type="object" class="btn-primary"/>
                    <button name="cancel" string="Cancel" special="cancel" class="btn-secondary"/>
                </footer>
            </form>
        </field>
    </record>
</odoo>
"""
        FileManager(self.module_name).write_file(os.path.join(self.module_name, 'views', f'{self.model_name}_views.xml'), view_content)

class SecurityBuilder:
    def __init__(self, module_name, model_names):
        self.module_name = module_name
        self.model_names = model_names

    def build_security_file(self):
        security_content = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
        for model_name in self.model_names:
            security_content += f"access_{model_name},access_{model_name},model_{model_name},,1,1,1,1\n"
        FileManager(self.module_name).write_file(os.path.join(self.module_name, 'security', 'ir.model.access.csv'), security_content)

class OdooModuleGenerator:
    def __init__(self, module_name):
        self.module_name = module_name
        self.model_names = []
        self.model_fields = {}

    def get_model_details(self):
        num_models = int(input("Enter the number of models: "))
        for _ in range(num_models):
            model_name = input("Enter the model name: ")
            self.model_names.append(model_name)
            fields = {}
            while True:
                field_name = input(f"Enter the field name for model {model_name} (or 'done' to finish): ")
                if field_name.lower() == 'done':
                    break
                field_type = input(f"Enter the field type for {field_name} (e.g., Char, Text, Many2one): ")
                fields[field_name] = field_type
            self.model_fields[model_name] = fields

    def generate_module(self):
        try:
            directory_manager = DirectoryManager(self.module_name)
            directory_manager.create_directory_structure()

            init_builder = InitFileBuilder(self.module_name, self.model_names)
            init_builder.build_module_init()
            init_builder.build_models_init()

            manifest_builder = ManifestBuilder(self.module_name, self.model_names)
            manifest_builder.build_manifest()

            for model_name in self.model_names:
                model_builder = ModelBuilder(self.module_name, model_name, self.model_fields[model_name])
                model_builder.build_model_file()

                view_builder = ViewBuilder(self.module_name, model_name, self.model_fields[model_name])
                view_builder.build_view_file()

            security_builder = SecurityBuilder(self.module_name, self.model_names)
            security_builder.build_security_file()

            return f"Module {self.module_name} has been created successfully."
        except Exception as e:
            return str(e)
