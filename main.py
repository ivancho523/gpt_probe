from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

app = FastAPI()

# Set up the database connection
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users = db['users']

# Set up the template engine
templates = Jinja2Templates(directory='templates')

# Set up the static files directory
app.mount('/static', StaticFiles(directory='static'), name='static')

# Set up the basic authentication
security = HTTPBasic()

# Define the login route
@app.get('/', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.post('/login')
def login(request: Request, response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    # Get the user's credentials
    username = credentials.username
    password = credentials.password

    # Check if the user exists in the database
    user = users.find_one({'username': username})
    if not user:
        return {'success': False}

    # Check if the password is correct
    if not pbkdf2_sha256.verify(password, user['password']):
        return {'success': False}

    # Redirect the user to the home page
    response = RedirectResponse(url='/home')
    response.set_cookie(key='username', value=username)
    return response

# Define the home route
@app.get('/home', response_class=HTMLResponse)
def home(request: Request, username: str = Cookie(None)):
    # Check if the user is logged in
    if not username:
        return RedirectResponse(url='/')

    # Get the user's data from the database
    user = users.find_one({'username': username})

    # Render the home page template
    return templates.TemplateResponse('home.html', {'request': request, 'user': user})

# Define the logout route
@app.get('/logout')
def logout(response: Response):
    # Redirect the user to the login page
    response = RedirectResponse(url='/')
    response.delete_cookie(key='username')
    return response