from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarHTTPException


def _problem(code: str, message: str, status: int, rid: str | None):
    body = {"error": {"code": code, "message": message}}
    if rid:
        body["error"]["correlation_id"] = rid
    return JSONResponse(status_code=status, content=body)


async def http_exception_handler(request: Request, exc: StarHTTPException):
    rid = request.headers.get("X-Request-Id")
    msg = "resource not found" if exc.status_code == 404 else "request failed"
    return _problem("http_error", msg, exc.status_code, rid)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    rid = request.headers.get("X-Request-Id")
    return _problem("validation_error", "invalid request", 422, rid)


async def unhandled_exception_handler(request: Request, exc: Exception):
    rid = request.headers.get("X-Request-Id")
    return _problem("internal_error", "unexpected error", 500, rid)
