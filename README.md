# IKT222-Assignment-2

This repository contains an example application for demonstrating XSS (Cross-Site Scripting) vulnerabilities.

## Getting Started

Follow the steps below to set up and run this Flask application.

### 1. Clone the Repository

If you haven't already, clone this repository to your local machine:

```bash
git clone https://github.com/SolUrsi/IKT222-Assignment-2.git
cd IKT222-Assignment-2
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a Python virtual environment to manage dependencies.  
On Windows, run:

```bash
python -m venv venv
source venv/Scripts/activate
```

On macOS/Linux, run:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

Set up the application's database by running:

```bash
python -m flask init-db
```

### 5. Run the Application

Start the Flask development server with:

```bash
python -m flask run
```

The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## Notes

- Make sure you have Python 3.7 or higher installed.
- If you encounter issues with Flask commands, ensure that the `FLASK_APP` environment variable is set correctly, e.g.:
  ```bash
  export FLASK_APP=app.py
  ```
  (On Windows: `set FLASK_APP=app.py`)
