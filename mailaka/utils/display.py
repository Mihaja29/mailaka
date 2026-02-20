"""Display utilities for styled terminal output."""

import click

# Color definitions
FG_GREY_PEARL = "\033[38;2;224;224;224m"
FG_RED_FLUO = "\033[38;2;255;51;51m"
FG_BLUE_NIGHT = "\033[38;2;18;30;64m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

BANNER = f"""
  {FG_RED_FLUO}{BOLD}███╗   ███╗ █████╗ ██╗██╗      █████╗ ██╗  ██╗ █████╗{RESET}
  {FG_RED_FLUO}{BOLD}████╗ ████║██╔══██╗██║██║     ██╔══██╗██║ ██╔╝██╔══██╗{RESET}
  {FG_RED_FLUO}{BOLD}██╔████╔██║███████║██║██║     ███████║█████╔╝ ███████║{RESET}
  {FG_RED_FLUO}{BOLD}██║╚██╔╝██║██╔══██║██║██║     ██╔══██║██╔═██╗ ██╔══██║{RESET}
  {FG_RED_FLUO}{BOLD}██║ ╚═╝ ██║██║  ██║██║███████╗██║  ██║██║  ██╗██║  ██║{RESET}
  {FG_RED_FLUO}{BOLD}╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{RESET}
"""


def styled(text, fg=FG_GREY_PEARL, bold=False):
    """Apply style to text.
    
    Args:
        text: Text to style
        fg: Foreground color code
        bold: Whether to apply bold style
        
    Returns:
        Styled text string
    """
    b = BOLD if bold else ""
    return f"{b}{fg}{text}{RESET}"


def echo(text, fg=FG_GREY_PEARL, bold=False):
    """Echo styled text to console.
    
    Args:
        text: Text to display
        fg: Foreground color code
        bold: Whether to apply bold style
    """
    click.echo(styled(text, fg=fg, bold=bold))


def echo_error(text):
    """Echo error message.
    
    Args:
        text: Error message to display
    """
    click.echo(styled(f"  [ERREUR] {text}", fg=FG_RED_FLUO, bold=True), err=True)


def echo_success(text):
    """Echo success message.
    
    Args:
        text: Success message to display
    """
    click.echo(styled(f"  [OK] {text}", fg=FG_GREY_PEARL, bold=True))


def echo_separator():
    """Echo a separator line."""
    click.echo(styled("  " + "─" * 56, fg=FG_GREY_PEARL))
