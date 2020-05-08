from werkzeug.exceptions import HTTPException


errors = {
    'LinkNotFoundError': {
        'message': "Link not found",
        'status': 404,
    },
    'NoUpdatedDataLinksError': {
        'message': "No data for update the url",
        'status': 400
    },
    'SpecialShortUrlAlreadyExistsError': {
        'message': "This named url already exists",
        'status': 400
    },
}


class LinkNotFoundError(HTTPException):
    code = 404
    description = ("Link not found",)


class NoUpdatedDataLinksError(HTTPException):
    code = 400
    description = ("No data for update the url",)


class SpecialShortUrlAlreadyExistsError(HTTPException):
    code = 400
    description = ("This named url already exists",)
