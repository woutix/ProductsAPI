# API для создания, получения, удаления списка продуктов.  

## Технологический стек

- FastAPI - фреймворк для создания API  
- PostgreSQL - БД для хранения всех данных
- pydantic - библиотека для формирования схем и валидации данных

## Реализованные методы

- `POST /products/` – добавляет новый товар. В запросе в теле указывается: название, цена, количество, в ответе указывается id, название, цена, количество. Id реализовать в формате GUID'а, не просто циферки.
- `GET /products/` – возвращает список всех товаров. Есть два квери параметра: skip и limit, которые соответственно работают как фильтры: skip сколько пропустить записей, limit — максимальное число. На выходе массив с товарами.
- `GET /products/{product_id}` – возвращает информацию о товаре по id.
- `DELETE /products/{product_id}` - удаляет товар по id.
- `PUT /products/{product_id}` - обновляет товар по id.

## Виртуальное окружение и зависимости

Перед запуском проекта необходимо поднять БД.

### Запуск виртуального окружения

Для запуска виртуального окружения необходимо выполнить команду:
```bash
tryinvenv\Scripts\activate
```

### Установка зависимостей

Для установки необходимых зависимостей необходимо выполнить команду:
```bash
pip install -r requirements.txt
```

### Деактивация виртуального окружения

Для выохда из виртуального окружения необходимо выполнить команду:
```bash
deactivate
```

## Запуск приложения

Для того, чтобы запустить сервер в dev-режиме, необходимо выполнить команду: 
```bash
uvicorn main:app
```
