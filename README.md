# Detector UI

This project is a graphical user interface (GUI) for visualizing the channel layout of a detector face. It is designed to run on Linux and provides a simple and intuitive way to display the detector's channel configuration.

UI links:
[Photek Map](https://agcheyne.github.io/detector-ui/)

## Project Structure

```
detector-ui
├── src
│   ├── main.py          # Entry point of the application
│   ├── ui               # Contains UI components
│   │   ├── canvas.py    # Renders the detector face layout
│   │   ├── window.py     # Creates the main application window
│   │   └── __init__.py   # Marks the ui directory as a package
│   ├── detector         # Contains detector-related logic
│   │   ├── layout.py    # Defines the channel layout for the detector
│   │   └── __init__.py   # Marks the detector directory as a package
│   └── utils            # Contains utility functions and configurations
│       ├── config.py    # Configuration settings for the application
│       └── __init__.py   # Marks the utils directory as a package
├── requirements.txt     # Lists project dependencies
├── setup.py             # Packaging information for the application
└── README.md            # Documentation for the project
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd detector-ui
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
python src/main.py
```

This will launch the GUI, displaying the detector face and its channel layout.

## Features

- Visual representation of the detector's channel layout.
- Modular design with separate components for UI, detector logic, and utilities.
- Easy to extend and modify for future enhancements.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
