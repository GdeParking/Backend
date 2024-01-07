from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.auth.auth import authenticate_user, create_token, get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await authenticate_user(email, password)
        if user:
            token = create_token({"sub": str(user.id)})
            request.session.update({"camera_manager_token": token})
        return True
      
    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("camera_manager_token")
        if not token:
            return False
        user = await get_current_user(token)
        if not user:
            #return RedirectResponse(request.url_for("admin:index")) ---- also works
            return False
        return True


authentication_backend = AdminAuth(secret_key="315")