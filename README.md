### README.md

```markdown
# Odoo Module Generator

Odoo Module Generator is a Tkinter-based GUI application designed to facilitate the creation of Odoo modules. This application allows users to define module information, add models and fields, and generate the necessary files and structure for an Odoo module.

## Features

- User-friendly interface to create Odoo modules.
- Define module information (name, version, category, summary, dependencies).
- Add multiple models with fields to the module.
- Automatically generate the necessary files (`__init__.py`, `__manifest__.py`, model files, views, and security files).
- Review and confirm module details before generation.

## Prerequisites

- Python 3.6 or higher.
- Tkinter (usually included with Python).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dmunoz2019/OdooModuleGenerator.git
    cd OdooModuleGenerator
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. Install dependencies (if any):

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Follow the steps in the GUI to create your Odoo module:
    - Click **Start** to begin.
    - Enter module information (name, version, category, summary, dependencies).
    - Add models and their respective fields.
    - Review and confirm the module details.
    - Generate the module.

## Application Structure

- `app.py`: Main application file containing the Tkinter GUI.
- `odoo_generator.py`: Contains classes for generating the Odoo module files and structure.
- `tests/test_app.py`: Unit tests for the application.

## Code Overview

### `app.py`

This file defines the Tkinter GUI application. Key classes include:

- `ModuleGeneratorApp`: Main application class.
- `MainMenu`: Frame for the main menu.
- `ModuleInfo`: Frame for entering module information.
- `ModelInfo`: Frame for adding models and fields.
- `Review`: Frame for reviewing and confirming module details.
- `Result`: Frame displaying the result of the module generation.
- `Help`: Frame providing help/documentation.

### `odoo_generator.py`

This file contains classes for generating the various files needed for an Odoo module:

- `DirectoryManager`: Creates the directory structure for the module.
- `FileManager`: Writes content to files.
- `InitFileBuilder`: Generates `__init__.py` files.
- `ManifestBuilder`: Generates `__manifest__.py`.
- `ModelBuilder`: Generates model files.
- `ViewBuilder`: Generates view XML files.
- `SecurityBuilder`: Generates security access CSV files.
- `OdooModuleGenerator`: Orchestrates the module generation process.

### `tests/test_app.py`

Contains unit tests for the Tkinter application using the `unittest` module. Tests include:

- Initial state of the application.
- Navigation between frames.
- Entering module information.
- Adding models and fields.
- Generating the module.

## Running Tests

To run the tests, use:

```bash
pytest tests/test_app.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [dmunoz2019@gmail.com].
```

### Explanation

1. **Repository Link**: Updated the clone command to use your GitHub repository link.
2. **Contact Information**: Included a generic email for contact; replace it with your actual email if necessary.

### Additional Steps

1. **Create `requirements.txt`**:
   If you have dependencies, list them in a `requirements.txt` file. For example:
   ```txt
   pytest
   pytest-mock
   ```

2. **Create `LICENSE` File**:
   Add a `LICENSE` file to your repository if you haven't already, to specify the licensing terms for your project.
