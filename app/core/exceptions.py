from fastapi import HTTPException, status


class BookingException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception
    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class WrongJWTTokenException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=401
    detail="Левый токен"


class EmailAlreadyExistsException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь с таким адресом почты уже существует"


class UsernameAlreadyExistsException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь с таким именем уже существует"


class NoSuchUserException(BookingException):  # <-- обязательно наследуемся от нашего класса
    status_code=status.HTTP_409_CONFLICT
    detail="Такого пользователя не существует"