import core
from simple_term_menu import TerminalMenu
from art import tprint
from rich import print
from rich.console import Console
from rich.table import Table
import os

console = Console()

def synthesize():
    full_settings = core.load_settings()
    settings = full_settings.get("default_synthesize", {
        "model": core.DEFAULT_MODEL,
        "lang": "en",
        "speaker": 6
    })

    while True:
        console.clear()
        print("[bold cyan]Settings of synthesize speech:[/bold cyan]")
        print(f"Model: [green]{settings.get('model', 'Not set')}[/green]")
        print(f"Lang: [green]{settings.get('lang', 'Not set')}[/green]")
        print(f"Speaker: [green]{settings.get('speaker', 'Not set')}[/green]\n\n")

        options = ["1. Change model", "2. Change language", "3. Change speaker", "4. Start", "5. Back"]

        settings_menu = TerminalMenu(
            options,
            title="Choose option",
            menu_cursor="> ",
            menu_cursor_style=("fg_cyan", "bold"),
            menu_highlight_style=("bg_cyan", "fg_black")
        )

        menu_entry_index = settings_menu.show()

        if menu_entry_index is None or menu_entry_index == 4:
            break

        elif menu_entry_index == 0:
            installed_models = core.get_installed_models()
            installed_options = installed_models + ["New model", "Back"]

            installed_menu = TerminalMenu(
                installed_options,
                title="Choose model",
                menu_cursor="> ",
                menu_cursor_style=("fg_cyan", "bold"),
                menu_highlight_style=("bg_cyan", "fg_black")
            )

            installed_idx = installed_menu.show()
            if installed_idx is not None:
                selected_model = installed_options[installed_idx]
                if selected_model == "Back":
                    continue
                elif selected_model == "New model":
                    console.clear()
                    new_model = input("Enter a link or ID of selected model (e.g. suno/bark-small): ")
                    if new_model.strip():
                        settings["model"] = new_model.strip()
                else:
                    settings["model"] = selected_model

                full_settings["default_synthesize"] = settings
                core.save_settings(full_settings)

        elif menu_entry_index == 1:
            langs = list(core.SUPPORTED_LANGUAGES.keys()) + ["Back"]
            lang_menu = TerminalMenu(
                langs,
                title="Choose language",
                menu_cursor="> ",
                menu_cursor_style=("fg_cyan", "bold"),
                menu_highlight_style=("bg_cyan", "fg_black")
            )
            lang_idx = lang_menu.show()
            if lang_idx is not None:
                selected_lang = langs[lang_idx]
                if selected_lang != "Back":
                    settings["lang"] = selected_lang
                    full_settings["default_synthesize"] = settings
                    core.save_settings(full_settings)

        elif menu_entry_index == 2:
            speakers = [str(i) for i in range(10)] + ["Back"]
            speaker_menu = TerminalMenu(
                speakers,
                title="Choose speaker (0-9)",
                menu_cursor="> ",
                menu_cursor_style=("fg_cyan", "bold"),
                menu_highlight_style=("bg_cyan", "fg_black")
            )
            speaker_idx = speaker_menu.show()
            if speaker_idx is not None:
                selected_speaker = speakers[speaker_idx]
                if selected_speaker != "Back":
                    settings["speaker"] = int(selected_speaker)
                    full_settings["default_synthesize"] = settings
                    core.save_settings(full_settings)

        elif menu_entry_index == 3:
            input_options = ["1. Enter text manually", "2. Choose a text file", "3. Back"]
            input_menu = TerminalMenu(
                input_options,
                title="How do you want to input text?",
                menu_cursor="> ",
                menu_cursor_style=("fg_cyan", "bold"),
                menu_highlight_style=("bg_cyan", "fg_black")
            )

            input_idx = input_menu.show()

            if input_idx is None or input_idx == 2:
                continue

            text = ""
            if input_idx == 0:
                text = input("Enter text to synthesize: ")
            elif input_idx == 1:
                file_path = input("Enter path to the text file: ")
                try:
                    with open(file_path.strip(), 'r', encoding='utf-8') as f:
                        text = f.read()
                except Exception as e:
                    print(f"\n[bold red]Error reading file:[/bold red] {e}")
                    input("\nPress Enter to continue...")
                    continue

            if text.strip():
                output_file = input("Enter output filename (e.g. result.wav): ")
                if not output_file.strip():
                    output_file = "result.wav"

                try:
                    print("\n[bold yellow]Synthesizing...[/bold yellow]")
                    core.synthesize_speech(
                        text.strip(),
                        output_file,
                        settings["lang"],
                        settings["model"],
                        settings.get("speaker", 6)
                    )
                    print(f"\n[bold green]Success! Audio saved to {output_file}[/bold green]")
                except Exception as e:
                    print(f"\n[bold red]Error:[/bold red] {e}")

                input("\nPress Enter to return...")
            else:
                print("\n[bold red]Text cannot be empty.[/bold red]")
                input("\nPress Enter to continue...")


def manage_models():
    while True:
        console.clear()
        models = core.get_installed_models()

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Installed Models", style="green")

        if models:
            for m in models:
                table.add_row(m)
        else:
            table.add_row("[yellow]No models installed yet.[/yellow]")

        console.print(table)
        print("\n")

        options = ["1. Download model", "2. Delete model", "3. Back"]
        model_menu = TerminalMenu(
            options,
            title="Manage models",
            menu_cursor="> ",
            menu_cursor_style=("fg_cyan", "bold"),
            menu_highlight_style=("bg_cyan", "fg_black")
        )

        choice = model_menu.show()

        if choice is None or choice == 2:
            break

        elif choice == 0:
            console.clear()
            model_id = input("Enter model ID to download (e.g. suno/bark-small): ")
            if model_id.strip():
                print(f"\n[bold yellow]Downloading {model_id.strip()}...[/bold yellow]")
                try:
                    core.download_model(model_id.strip())
                    print("[bold green]Model downloaded successfully![/bold green]")
                except Exception as e:
                    print(f"[bold red]Error downloading model:[/bold red] {e}")
                input("\nPress Enter to continue...")

        elif choice == 1:
            if not models:
                console.clear()
                print("[bold red]No models available to delete.[/bold red]")
                input("\nPress Enter to continue...")
                continue

            console.clear()
            del_menu = TerminalMenu(
                models + ["Back"],
                title="Select model to delete",
                menu_cursor="> ",
                menu_cursor_style=("fg_red", "bold"),
                menu_highlight_style=("bg_red", "fg_gray")
            )
            del_idx = del_menu.show()

            if del_idx is not None and del_idx < len(models):
                selected_model = models[del_idx]
                console.clear()
                confirm = input(f"Are you sure you want to delete '{selected_model}'? (y/n): ")
                if confirm.lower() == 'y':
                    if core.delete_model(selected_model):
                        print("[bold green]Model deleted successfully.[/bold green]")
                    else:
                        print("[bold red]Failed to delete model. Folder might not exist.[/bold red]")
                else:
                    print("[bold yellow]Deletion cancelled.[/bold yellow]")
                input("\nPress Enter to continue...")


def main():
    while True:
        console.clear()
        tprint("BlaBla-Text")
        options = ["1. Synthesize speech", "2. My models", "3. Exit"]

        terminal_menu = TerminalMenu(
            options,
            title="Choose option",
            menu_cursor="> ",
            menu_cursor_style=("fg_cyan", "bold"),
            menu_highlight_style=("bg_cyan", "fg_black")
        )

        menu_entry_index = terminal_menu.show()

        if menu_entry_index is None or menu_entry_index == 2:
            console.clear()
            break

        elif menu_entry_index == 0:
            synthesize()

        elif menu_entry_index == 1:
            manage_models()

if __name__ == "__main__":
    main()