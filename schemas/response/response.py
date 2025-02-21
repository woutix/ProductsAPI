from pydantic import BaseModel


# Создаем класс для передачи ответа
class ResponseMessage(BaseModel):
        message: str
