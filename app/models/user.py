from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db import Base
from app.models.mixins import TimestampMixin
from pydantic import EmailStr


class User(Base, TimestampMixin):
    username: Mapped[str] = mapped_column(String(255), unique=True)  
    email: Mapped[EmailStr] = mapped_column(String(60))  
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # repr_cols_num = 5
    # repr_cols = tuple()
