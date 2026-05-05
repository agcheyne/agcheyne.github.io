# Detector UI

This project is a graphical user interface (GUI) for visualizing the channel layout of a detector face. It is designed to run on Linux and provides a simple and intuitive way to display the detector's channel configuration.

UI links:
[Photek Map](https://agcheyne.github.io/detector-ui/)

## Project Structure

```
detector-ui                     # Folder containing the UI project. Defines the address.
├── static                      
│   ├── detector-data.json      # Detector mapping info (generared in app.py from mapping class)
├── app.py                      # Standalone app that can pull info from API
├── index.html                  # The main function that generates the html site
README.md                       # Documentation - Printed on splash page
_config.yml                     # Splash page config file
```

## Installation
No installation needed. Simply visit the site.

## Features

- Visual representation of the detector's channel layout.
- Tools are available for:
  - Finding a pixel channel, and laser position (via click)
  - Look up for laser x,y position. Returns channel, and readout board.
  - Look up a channel position (all or in specific octants)
  - Adding a mask for laser scans, showing defined region of interest.
- Easy to extend and modify for future enhancements, and other detector layouts.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
