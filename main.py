from fastapi import FastAPI

app = FastAPI()
@app.get('/')

def index():
    return {'data': {'first_name': 'Anish', 'last_name': 'Dahal'}}

@app.get('/about')

def about():
    return {'data': {'context': 'about page'}}
    
   