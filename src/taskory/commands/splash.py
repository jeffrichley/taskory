import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

def load_config(config_file: Path) -> dict:
    config_file.parent.mkdir(parents=True, exist_ok=True)
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}

def save_config(cfg: dict, config_file: Path):
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def show_splash(console: Console):
    ascii_art = '''
[#65007a bold]████████  █████  ███████ ██   ██  ██████  ██████  ██    ██     █████  ██ 
   ██    ██   ██ ██      ██  ██  ██    ██ ██   ██  ██  ██     ██   ██ ██ 
   ██    ███████ ███████ █████   ██    ██ ██████    ████      ███████ ██ 
   ██    ██   ██      ██ ██  ██  ██    ██ ██   ██    ██       ██   ██ ██ 
   ██    ██   ██ ███████ ██   ██  ██████  ██   ██    ██    ██ ██   ██ ██ [/#65007a bold]
[cyan]                                                                         [/cyan]
[white]Your AI-powered task manager[/white]
'''
    splash_text = Align.center(
        Panel(
            ascii_art + "\n[cyan]https://github.com/jeffrichley/taskory[/cyan]",
            title="🚀 Welcome to Taskory!",
            border_style="bold magenta",
            padding=(1, 4),
        ),
        vertical="middle",
    )
    console.print(splash_text)

def maybe_show_splash(console: Console, config_file: Path):
    cfg = load_config(config_file)
    if not cfg.get("splash_shown", False):
        show_splash(console)
        cfg["splash_shown"] = True
        save_config(cfg, config_file) 