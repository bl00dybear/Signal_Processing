import sys
from rich.console import Console
from rich.style import Style
import pyfiglet
import questionary
from questionary import Style as QStyle

from encodeing_pipeline.encodeing_pipeline import process_encoding_pipeline 

console = Console()

calm_style = QStyle([
    ('qmark', 'fg:cyan bold'),
    ('question', 'fg:cyan bold'),
    ('answer', 'fg:white bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold'),
    ('selected', 'fg:white'),
    ('separator', 'fg:blue dim'),
    ('instruction', 'fg:blue dim'),
    ('text', 'fg:blue'),
    ('disabled', 'fg:grey italic')
])

def print_banner():
    console.clear()
    ascii_banner = pyfiglet.figlet_format("JPEG  ENCODER", font="slant")
    console.print(f"{'='*75}", style="dim cyan")
    console.print(ascii_banner, style="bold cyan")
    console.print(f"{'='*75}", style="dim cyan")



def main():
    while True:
        print_banner()
        
        action = questionary.select(
            "SELECT_OPERATION >>",
            choices=[
                "0x01 :: START_COMPRESSION",
                "0x00 :: EXIT"
            ],
            style=calm_style,
            pointer=">>",
            use_indicator=False,
            instruction="(USE_ARROWS)"
        ).ask()

        if action == "0x00 :: EXIT":
            console.print("\n[bold cyan][!] PROCESS TERMINATED.[/bold cyan]")
            sys.exit()
            
        elif action == "0x01 :: START_COMPRESSION":
            path = questionary.path(
                "INPUT_RAW_FILE >>",
                style=calm_style,
                validate=lambda text: True if len(text) > 0 else "INVALID_PATH"
            ).ask()
            
            if path:
                process_encoding_pipeline(path,console)
                questionary.press_any_key_to_continue(
                    "PRESS_ANY_KEY_TO_RESET...",
                    style=calm_style
                ).ask()

if __name__ == "__main__":
    main()