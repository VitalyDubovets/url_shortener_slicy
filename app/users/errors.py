from werkzeug.exceptions import HTTPException


errors = {
    'BadUsernameOrPasswordError': {
        'message': "Bad username or password",
        'status': 400,
        'extra': 'Make sure that you entered your username or password correctly'
    },
    'UserAlreadyExistsError': {
        'message': "A user with that username or email already exists",
        'status': 409,
    },
    'ArgumentsIsEmptyError': {
        'message': "JSON's arguments is empty",
        'status': 400,
        'extra': "Please, fill all arguments in your JSON before sending request",
    },
    'UserNotFoundError': {
        'message': "User not found",
        'status': 404,
    }
}


class BadUsernameOrPasswordError(HTTPException):
    code = 400
    description = ('Bad username or password',)


class UserAlreadyExistsError(HTTPException):
    code = 409
    description = ("User already exists",)


class UserNotFoundError(HTTPException):
    code = 404
    description = ("User not found",)


class UserIsAlreadyDeletedError(HTTPException):
    code = 404
    description = ('User is already deleted',)


class ArgumentsIsEmptyError(HTTPException):
    code = 400
    description = ("json's arguments is empty",)
