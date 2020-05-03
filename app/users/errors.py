from werkzeug.exceptions import HTTPException


errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username or email already exists.",
        'status': 409,
    },
    'UserIsAlreadyDeletedError': {
        'message': "A user is already deleted.",
        'status': 404,
    },
    'ArgumentsIsEmptyError': {
        'message': "JSON's arguments is empty",
        'status': 400,
        'extra': "Please, fill all arguments in your JSON before sending request",
    },
    'UserDoesNotExistError': {
        'message': "User doesn't exist",
        'status': 404,
    }
}


class UserAlreadyExistsError(HTTPException):
    code = 409
    description = ("User already exists",)


class UserDoesNotExistError(HTTPException):
    code = 404
    description = ("User doesn't exist",)


class UserIsAlreadyDeletedError(HTTPException):
    code = 404
    description = ('User is already deleted',)


class ArgumentsIsEmptyError(HTTPException):
    code = 400
    description = ("json's arguments is empty",)
