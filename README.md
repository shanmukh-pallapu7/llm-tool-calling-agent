# LLM Tool Calling Agent

A Python-based LLM agent that dynamically selects and executes tools using function calling.

## 🚀 Project Overview

This project demonstrates how an LLM can interact with external tools instead of generating responses using only its internal knowledge.

The agent can:

* Understand a user's request
* Decide which tool is required
* Generate structured tool calls
* Execute the selected tool
* Return tool results to the LLM
* Generate a final response based on the tool results
* Execute multiple tools for a single request

## 🧠 Architecture

```text
User
  ↓
LLM
  ↓
Tool Selection
  ↓
┌──────────────────────┐
│      Tool Router     │
└──────────────────────┘
       ↓          ↓
   Weather      Flights
     Tool         Tool
       ↓          ↓
   API Data     Flight Data
       └──────┬───┘
              ↓
             LLM
              ↓
        Final Response
```

## 🛠️ Technologies

* Python
* LLM APIs
* OpenRouter
* Function Calling / Tool Calling
* REST APIs
* JSON
* `requests`
* Environment Variables
* Git & GitHub

## 🔧 Tools

### Weather Tool

The agent can use a weather tool to retrieve weather information for a requested location.

The weather workflow uses:

* Nominatim for geocoding
* Open-Meteo for weather data

### Flight Search Tool

A flight-search tool is included to demonstrate how an agent can route requests to different tools.

> Note: The current flight tool uses mock data for learning and agent orchestration purposes.

## 🔄 Agent Loop

The core agent follows this process:

```text
1. User sends a request
        ↓
2. LLM analyzes the request
        ↓
3. LLM decides whether a tool is required
        ↓
4. LLM generates tool call(s)
        ↓
5. Agent executes the tool(s)
        ↓
6. Tool results are returned to the LLM
        ↓
7. LLM generates the final answer
```

The agent supports multiple tool calls in the same request.

## 📌 Example

A user could ask:

```text
What's the weather in Hyderabad and find me a flight to Delhi?
```

The LLM can determine that two tools are required:

```text
Weather Tool → Hyderabad weather
Flight Tool  → Flight search
```

The agent executes both tools and sends their results back to the LLM before producing the final response.

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/shanmukh786/llm-tool-calling-agent.git
cd llm-tool-calling-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file or configure the required environment variable:

```bash
export API_KEY="your_api_key"
```

Do not commit API keys or other secrets to GitHub.

### 5. Run the agent

```bash
python3 llm-tool-calling-agent.py
```

## 🎯 What I Learned

This project helped me understand:

* How LLM tool calling works
* Tool schemas and structured arguments
* Dynamic tool routing
* JSON argument parsing
* Multi-tool execution
* Agent loops
* Tool results and message sequencing
* Error handling during tool execution
* Calling external APIs from an AI agent
* Connecting LLMs with real-world services
* Using Git and GitHub to version-control an AI project

## 🔮 Future Improvements

Planned improvements include:

* Replace mock flight data with a real flight API
* Add more tools
* Add conversation memory
* Improve error handling and retries
* Add logging
* Add automated tests
* Add streaming responses
* Add evaluation of tool selection
* Containerize the application
* Deploy the agent as an API service

---

**Learning Project — AI Engineer Journey**

