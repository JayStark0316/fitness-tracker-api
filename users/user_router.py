from typing import Annotated

import names_generator
from fastapi import APIRouter
from fastapi.params import Depends
from pymongo.synchronous.database import Database

from commons.exceptions.base_api_exception_handler import BadRequestException, ResourceConflictException, \
    InternalServerErrorException
from commons.utils.app_settings import AppSettings, get_settings
from commons.utils.database import get_database
from users.db_user_model import UserDbModel
from users.user_schemas import UserCreateRequest, ResponseUserSchema
from commons.exceptions.error_constants import BAD_REQUEST_ERROR, CONFLICT_ERROR, INTERNAL_SERVER_ERROR
from commons.utils.app_utils import hash_email, encrypt_email, generate_password_hash
from users.user_repository import create_user, get_user_by_hashed_email, get_user_by_id
from commons.utils.logger_config import api_logger

router = APIRouter(prefix="/users",tags=["Users"])

DBSession = Annotated[Database, Depends(get_database)]
AppSettings = Annotated[AppSettings, Depends(get_settings)]


@router.post("/", status_code=201, response_model=ResponseUserSchema,
             summary="Create a new user",
             description="Create a new user with the given email and password")
async def create_new_user(db: DBSession,
                          request: UserCreateRequest,
                          app_settings: AppSettings):
    #  Strip off whitespaces from the request attributes
    api_logger.info(f"Creating a new user with email: {request.email}")

    request.email = request.email.strip()
    request.password = request.password.strip()

    # If the email or password is not present in the request, raise an error.
    if not request.email or not request.password:
        api_logger.error("Email or password is missing in the request")
        raise BadRequestException(BAD_REQUEST_ERROR)

    # Check if the display name is not then generate one using the library.
    if request.display_name:
        request.display_name = request.display_name.strip()
    else:
        request.display_name = names_generator.generate_name()

    hashed_email = hash_email(request.email)

    # Check if the user already exists in the database
    api_logger.info(f"Checking if user with email {request.email} already exists")
    if get_user_by_hashed_email(hashed_email, db):
        api_logger.error(f"User with email {request.email} already exists")
        raise ResourceConflictException(CONFLICT_ERROR)

    encrypted_email = encrypt_email(request.email, app_settings.aes_key)

    hashed_password = generate_password_hash(request.password)

    # Create a user db model
    __user = UserDbModel(
        email=encrypted_email,
        display_name=request.display_name,
        password=hashed_password,
        hashed_email=hashed_email
    )

    # Create a new user in the database
    __user_id = None
    try:
        api_logger.info("Creating a new user in the database")
        __user_id = create_user(__user, db)
    except Exception as e:
        api_logger.error(f"Error while creating a new user: {e}")
        raise InternalServerErrorException(INTERNAL_SERVER_ERROR)

    api_logger.info(f"User created successfully with id: {__user_id}")
    saved_user = get_user_by_id(__user_id, db)

    if saved_user:
        api_logger.info(f"User created successfully with id: {saved_user.id}")
        return ResponseUserSchema(**saved_user.__dict__)
    else:
        api_logger.error("Error while saving the user in the database")
        raise InternalServerErrorException(INTERNAL_SERVER_ERROR)
