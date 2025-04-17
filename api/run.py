import importlib
import os
import json

def list_available_tools(command_data):
    """
    List all tool names present in the 'tools' folder by returning their filenames without the .py extension.

    Args:
        command_data (dict): JSON structure with 'command'.

    Returns:
        dict: JSON response with tool names if the command is 'list_tools'.
    """
    tools_dir = "tools"  # Folder where all tool modules are stored
    tool_names = []

    try:
        # Debugging output
        print(f"Command received: {command_data.get('command')}")
        
        # Validate command type
        if command_data.get("command") != "list_tools":
            return {"error": "Invalid command."}

        # Check if tools directory exists
        if not os.path.exists(tools_dir):
            raise FileNotFoundError(f"Directory '{tools_dir}' not found.")

        print(f"Tools Directory Path: {os.path.abspath(tools_dir)}")
        print(f"Files in Directory: {os.listdir(tools_dir)}")

        # Iterate through all files in the directory
        for file in os.listdir(tools_dir):
            if file.endswith(".py") and not file.startswith("__"):  # Ignore __init__.py and hidden files
                tool_name = file[:-3]  # Remove the '.py' extension
                tool_names.append(tool_name)
        return  tool_names

    except Exception as e:
        return {"error": f"Error accessing tools directory: {e}"}         


def run_tool(command):
    """
    Dynamically run the specified tool or list available tools.

    Args:
        command (dict): JSON command containing the tool name, message, and parameters.

    Returns:
        dict: Response from the executed tool or error details.
    """
    tool_name = command.get("tool", "").strip().lower()
    data = command.get("data", {})
    message = data.get("message", "")
    params = data.get("params", {})

    # Handle 'list_tools' command directly
    if command.get("command") == "list_tools":
        return list_available_tools(command)

    try:
        # Dynamically import the tool module
        module_name = f"tools.{tool_name}"

        print(module_name)
        tool_module = importlib.import_module(module_name)

        if hasattr(tool_module, "run"):
            response = tool_module.run(message, params)
            return {"response": response}
        else:
            return {"status": "error", "message": f"The tool '{tool_name}' does not have a 'run' method."}

    except ModuleNotFoundError:
        return {"status": "error", "message": f"Tool '{tool_name}' not found in the 'tools' folder."}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred while running the tool: {e}"}








# def list_available_tools():
#     """
#     List all tool names present in the 'tools' folder by returning their filenames without the .py extension.

#     Returns:
#         list: A list of tool names (filenames without the .py extension).
#     """
#     tools_dir = "tools"  # Folder where all tool modules are stored
#     tool_names = []

#     try:
#         # Check if tools directory exists
#         if not os.path.exists(tools_dir):
#             raise FileNotFoundError(f"Directory '{tools_dir}' not found.")

#         # Iterate through all files in the directory
#         for file in os.listdir(tools_dir):
#             if file.endswith(".py") and not file.startswith("__"):  # Ignore __init__.py and hidden files
#                 tool_name = file[:-3]  # Remove the '.py' extension
#                 tool_names.append(tool_name)

#     except Exception as e:
#         print(f"Error accessing tools directory: {e}")

#     return tool_names

# _______________________

# def run_tool(command):
#     """
#     Dynamically run the specified tool by importing its module and calling the `run` method with multiple arguments.

#     Args:
#         command (dict): JSON command containing the tool name, message, and parameters.

#     Returns:
#         dict: Response from the executed tool or error details.
#     """
#     tool_name = command.get("tool", "").lower()  # Get the tool name and convert to lowercase
#     data = command.get("data", {})
#     message = data.get("message", "")  # Get the message (query)
#     params = data.get("params", {})  # Get the params (arguments like URL)

#     try:
#         # Dynamically import the tool module (e.g., tools.smart_scraper)
#         module_name = f"tools.{tool_name}"
#         tool_module = importlib.import_module(module_name)

#         # Check if the module has a `run` method
#         if hasattr(tool_module, "run"):
#             # Call the `run()` method with the message and params
#             response = tool_module.run(message, params)  # Pass both message and params
#             return {"status": "success", "response": response}
#         else:
#             return {"status": "error", "message": f"The tool '{tool_name}' does not have a 'run' method."}

#     except ModuleNotFoundError:
#         return {"status": "error", "message": f"Tool '{tool_name}' not found in the 'tools' folder."}
#     except Exception as e:
#         return {"status": "error", "message": f"An error occurred while running the tool: {e}"}
