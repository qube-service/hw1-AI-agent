#!/usr/bin/env python3
"""
AI Agent s OpenAI Responses API a Weather funkcionalitou
"""

import json
import requests
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, HTTP_TIMEOUT

# Inicializace OpenAI klienta
client = OpenAI(api_key=OPENAI_API_KEY)

def get_weather(city: str) -> str:
    """Získá informace o počasí pro zadané město"""
    try:
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=HTTP_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        current = data['current_condition'][0]
        
        temp = current['temp_C']
        feels_like = current['FeelsLikeC'] 
        humidity = current['humidity']
        description = current['weatherDesc'][0]['value']
        wind_speed = current['windspeedKmph']
        
        return f"Počasí v {city}: {description}, teplota {temp}°C (pocitově {feels_like}°C), vlhkost {humidity}%, vítr {wind_speed} km/h"
        
    except Exception as e:
        return f"Nepodařilo se získat počasí pro {city}: {str(e)}"

def get_current_time() -> str:
    """Získá aktuální datum a čas"""
    return f"Aktuální čas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Mapování funkcí
function_map = {
    "get_weather": get_weather,
    "get_current_time": get_current_time
}

# Definice nástrojů pro OpenAI
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Získá aktuální informace o počasí pro zadané město",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Název města"
                }
            },
            "required": ["city"]
        }
    },
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Získá aktuální datum a čas",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

class AIAgent:
    """AI Agent využívající OpenAI Responses API"""
    
    def __init__(self):
        self.client = client
        self.current_response_id = None
        
    def send_message(self, message: str) -> str:
        """Pošle zprávu a zpracuje odpověď včetně function calls"""
        try:
            request_params = {
                "model": MODEL,
                "input": message,
                "tools": tools,
                "tool_choice": "auto"
            }
            
            if self.current_response_id:
                request_params["previous_response_id"] = self.current_response_id
            
            response = self.client.responses.create(**request_params)
            self.current_response_id = response.id
            
            return self._process_response(response)
            
        except Exception as e:
            return f"Chyba při komunikaci s AI: {str(e)}"
    
    def _process_response(self, response) -> str:
        """Zpracuje odpověď a vykoná případné function calls"""
        function_calls = [output for output in response.output if output.type == "function_call"]
        
        if function_calls:
            print(f"Používám {len(function_calls)} nástroj(ů)...")
            
            function_outputs = []
            
            for func_call in function_calls:
                function_name = func_call.name
                function_args = func_call.arguments if hasattr(func_call, 'arguments') else {}
                
                if isinstance(function_args, str):
                    try:
                        function_args = json.loads(function_args)
                    except:
                        function_args = {}
                
                print(f"Volám: {function_name}")
                
                if function_name in function_map:
                    try:
                        func = function_map[function_name]
                        result = func(**function_args) if function_args else func()
                        print(f"Výsledek: {result}")
                        
                    except Exception as e:
                        result = f"Chyba při volání funkce: {e}"
                        print(result)
                else:
                    result = f"Neznámá funkce: {function_name}"
                    print(result)
                
                function_outputs.append({
                    "type": "function_call_output",
                    "call_id": func_call.call_id,
                    "output": result
                })
            
            print("Zpracovávám výsledky...")
            
            follow_up_response = self.client.responses.create(
                model=MODEL,
                previous_response_id=response.id,
                input=function_outputs
            )
            
            self.current_response_id = follow_up_response.id
            return follow_up_response.output_text
        
        return response.output_text

def main():
    """Hlavní program"""
    agent = AIAgent()
    
    print("=== AI Agent s Weather API ===")
    print("Napište dotaz nebo 'quit' pro ukončení")
    print()
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Ukončuji...")
                break
                
            if not user_input:
                print("Zadejte dotaz")
                continue
            
            print()
            response = agent.send_message(user_input)
            print(f"\nOdpověď: {response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nUkončeno uživatelem")
            break
        except Exception as e:
            print(f"Chyba: {e}")

if __name__ == "__main__":
    main() 