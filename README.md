# 🤖 Professional Telegram Bot Template

**Production-ready Telegram bot template with multi-language support, built with best practices.**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- ✅ **Multi-language Support** (Uzbek, Russian, English)
- ✅ **SQLAlchemy ORM** with migrations
- ✅ **Pydantic Settings** for configuration
- ✅ **Custom Filters & Decorators**
- ✅ **Admin Panel**
- ✅ **User Management**
- ✅ **Statistics Tracking**
- ✅ **Structured Logging** (JSON + Console)
- ✅ **Error Handling**
- ✅ **Database Migrations** (Alembic ready)
- ✅ **Type Hints** throughout
- ✅ **Production Ready**

## 📁 Project Structure

```
telegram_bot_template/
├── bot/
│   ├── config/              # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py     # Pydantic settings
│   │   └── constants.py    # Application constants
│   ├── database/           # Database layer
│   │   ├── __init__.py
│   │   ├── models.py       # SQLAlchemy models
│   │   └── manager.py      # Database operations
│   ├── filters/            # Custom filters
│   │   ├── __init__.py
│   │   └── permissions.py  # Permission filters
│   ├── handlers/           # Request handlers
│   │   ├── __init__.py
│   │   └── basic.py        # Basic commands
│   ├── keyboards/          # Telegram keyboards
│   │   ├── __init__.py
│   │   ├── inline.py       # Inline keyboards
│   │   └── reply.py        # Reply keyboards
│   ├── locales/            # Translations
│   │   ├── __init__.py     # i18n manager
│   │   ├── uz/
│   │   │   └── messages.json
│   │   ├── ru/
│   │   │   └── messages.json
│   │   └── en/
│   │       └── messages.json
│   ├── middlewares/        # Middlewares (optional)
│   ├── services/           # Business logic (optional)
│   ├── utils/              # Utilities
│   │   ├── __init__.py
│   │   ├── decorators.py   # Handler decorators
│   │   ├── helpers.py      # Helper functions
│   │   └── logging_config.py # Logging setup
│   ├── __init__.py
│   └── main.py             # Application entry point
├── data/                   # Data directory
│   └── backups/           # Database backups
├── logs/                   # Log files
├── tests/                  # Tests
│   ├── unit/
│   └── integration/
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── .env.example           # Environment template
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── run.py                 # Run script
└── README.md
```

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <repository-url>
cd telegram_bot_template

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your values
```

Required configuration:
```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789,987654321
SUPER_ADMIN_ID=123456789
```

### 3. Run the Bot

```bash
python run.py
# or
python -m bot.main
```

## 📚 Documentation

### Configuration

All configuration is done via `.env` file using Pydantic Settings:

```python
from bot.config import settings

# Access settings
settings.bot_token
settings.admin_ids
settings.default_language
```

### Multi-language Support

```python
from bot.locales import i18n, _

# Get translation
message = i18n.get('commands.start.message', language='uz', name='John')

# Or use shortcut
message = _('commands.start.message', language='uz', name='John')

# Get button text
button_text = i18n.get_button('back', language='ru')

# Get error message
error_msg = i18n.get_error('permission_denied', language='en')
```

### Database Operations

```python
from bot.database import db

# Get or create user
user = db.get_or_create_user(
    user_id=123456789,
    username='johndoe',
    first_name='John',
    language='uz'
)

# Update user
db.update_user(user_id=123456789, is_premium=True)

# Get statistics
stats = db.get_statistics()
```

### Custom Filters

```python
from bot.filters import admin_filter, premium_filter
from telegram.ext import CommandHandler

# Use filters in handlers
dp.add_handler(CommandHandler(
    'admin',
    admin_handler,
    filters=admin_filter & private_filter
))
```

### Decorators

```python
from bot.utils import protected_handler, admin_only, premium_only

# Protected handler (track + check_blocked + log + error handling)
@protected_handler
def my_handler(update, context):
    pass

# Admin only
@admin_only
def admin_handler(update, context):
    pass

# Premium only
@premium_only
def premium_feature(update, context):
    pass

# Combine decorators
@admin_only
@log_command
def special_handler(update, context):
    pass
```

### Keyboards

```python
from bot.keyboards import (
    main_menu_keyboard,
    settings_keyboard,
    language_keyboard
)

# Inline keyboard with language support
update.message.reply_text(
    "Choose option:",
    reply_markup=main_menu_keyboard(language='uz')
)
```

## 🔧 Development

### Adding New Language

1. Create directory: `bot/locales/fr/`
2. Add `messages.json` with translations
3. Update `.env`: `AVAILABLE_LANGUAGES=uz,ru,en,fr`

### Adding New Handler

```python
# bot/handlers/my_feature.py
from bot.utils import protected_handler

@protected_handler
def my_command(update, context):
    # Your logic
    pass

# bot/main.py
from bot.handlers.my_feature import my_command

dp.add_handler(CommandHandler('mycommand', my_command))
```

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/
pytest --cov=bot tests/
```

## 📊 Database Migrations

```bash
# Initialize Alembic (first time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚀 Deployment

### Using Systemd (Linux)

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/telegram_bot_template
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

```bash
docker build -t telegram-bot .
docker run -d --name my-bot --env-file .env telegram-bot
```

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram bot token | Yes | - |
| `ADMIN_IDS` | Comma-separated admin IDs | Yes | - |
| `SUPER_ADMIN_ID` | Super admin ID | Yes | - |
| `DATABASE_URL` | Database connection URL | No | `sqlite:///data/bot.db` |
| `DEFAULT_LANGUAGE` | Default language | No | `uz` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `DEBUG` | Debug mode | No | `false` |

See `.env.example` for all variables.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👨‍💻 Author

Your Name - [@yourusername](https://t.me/yourusername)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

---

**⭐ Star this repo if you find it useful!**
