"""
Konfigurace AI agenta
"""

import os

# OpenAI API klíč - nastavte svojí hodnotu
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

# Nastavení modelu
MODEL = "gpt-4.1"

# Timeout pro HTTP requesty
HTTP_TIMEOUT = 10 