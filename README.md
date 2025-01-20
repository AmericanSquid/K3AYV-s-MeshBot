# K3AYV's Meshtastic Scripts

Welcome to K3AYV's Meshtastic Scripts, a collection of Python scripts designed to enhance your experience with Meshtastic devices. These scripts serve various purposes, from automating tasks to extending the functionality of your Meshtastic network.

## Table of Contents

* Introduction

* Features

* Requirements

* Installation

* Usage

* Available Scripts

* Contributing

* License

## Introduction

Meshtastic is an open-source project that enables long-range mesh communication using inexpensive LoRa devices. As a licensed amateur radio operator (K3AYV), I've created this library of Python scripts to:

* Create a modular system of Python scripts to extend the functionality of Meshtastic nodes.

* Provide additional tools to leverage the Meshtastic protocol for creative and practical use cases.

* Support experimentation and learning with LoRa mesh networks.

## Features

* Automated Message Delivery: Scripts to send and receive automated messages across the network.

* Network Monitoring: Tools to monitor and log network activity.

* Custom Data Transmission: Examples of how to send custom data packets for unique applications.

## Requirements

To use these scripts, you'll need:

* A Meshtastic-compatible device (e.g., T-Beam, T-Echo).

* A computer with Python 3.9+ installed.

* The Meshtastic Python API: Meshtastic Python Library.

* Basic knowledge of Python and command-line tools.

## Installation

* Clone this repository:

`git clone https://github.com/K3AYV/meshtastic-scripts.git
cd K3AYV-s-Meshtastic-Scripts`

* Install the required dependencies:

`pip install -r requirements.txt`

* Set up your Meshtastic device and ensure it is paired with your computer.

## Usage

Each script in this repository is designed for a specific purpose. Check the scripts/ folder for available scripts. To run a script:

python3 <script_name>.py

Refer to the documentation within each script for detailed usage instructions and available options.

## Available Scripts

* weather.py: Fetches the current weather for a specified location and broadcasts it over the Meshtastic network. Leverages the OpenWeatherMap API.

## Contributing

Contributions are welcome! If you have an idea for a new script or want to improve existing ones:

* Fork the repository.

* Create a new branch for your feature or fix.

* Submit a pull request with a clear description of your changes.

## Suggestions and Feedback

Feel free to open an issue for any suggestions, bug reports, or general feedback.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as needed, while giving credit to the original author.

Happy Meshing! 🎙️
