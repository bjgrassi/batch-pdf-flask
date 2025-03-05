# batch-pdf-flask
## 1. If you're cloning this repo for the first time
### 1.1. Check if you have python installed. 
`python --version`

It must be >= 3.9. Mine is 3.13.0

### 1.2. Create and activate the virtual environment

```
py -3 -m venv .venv
.venv\Scripts\activate
```

### 1.3. Install the requirements (the libraries used on the app)
```
pip3 install -r requirements.txt
```

### 1.4. Add FLASK_APP variable (.venv must be activated)

On Windows (Command Prompt):
```
set FLASK_APP=app:create_app
```

On Windows (PowerShell):
```
$env:FLASK_APP = "app:create_app"
```

### 1.5 Run the application
```
flask run --debug
```

Will show messages on the terminal. Look for the "Running on http://127.0.0.1:5000" to open the app.
Every change you do in the code, reload the browser.

## 2. If you already have the app in your computer, just run the application
```
.venv\Scripts\activate
flask run --debug
```

## If you added a new library, save on the requirements.txt
`pip3 freeze > requirements.txt`