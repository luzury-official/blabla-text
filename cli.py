import core
from simple_term_menu import TerminalMenu # Terminal Menu
from art import tprint # Big text print
from rich import print
from rich.console import Console
from rich.progress import track
import time

console = Console()

tprint("BlaBla-Text")

def synthesize():
    settings = core.load_settings().get("default_synthesize", {
        "model": "facebook/mms-tts-eng",
        "lang": "en",
        "voice": "default"
    })

    print("[bold cyan]Settings of synesthize speech:[/bold cyan]")
    print(f"Model: [green]{settings.get('model', 'не задана')}[/green]")
    print(f"Lang: [green]{settings.get('lang', 'не задан')}[/green]")
    print(f"Voice: [green]{settings.get('voice', 'не задан')}[/green]\n\n")

    options = ["1. Change model", "2. Change language", "3. Change voice, if it possible for choosed model", "4. Start", "5. Back"]

    settings_menu = TerminalMenu(
        options,
        title="Choose option",
        menu_cursor="> ",
        menu_cursor_style=("fg_cyan", "bold"),
        menu_highlight_style=("bg_cyan", "fg_black")
    )

    menu_entry_index = settings_menu.show()

    if menu_entry_index == 0:
        console.clear()
        installed = ["1. " + core.get_installed_models(), "2. New model", "3. Back"]

        installed_menu = TerminalMenu(
            installed,
            title="Choose model",
            menu_cursor="> ",
            menu_cursor_style=("fg_cyan", "bold"),
            menu_highlight_style=("bg_cyan", "fg_black")
        )

        installed_menu_entry_index = installed_menu.show()
        selected_option = options[menu_entry_index]

        if "Back" in selected_option:
            pass
        elif "2. New model" in selected_option:
            input("Enter a link of selected model")
            # Checks is link correct
            # Using link in a synthesizing
        else:
            settings["default_synthesize"]["model"] = if "1. " in selected_option: selected_option - "1. " else: sected_option



while True:
    options = ["1. Synthesize speech", "2. My models", "3. Exit"]
    
    terminal_menu = TerminalMenu(
        options,
        title="Choose option",
        menu_cursor="> ",
        menu_cursor_style=("fg_cyan", "bold"),
        menu_highlight_style=("bg_cyan", "fg_black")
    )

    menu_entry_index = terminal_menu.show()

    if menu_entry_index is None:
        print("Exiting...")
        console.clear()
        break

    elif menu_entry_index == 0:
        console.clear()
        synthesize()