"""
Localization manager for multi-language support
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

from bot.config import settings


class LocalizationManager:
    """Manage translations for multiple languages"""
    
    def __init__(self):
        self.translations: Dict[str, Dict] = {}
        self.locales_dir = Path(__file__).parent
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files"""
        for lang_code in settings.available_languages:
            lang_dir = self.locales_dir / lang_code
            messages_file = lang_dir / 'messages.json'
            
            if messages_file.exists():
                with open(messages_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
    
    def get(self, key: str, language: str = None, **kwargs) -> str:
        """
        Get translated message
        
        Args:
            key: Translation key (e.g., 'commands.start.message')
            language: Language code (default: from settings)
            **kwargs: Format parameters
            
        Returns:
            Translated message
        """
        if language is None:
            language = settings.default_language
        
        # Get translation for language
        translations = self.translations.get(language, {})
        
        # Navigate through nested keys
        keys = key.split('.')
        value = translations
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                break
        
        # If not found, try default language
        if value is None and language != settings.default_language:
            return self.get(key, settings.default_language, **kwargs)
        
        # If still not found, return key
        if value is None:
            return key
        
        # Format with parameters
        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        
        return value
    
    def get_button(self, button_name: str, language: str = None) -> str:
        """Get button text"""
        return self.get(f'buttons.{button_name}', language)
    
    def get_menu(self, menu_name: str, language: str = None) -> str:
        """Get menu text"""
        return self.get(f'menu.{menu_name}', language)
    
    def get_error(self, error_name: str, language: str = None) -> str:
        """Get error message"""
        return self.get(f'errors.{error_name}', language)
    
    def get_success(self, success_name: str, language: str = None) -> str:
        """Get success message"""
        return self.get(f'success.{success_name}', language)
    
    def get_language_name(self, language_code: str) -> str:
        """Get language name"""
        translations = self.translations.get(language_code, {})
        return translations.get('language_name', language_code)
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get all available languages with names"""
        return {
            code: self.get_language_name(code)
            for code in settings.available_languages
        }


# Global localization manager instance
i18n = LocalizationManager()


def _(key: str, language: str = None, **kwargs) -> str:
    """
    Shortcut for getting translations
    
    Usage:
        _('commands.start.message', name='John')
        _('errors.generic', language='ru')
    """
    return i18n.get(key, language, **kwargs)
