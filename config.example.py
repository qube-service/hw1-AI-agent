"""
Konfigurace AI agenta - Vzor
Zkopírujte tento soubor jako config.py a vložte svůj API klíč
"""

import os

# OpenAI API klíč - VLOŽTE SVŮJ KLÍČ
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'VÁŠE_OPENAI_API_KLÍČ')

# Nastavení modelu
MODEL = "gpt-4.1"

# Timeout pro HTTP requesty
HTTP_TIMEOUT = 10 