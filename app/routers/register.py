from fastapi import Depends, APIRouter, HTTPException, status
from ..import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..databases import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['register']
)

###Registerating users

@router.post("/userss",response_model=schemas.ShowUser)
def post(usr:schemas.CreateUser,db:Session=Depends(get_db)):
    hashed_password = utils.hash(usr.password)
    usr.password=hashed_password
    new_user=models.Users(**usr.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/userss/{id}",response_model=schemas.ShowUser)
def get(id:int,db:Session=Depends(get_db),current_user:str = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        return {"msg":" user not found"}
    return user

#validating the user LOGIN

@router.post("/userss/login",response_model=schemas.Token)
def login(users_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user_data=db.query(models.Users).filter(models.Users.email == users_credentials.username).first()
    if user_data == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    print(users_credentials.password,user_data.password)
    if not utils.verify(users_credentials.password,user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    acess_token=oauth2.create_acess_token(data={"user_email":user_data.email})
    return {"acess_token":acess_token,"token_type":"Bearer"}




