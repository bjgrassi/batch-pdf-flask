# batch-pdf-flask
## If you're cloning this repo for the first time:
### Check if you have python installed. 
`python --version`

It must be >= 3.9. Mine is 3.13.0

Create and activate the virtual environment

```
py -3 -m venv .venv
.venv\Scripts\activate
```
Install the requirements (the libraries used on the app)

`pip3 install -r requirements.txt`

Run the application
`flask --app main run --debug`

Will show messages on the terminal. Look for the "Running on http://127.0.0.1:5000" to open the app.
Every change you do in the code, reload the browser.

## If you already have the app in your computer, just run the application
`.venv\Scripts\activate`

`flask --app main run --debug`

## If you added a new library, save on the requirements.txt:
`pip3 freeze > requirements.txt`

# New
On Windows (Command Prompt):
```
(.venv) PS C:\Projetos\batch-pdf-flask> set FLASK_APP=app:create_app
(.venv) PS C:\Projetos\batch-pdf-flask> flask run --debug
```

On Windows (PowerShell):
```
$env:FLASK_APP = "app:create_app"
flask run --debug
```