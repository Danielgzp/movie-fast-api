from fastapi import FastAPI, HTTPException, Body, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email:str
    password:str
#Este vendria siendo el Schema
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=3, max_length=15)
    '''
    gt: greater than
    ge: greater than or equal
    lt: less than
    le: less than or equal

    '''

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 0,
                "category" : "Nombre de la categoria"
            }
        }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post("/login", tags=["auth"])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == "123456"):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})

@app.get('/movies', tags=['movies'], dependencies=[Depends(JWTBearer())])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail="Movie not found")
#   return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    # List Comprenhension
    data = [movie for movie in movies if movie['category'] == category]
    return data

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    # movie.dict()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado correctamente la película"})
# otra forma de hacer el post
    # async def create_movie(request: Request):
    # movie = await request.json()

    # movies.append(movie)

    # return movie

@app.delete('/movies', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int = Path(ge=1, le=2000)) -> dict:
    for item in movies:
        if(item['id'] == id):
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado correctamente la película"})
             
            
#response_model=dict con esto estamos diciendo de que nos devuelva un diccionario
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
#-> dict | con esto estamos diciendo de que nos devuelva un diccionario
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
	    if item["id"] == id:
                item['title'] = movie.title
                item['overview'] = movie.overview
                item['year'] = movie.year
                item['rating'] = movie.rating
                item['category'] = movie.category
                return JSONResponse(status_code=200, content={"message": "Se actualizo correctamente la película"})
                    
                    
		    

    

