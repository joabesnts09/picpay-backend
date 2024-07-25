from django.core.exceptions import ValidationError
from ninja import Router
from .schemas import TypeUserSchema, TypeUserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from rolepermissions.roles import assign_role


users_router = Router()


@users_router.post('/', response={200: dict, 400: dict, 500: dict})
def create_user(request, type_user_schema: TypeUserSchema):
    user = User(**type_user_schema.user.dict())
    user.password = make_password(type_user_schema.user.password)
    try:
        user.full_clean()
        user.save()
        assign_role(user, type_user_schema.type_user.type)
    except ValidationError as err:
        return 400, {'error': err.message_dict}
    except Exception as err:
        return 500, {'error': 'Internal Server Error, contact an administrator.'}
        
        
    return {'id': user.id, 'username': user.username}