from fastapi import  Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

#Ruta protegida por un token de inicio de seison de usuario
@movie_router.get('/movies', tags=['movies'], dependencies=[Depends(JWTBearer())])
def get_movies():
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
#   return JSONResponse(status_code=404, content=[])

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Categoria no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado correctamente la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    result = MovieService(db).delete_movie(id)
    return result

#response_model=dict con esto estamos diciendo de que nos devuelva un diccionario
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
#-> dict | con esto estamos diciendo de que nos devuelva un diccionario
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    else: 
        MovieService(db).update_movie(id, movie)
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})
                    