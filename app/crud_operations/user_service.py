from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.db.db import get_db_session
from app.models import User
from app.schemas.user_schema import UserCreateSchema
from app.core import hash_password

async def create_user(
        db: AsyncSession, # db session will be passed from router file
        user_data: UserCreateSchema # validate user data from request
    ):

    print("user_data before stmt", user_data)
    print("user_data type before stmt", type(user_data))
    # check for existing user
    statement = select(User).where(User.username == user_data.username)

    result = await db.execute(statement)
    is_exist = result.scalar_one_or_none()
    if(is_exist):
        raise ValueError("User already exist")
    

    # hash password
    hashed_pwd = hash_password(user_data.password)

    # create user (sqlalchemy model/instance creation) 
    new_user = User(
        **user_data.model_dump(exclude={"password"}), # convert the pydantic object to dictionary and unpack it to match the model (keyword parameter unpacking)
        hashed_password=hashed_pwd) 
    

    print("new_user after db model", new_user)
    print("new_user type after db model", type(new_user))

    db.add(new_user) # add the new_user to db(session)
    await db.commit() # commit the changes(adds to database)
    await db.refresh(new_user) # refresh the object(get the new data)
    
    return new_user