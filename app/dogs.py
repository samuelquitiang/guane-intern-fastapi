from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
import schemas, authentication, token_  # Code where are the entities
from datetime import datetime
import requests

import sys
sys.path.append(r"c:\\Users\\samue\\Dropbox\\Proyectos\\Guane\\app_dogs\\worker")

from cel_app import celery_app

""" This code makes an api that receives data about dogs and save them,
besides the user can get info about one dog with a name in particular,
delete it or actualize their data. """

router = APIRouter(tags=['Dogs'])
data = []  # Data in memory list


@router.get('/api/dogs')
def dogs():
    return ' The registered dogs are: ', data


@router.get('/api/dogs/is_adopted')
def get_adopted():
    # Iterable lambda function to obtain the adopted dogs
    dogs_adopted = list(filter(lambda dog: dog['is_adopted'], data))

    # Error message with the detailed problem
    if not dogs_adopted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There are no adopted dogs')

    return dogs_adopted


@router.get('/api/dogs/{name}')
def get_dog(name: str):
    # Iterable lambda function to obtain the dogs by their name
    dogs = list(filter(lambda dog: dog['dog_name'] == name, data))

    # Error message with the detailed problem
    if not dogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The dog with name: {name} does not exist')

    return dogs


@router.get('/api/dogs/user/{user_id}')
def get_user_dogs(user_id: str):
    # Iterable lambda function to obtain the dogs by their name
    dogs = list(filter(lambda dog: dog['user_id'] == user_id, data))

    # Error message with the detailed problem
    if not dogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with id: {user_id} has no dogs')

    return dogs


# Optional 1 and 3 include.
@router.post('/api/dogs/{name}')
async def input_dog(id: str, adopted: bool, name: str, user_id: str,
                    get_current_user: schemas.Admin_Login = Depends(token_.get_current_user)):
    # Gets the image from the extern API
    req = requests.get(f'https://dog.ceo/api/breeds/image/random')
    picture = req.json()['message']
    sd = str(datetime.now())  # Gives the current time
    # Definition of the dog with the given parameters and enter it to the database
    dog = schemas.Dog(
        id=id, user_id=user_id, dog_name=name,
        picture=picture, create_date=sd,
        is_adopted=adopted)
    task = celery_app.send_task(
        "worker.celery_worker.test_celery", args=[id])  # Worker (?)
    print(task)
    data.append(dog.dict())
    return data[-1]


@router.put('/api/dogs/{name}')
def update_dog(name: str, user_id: str, adopted: bool):
    try:
        to_update = get_dog(name)[0]
        to_update['is_adopted'] = adopted
        to_update['user_id'] = user_id

    # Error message with detailed problem, if there is an IndexError
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The dog with name: {name} does not exist')

    return to_update


@router.delete('/api/dogs/{name}')
def destroy_dog(name: str):
    # Gets the index of the dog with the given name and delete it from the data
    to_del = data.index(get_dog(name)[0])
    data.pop(to_del)

    return 'Done'
