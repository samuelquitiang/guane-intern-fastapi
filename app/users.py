from fastapi import APIRouter, HTTPException, status, Depends
import schemas, authentication, token_, dogs  # Code where are the entities
from datetime import datetime
import requests


""" This code is the Optional 3. makes an entity called user, this one receives
data about users and save them, besides access to the info with
the user_id, delete it or actualize it. """

router = APIRouter(tags=['Users'])
user_data = []  # user_Data in memory list


@router.get('/api/users')
def lista_users():
    return ' The registered users are: ', user_data


@router.get('/api/users/{user_id}')
def get_users(user_id: str):
    # Iterable lambda function to obtain the users by their user_id
    users = list(filter(lambda user: user['user_id'] == user_id, user_data))

    # Error message with the detailed problem
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with user_id: {user_id} does not exist')

    return users


# Optional 1 include.
@router.post('/api/users/')
def input_user(user_id: str, user_name: str, last_name: str, email: str,
               get_current_user: schemas.Admin_Login
               = Depends(token_.get_current_user)):

    # Definition of the user with the given parameters and enter it to the database
    user = schemas.User(
        user_id=user_id, user_name=user_name,
        last_name=last_name, email=email)
    user_data.append(user.dict())
    return user_data[-1]


@router.put('/api/users/{user_id}')
def update_user(user_id: str, user_name: str, last_name: str, email: str):

    # This will actualize the information of the user with the corresponding id
    try:
        to_update = get_users(user_id)[0]
        to_update['user_name'] = user_name
        to_update['last_name'] = last_name
        to_update['email'] = email

    # Error message with detailed problem, if there is an IndexError
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The user with user_id: {user_id} does not exist')

    return to_update


@router.delete('/api/users/{user_id}')
def destroy_user(user_id: str):
    # Gets the index of the user with the given user_id and delete it from the user_data
    to_del = user_data.index(get_users(user_id)[0])
    dog_todel = dogs.data.index(dogs.get_user_dogs(user_id)[0])
    user_data.pop(to_del)
    dogs.data.pop(dog_todel)

    return 'Done'
    