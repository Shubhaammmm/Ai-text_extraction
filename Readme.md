# WebSocket Tool Server

This project is a WebSocket-based server that allows clients to invoke tools dynamically by sending commands. Each tool performs a specific function and can be easily extended or modified.

## Features
- Dynamically handle multiple tools.
- Simple architecture for adding new tools.
- Communicates over WebSocket for real-time interaction.
- Communicates using Fastapi.

## Installation

1) Step 1 :- Set up a virtual environment:  
> python3 -m venv venv

> source venv/bin/activate

2) Step2  :- Install the dependencies:
> pip install -r requirements.txt

3) Step 3 :- Run the WebSocket server:
> venv/bin/python main.py

### How It Works
The server listens for incoming WebSocket connections on ws://localhost:8769.
Clients send commands in JSON format to invoke specific tools.
The server processes the command, runs the appropriate tool, and sends back the result.







## New Requirements
+ 