import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add project root to sys.path to support imports like `from api.run import run_tool`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.run import run_tool  # Dynamic tool executor

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def execute_tool(request: Request):
    """
    Endpoint to execute a tool by passing query parameters:
    - tool: tool name
    - message: optional message
    - other query params are passed to the tool
    """
    try:
        params = dict(request.query_params)
        tool = params.pop("tool", None)
        message = params.pop("message", "")

        if not tool:
            raise HTTPException(status_code=400, detail="Tool parameter is required")

        command = {
            "command": "run",
            "tool": tool,
            "data": {"message": message, "params": params}
        }

        response = run_tool(command)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.post("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "running"}

async def run_fastapi_server():
    """
    Starts the FastAPI server with configurable host and port.
    """
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 6003))

    config = uvicorn.Config(app, host=host, port=port, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()
