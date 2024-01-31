# Dashboars cheking with Looker API

This is the first version of the application that allows you to perform dashboards on errors loading data from the database

## Installation

Follow these steps to set up your environment and run the application.

### Prerequisites

Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/). This project was developed using Python 3.12, but it should work with Python 3.6+.

### Setting Up a Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to your project directory:
cd path/to/your/project
3. Create a virtual environment:
python -m venv env
4. Activate the virtual environment:
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

### Installing Dependencies

Install all necessary libraries using the provided `requirements.txt` file:
```
pip install -r requirements.txt
```
### Configuration

Ensure you have a `looker.ini` file in the same directory as your executable file. This file should contain your Looker user ID and secret:

```ini
[Looker]
# API Endpoint
base_url=https://bigfishgames.gw1.cloud.looker.com

# API 3 client ID
client_id=******

# API 3 client secret
client_secret=*******

# Optional embed secret for user authentication
# embed_secret=YOUR_EMBED_SECRET

# Optional API version. Default is "3.1"
# api_version=3.1
```
### Running the Application
To run the application from the desktop, create a batch file (run_app.bat for Windows) with the following content:
```
@echo off
cd path\to\your\project
call path\to\your\venv\Scripts\activate
python big_fish_main.py
pause
```
Replace path/to/your/project and path\to\your\venv with the actual path to your project and virtual environment.

Double-click run_app.bat to start the application.