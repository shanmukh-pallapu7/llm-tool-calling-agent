import requests
import os
import json


def get_weather(city):
    url_nominatim = "https://nominatim.openstreetmap.org/search"
    params = {"city": city, "country": "india", "format": "jsonv2"}
    headers = {"User-Agent": "windy_app_api"}
    response_nominatim = requests.get(
        url_nominatim, params=params, headers=headers, timeout=10
    )
    data_nm = response_nominatim.json()
    latitude = float(data_nm[0]["lat"])
    longitude = float(data_nm[0]["lon"])

    open_meteo_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast", params=open_meteo_params
    )
    return response.json()


"""def search_flights(source, destination):
    base_url = "FLIGHT_API_URL"
    headers = {"Authorization": "bearer ABC123"}
    params = {"source": source, "destination": destination}
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()"""


def search_flights(source, destination):
    return {
        "source": source,
        "destination": destination,
        "status": "available",
        "message": "Mock flight data",
    }


weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get wether information for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city to get weather for"}
            },
            "required": ["city"],
        },
    },
}

flight_tool = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "search flights infromation from source to destination",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "The source city"},
                "destination": {
                    "type": "string",
                    "description": "The destination city",
                },
            },
            "required": ["source", "destination"],
        },
    },
}

api_key = os.getenv("API_KEY")

messages = [
    {
        "role": "user",
        "content": "What's the weather in Hyderabad and find a flight from Hyderabad to Delhi?",
    }
]


def call_llm(messages):
    data = {
        "model": "inclusionai/ling-3.0-flash-fin:free",
        "messages": messages,
        "tools": [weather_tool, flight_tool],
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=data,
    )
    llm_data = response.json()
    return llm_data


def execute_tool(tool_call):
    tool_call_id = tool_call["id"]
    tool_name = tool_call["function"]["name"]
    arguments = tool_call["function"]["arguments"]
    arguments = json.loads(arguments)
    tool_route = {"get_weather": get_weather, "search_flights": search_flights}
    if tool_name in tool_route:
        try:
            selected_tool = tool_route[tool_name]
            result = selected_tool(**arguments)
        except Exception as e:
            result = f"Tool execution failed {e}"

    else:
        result = f"{tool_name} not exists"
    return tool_call_id, result


def agent(messages):
    while True:
        llm_data = call_llm(messages)
        if llm_data["choices"][0]["finish_reason"] == "tool_calls":
            messages.append(llm_data["choices"][0]["message"])
            tool_calls = llm_data["choices"][0]["message"]["tool_calls"]
            for tool_call in tool_calls:
                tool_call_id, result = execute_tool(tool_call)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result),
                    }
                )

        else:
            final_answer = llm_data["choices"][0]["message"]["content"]
            print(final_answer)
            break


while True:
    data = {
        "model": "inclusionai/ling-3.0-flash-fin:free",
        "messages": messages,
        "tools": [weather_tool, flight_tool],
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=data,
    )
    llm_data = response.json()

    if llm_data["choices"][0]["finish_reason"] == "tool_calls":
        messages.append(llm_data["choices"][0]["message"])
        tool_route = {"get_weather": get_weather, "search_flights": search_flights}
        tool_calls = llm_data["choices"][0]["message"]["tool_calls"]

        for tool_call in tool_calls:
            tool_call_id = tool_call["id"]
            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            arguments = json.loads(arguments)

            if tool_name in tool_route:
                try:
                    selected_tool = tool_route[tool_name]
                    result = selected_tool(**arguments)
                except Exception as e:
                    result = f"Tool execution failed {e}"
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result),
                    }
                )

            else:
                print(f"{tool_name} not exists")

    else:
        final_answer = llm_data["choices"][0]["message"]["content"]
        print(final_answer)
        break
