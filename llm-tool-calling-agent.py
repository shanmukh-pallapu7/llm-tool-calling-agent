import json
import os

import requests

# --------------------------------------------------
# Tools
# --------------------------------------------------


def get_weather(city):
    """Get current weather information for a city."""

    url_nominatim = "https://nominatim.openstreetmap.org/search"

    params = {
        "city": city,
        "country": "India",
        "format": "jsonv2",
    }

    headers = {"User-Agent": "ai-agent-weather-tool"}

    response = requests.get(
        url_nominatim,
        params=params,
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    data_nm = response.json()

    if not data_nm:
        raise ValueError(f"Could not find location: {city}")

    latitude = float(data_nm[0]["lat"])
    longitude = float(data_nm[0]["lon"])

    open_meteo_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=open_meteo_params,
        timeout=10,
    )
    response.raise_for_status()

    return response.json()


def search_flights(source, destination):
    """Mock flight search tool."""

    return {
        "source": source,
        "destination": destination,
        "status": "available",
        "message": "Mock flight data",
    }


# --------------------------------------------------
# Tool schemas
# --------------------------------------------------

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather information for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for.",
                }
            },
            "required": ["city"],
        },
    },
}


flight_tool = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search flight information from a source city to a destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "The source city.",
                },
                "destination": {
                    "type": "string",
                    "description": "The destination city.",
                },
            },
            "required": ["source", "destination"],
        },
    },
}


# --------------------------------------------------
# Configuration
# --------------------------------------------------

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY environment variable is not set.")


# --------------------------------------------------
# LLM
# --------------------------------------------------


def call_llm(messages):
    """Send the conversation to the LLM and return its response."""

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
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# Tool execution
# --------------------------------------------------


def execute_tool(tool_call):
    """Execute one tool call and return its ID and result."""

    tool_call_id = tool_call["id"]

    tool_name = tool_call["function"]["name"]

    arguments = json.loads(tool_call["function"]["arguments"])

    tool_route = {
        "get_weather": get_weather,
        "search_flights": search_flights,
    }

    if tool_name not in tool_route:
        return tool_call_id, f"{tool_name} does not exist."

    try:
        selected_tool = tool_route[tool_name]

        result = selected_tool(**arguments)

    except Exception as e:
        result = f"Tool execution failed: {e}"

    return tool_call_id, result


# --------------------------------------------------
# Agent
# --------------------------------------------------


def agent(messages):
    """Run the agent until the LLM produces a final answer."""

    while True:

        # 1. Ask the LLM what to do
        llm_data = call_llm(messages)

        choice = llm_data["choices"][0]

        # 2. Check whether the LLM wants to use tools
        if choice["finish_reason"] == "tool_calls":

            assistant_message = choice["message"]

            # Add the assistant's tool-call message
            messages.append(assistant_message)

            tool_calls = assistant_message["tool_calls"]

            # 3. Execute every requested tool
            for tool_call in tool_calls:

                tool_call_id, result = execute_tool(tool_call)

                # 4. Add each tool result to conversation
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps(result),
                    }
                )

        # 5. LLM has finished
        else:

            final_answer = choice["message"]["content"]

            return final_answer


# --------------------------------------------------
# Run agent
# --------------------------------------------------

messages = [
    {
        "role": "user",
        "content": (
            "What's the weather in Hyderabad and "
            "find a flight from Hyderabad to Delhi?"
        ),
    }
]

answer = agent(messages)

print(answer)
