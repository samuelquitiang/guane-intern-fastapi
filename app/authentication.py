from fastapi import APIRouter, status, HTTPException, Depends
import schemas, token_
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

# Method to hash the password
myctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = 'contraseña'
# For all the admin users the password must be hashed
hashed_password = myctx.hash(password)

# Creation of an admin who can enter the dogs data
admin_users = []  # List of the admins
admin1 = schemas.Admin_Login(username='first_admin', password=hashed_password)
admin_users.append(admin1.dict())


@router.get('/api/admins')
def admis():
    return ' The registered admin_users are: ', admin_users


@router.post('/api/login/{username}')
def add_admin(username: str, password: str,
              get_current_user:
              schemas.Admin_Login = Depends(token_.get_current_user)):
    hashed_password = myctx.hash(password)          
    new_admin_user = schemas.Admin_Login(username=username, 
                                   password=hashed_password)
    admin_users.append(new_admin_user.dict())        
    return 'Successfully added'                   


@router.delete('/api/login/{username}')
def destroy_dog(username: str, get_current_user:
                schemas.Admin_Login = Depends(token_.get_current_user)):
    # Gets the index of the dog with the given name and delete it from the data
    user = list(filter(lambda us: us['username'] == username, admin_users))
    to_del = admin_users.index(user[0])
    admin_users.pop(to_del)

    return 'Done'


@router.post('/login', include_in_schema=False)
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = list(filter(lambda us: us['username'] == request.username,
                       admin_users))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    if not myctx.verify(request.password, user[0]['password']):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Incorrect Password')
    access_token = token_.create_token(data={'sub': user[0]['username']})
    return {'access_token': access_token, 'token_type': 'bearer'}
