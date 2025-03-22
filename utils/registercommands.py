import os
import importlib.util
import glob

async def register_commands(bot):
    # First, clear all existing global commands
    bot.tree.clear_commands(guild=None)
    print("Cleared all global commands.")

    # Path to the commands folder
    commands_path = os.path.join(os.path.dirname(__file__), "commands")
    # Get all Python files in the commands folder
    command_files = glob.glob(os.path.join(commands_path, "*.py"))
    
    for command_file in command_files:
        # Skip __init__.py if it exists
        if os.path.basename(command_file) == "__init__.py":
            continue
        
        module_name = os.path.splitext(os.path.basename(command_file))[0]
        spec = importlib.util.spec_from_file_location(module_name, command_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "setup"):
            module.setup(bot)
            print(f"Registered command module: {module_name}")
        else:
            print(f"Module {module_name} does not have a setup(bot) function; skipping.")
    
    # Sync all commands globally
    await bot.tree.sync(guild=None)
    print("Globally synced all slash commands.")
