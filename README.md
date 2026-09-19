# MASA CineVault Manager

Desktop catalog and database management workstation for films, directors, and reviews

## Technical Architecture

The application is architected with modular separation of concerns adhering to modern clean code standards:

- **Component Layering**: Isolated view layouts, state managers, and service controllers.
- **Defensive Engineering**: Robust input sanitization and exception management.
- **Modern Design Standards**: High-contrast dark-mode interface styled for optimal usability and visual polish.

## Preview

![Application Interface](screenshots/app_interface.png)

## Features

- Full CRUD pipeline managing film titles, genres, release years, and rating scores.
- Search and multi-parameter filtering engine across local SQLite catalog.
- Tabular data table with sortable columns and record selection.
- JSON import and export functionality for library backups.

## Prerequisites

- Python 3.10 or higher
- Required packages:

```bash
pip install customtkinter pillow requests
```

## Execution

Launch the application via Python:

```bash
python "Movie Management System in Python/index.py"
```

## Project Structure

```
.
├── Movie Management System in Python
├── screenshots/
│   └── app_interface.png
├── .gitignore
├── LICENSE             # MIT License
└── README.md           # Developer documentation
```

## License

This project is licensed under the terms of the MIT License. Refer to the `LICENSE` file for details.
