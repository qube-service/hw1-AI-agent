# AI Agent s OpenAI Responses API

Profesionální AI agent využívající OpenAI Responses API s automatickým ukládáním historie a function calling.

## Funkce

- **Responses API**: Nové stateful API od OpenAI s automatickým ukládáním historie
- **Function Calling**: AI může využívat nástroje jako weather API a získávání času
- **Pokračování konverzace**: Historie se automaticky ukládá na OpenAI serverech
- **Čistý kód**: Bez zbytečného logování, profesionální implementace

## Dostupné nástroje

- **Weather API**: Reálné informace o počasí pro jakékoliv město
- **Aktuální čas**: Získání data a času

## Instalace

1. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

2. Spusťte aplikaci:
```bash
python ai_agent.py
```

## Konfigurace

1. Zkopírujte vzorový config soubor:
```bash
cp config.example.py config.py
```

2. Upravte `config.py` a vložte svůj OpenAI API klíč

Nebo použijte environment variable:
```bash
export OPENAI_API_KEY="váš-api-klíč"
```

## Použití

Aplikace funguje jako interaktivní chat:

```
=== AI Agent s Weather API ===
Napište dotaz nebo 'quit' pro ukončení

>>> Jaké je počasí v Praze?
Používám 1 nástroj(ů)...
Volám: get_weather
Výsledek: Počasí v Praha: Sunny, teplota 18°C (pocitově 18°C), vlhkost 60%, vítr 9 km/h
Zpracovávám výsledky...

Odpověď: V Praze je momentálně slunečno s teplotou 18°C...
```

## Struktura

- `ai_agent.py` - Hlavní aplikace
- `config.example.py` - Vzorová konfigurace
- `requirements.txt` - Python závislosti

## Jak to funguje

1. **Input**: Uživatel zadá dotaz
2. **AI Analysis**: OpenAI rozhodne, zda použít nástroje
3. **Function Calling**: Spustí potřebné funkce (weather, time)
4. **Result Processing**: AI zpracuje výsledky a formuluje odpověď
5. **Historie**: Celá konverzace se uloží na OpenAI serverech

## Technické detaily

- **API**: OpenAI Responses API (stateful)
- **Model**: gpt-4o-mini
- **Weather**: wttr.in API (zdarma, bez registrace)
- **Historie**: Automaticky na OpenAI serverech (30 dní) # hw1-AI-agent
