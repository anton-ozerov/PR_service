import base64

from fastapi import Request, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config.config import DOCS_USERNAME, DOCS_PASSWORD


class DocsAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware для защиты:
    Swagger UI (/docs) и ReDoc (/redoc) с помощью HTTP Basic Auth
    """

    def __init__(self, app):
        super().__init__(app)
        self.protected_paths = ["/docs", "/redoc", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        """Проверка авторизации для защищенных путей"""

        if any(request.url.path.startswith(path)
               for path in self.protected_paths):
            authorization = request.headers.get("Authorization")

            if not authorization:
                return self._get_unauthorized_response()

            if not authorization.startswith("Basic "):
                return self._get_unauthorized_response()

            try:
                encoded_credentials = authorization.split(" ")[1]
                decoded_credentials = base64.b64decode(
                    encoded_credentials
                ).decode("utf-8")
                username, password = decoded_credentials.split(":", 1)

                if username == DOCS_USERNAME and password == DOCS_PASSWORD:
                    return await call_next(request)
                else:
                    return self._get_unauthorized_response()

            except (ValueError, IndexError, UnicodeDecodeError):
                return self._get_unauthorized_response()

        return await call_next(request)

    def _get_unauthorized_response(self) -> Response:
        """Возвращает ответ 401 с заголовком WWW-Authenticate для Basic Auth"""
        return Response(
            content="Unauthorized",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic realm=\"Swagger UI\""}
        )
