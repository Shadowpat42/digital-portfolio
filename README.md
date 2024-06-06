# Вас приветствует команда ИП Шадрин <img src="https://media.tenor.com/dMwtTTN4XusAAAAj/yeah-cute.gif" width="100" height="100" />

### Состав команды:

| Участник                                   | Роль                    | 
| ------------------------------------------ | ----------------------- | 
| Шадрин Андрей Алексеевич                   | Тимлид                  | 
| Савина Анастасия Олеговна                  | Аналитик                |
| Зубова Екатерина Александровна             | Дизайнер                |
| Джобиров Владимир Джамшедович              | Backend-разработчик     |
| Ворожцов Антон Александрович               | Frontend-разработчик    |
| Лукин Станислав Сергеевич                  | Frontend-разработчик    |

## Структура репозитория:

```text
.
├── main                   # Головное приложение
│   ├── migrations         # Миграции базы данных
│   ├── templates          # HTML шаблоны
│   ├── templatetags       # Пользовательские теги для шаблонов
│   ├── __init__.py        # Инициализация пакета
│   ├── admin.py           # Конфигурация административной части
│   ├── apps.py            # Конфигурация приложения
│   ├── forms.py           # Веб-формы
│   ├── models.py          # Модели базы данных
│   ├── signals.py         # Сигналы Django
│   ├── tests.py           # Тесты приложения
│   ├── urls.py            # URL маршруты
│   └── views.py           # Виды приложения
├── media                  # Медиа файлы
│   ├── images             # Изображения
|       └── ... 
│   └── methodological_files # Методические файлы
|       └── ... 
├── portfolio              # Портфолио проекта
│   ├── __init__.py        # Инициализация пакета
│   ├── asgi.py            # Конфигурация ASGI
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # URL маршруты
│   └── wsgi.py            # Конфигурация WSGI
├── static                 # Статические файлы проекта
├── .gitignore             # Исключения для Git
├── README.md              # Описание проекта
├── manage.py              # Управление проектом Django
└── requirements.txt       # Список зависимостей проекта
