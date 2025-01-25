# batch-pdf-flask
## If you're cloning this repo for the first time:
### Check if you have python installed. 
`python --version`

It must be >= 3.9. Mine is 3.13.0

<!-- Create and activate the virtual environment -->
```
py -3 -m venv .venv
.venv\Scripts\activate
```
<!-- Install the requirements (the libraries used on the app) -->
`pip3 install -r requirements.txt`

<!-- Run the application -->
`flask --app main run --debug`

Every change you do, reload the browser.

## If you already have the app in your computer, just run the application
`.venv\Scripts\activate`

`flask --app main run --debug`

## If you added a new library, save on the requirements.txt:
`pip3 freeze > requirements.txt`