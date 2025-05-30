from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class NotFoundMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "detail": "Ruta no encontrada 404 😅",
                    "path": request.url.path,
                    "method": request.method, 
                    "ms": 404
                },
            )
        return response

