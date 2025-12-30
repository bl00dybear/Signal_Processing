import sys
from rich.console import Console
from rich.style import Style
import pyfiglet
import questionary
from questionary import Style as QStyle

from encoding_pipeline.encoding_pipeline import process_encoding_pipeline 
from decoding_pipeline.decoding_pipeline import process_decoding_pipeline


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
                "0x01 :: START_JPEG_ENCODING",
                "0x02 :: START_JPEG_DECODING",
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
            
        elif action == "0x01 :: START_JPEG_ENCODING":
            path = questionary.path(
                "INPUT_RAW_FILE >>",
                style=calm_style,
                validate=lambda text: True if len(text) > 0 else "INVALID_PATH"
            ).ask()
            
            if path:
                mse_trheshold = questionary.text(
                    "MSE THRESHOLD >>",
                    style=calm_style,
                    validate=lambda text: True if text.isdigit() and 1 <= int(text) <= 255**2 else "INVALID_NUMBER (1-65025)"
                ).ask()
                
                if mse_trheshold:
                    mse_trheshold = int(mse_trheshold)
                    process_encoding_pipeline(path, console, mse_trheshold)
                    questionary.press_any_key_to_continue(
                        "PRESS_ANY_KEY_TO_RESET...",
                        style=calm_style
                    ).ask()

        elif action == "0x02 :: START_JPEG_DECODING":
            path = questionary.path(
                "INPUT_RAW_FILE >>",
                style=calm_style,
                validate=lambda text: True if len(text) > 0 else "INVALID_PATH"
            ).ask()
            
            if path:
                process_decoding_pipeline(path,console)
                questionary.press_any_key_to_continue(
                    "PRESS_ANY_KEY_TO_RESET...",
                    style=calm_style
                ).ask()
        

if __name__ == "__main__":
    main()