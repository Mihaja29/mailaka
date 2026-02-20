"""Display utilities for styled terminal output.
"""

import click

# Color palette - Anthropic dark theme inspired
COLORS = {
    'bg': '\033[48;2;13;13;13m',
    'fg': '\033[38;2;224;224;224m',
    'fg_dim': '\033[38;2;150;150;150m',
    'accent': '\033[38;2;200;50;50m',
    'accent_bold': '\033[38;2;220;80;80m',
    'success': '\033[38;2;50;180;90m',
    'warning': '\033[38;2;220;180;50m',
    'border': '\033[38;2;80;80;80m',
    'reset': '\033[0m',
}

# Legacy for compatibility
FG_GREY_PEARL = COLORS['fg']
FG_RED_FLUO = COLORS['accent']
FG_BLUE_NIGHT = '\033[38;2;40;50;80m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = COLORS['reset']

BANNER = f"""
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  ███╗   ███╗ █████╗ ██╗██╗      █████╗ ██╗  ██╗ █████╗     │
  │  ████╗ ████║██╔══██╗██║██║     ██╔══██╗██║ ██╔╝██╔══██╗    │
  │  ██╔████╔██║███████║██║██║     ███████║█████╔╝ ███████║    │
  │  ██║╚██╔╝██║██╔══██║██║██║     ██╔══██║██╔═██╗ ██╔══██║    │
  │  ██║ ╚═╝ ██║██║  ██║██║███████╗██║  ██║██║  ██╗██║  ██║    │
  │  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
{RESET}"""


def styled(text, fg=None, bold=False):
    """Apply style to text."""
    fg = fg or COLORS['fg']
    b = BOLD if bold else ""
    return f"{b}{fg}{text}{RESET}"


def echo(text, fg=None, bold=False):
    """Echo styled text to console."""
    fg = fg or COLORS['fg']
    click.echo(styled(text, fg=fg, bold=bold))


def echo_separator(width=60):
    """Echo top border of card."""
    click.echo(styled(f"  ┌{'─' * width}┐", fg=COLORS['border']))


def echo_error(text):
    """Echo error message."""
    click.echo(styled(f"  [✖] {text}", fg=COLORS['accent'], bold=True))


def echo_success(text):
    """Echo success message."""
    click.echo(styled(f"  [✔] {text}", fg=COLORS['success']))


def _display_width(text):
    """Calculate display width (accounts for ANSI codes)."""
    import re
    # Remove ANSI escape sequences
    clean = re.sub(r'\033\[[0-9;]*m', '', text)
    return len(clean)


def echo_card_header(title, width=60):
    """Display card header with title in RED."""
    # Title styled in red
    styled_title = styled(title, fg=COLORS['accent'], bold=True)
    
    # Calculate padding
    title_width = len(title)
    total_padding = width - title_width
    left = total_padding // 2
    right = total_padding - left
    
    # Build line: left border + left padding + title + right padding + right border
    border_left = styled("  ┌", fg=COLORS['border'])
    border_right = styled("┐", fg=COLORS['border'])
    padding_left = "─" * left
    padding_right = "─" * right
    
    click.echo(f"{border_left}{padding_left} {styled_title} {padding_right}{border_right}")


def echo_card_line(content, width=60, fg=None):
    """Display card content line."""
    fg = fg or COLORS['fg']
    content_styled = styled(content, fg=fg)
    
    # Calculate exact padding needed
    content_len = len(content)
    padding = width - content_len
    if padding < 0:
        padding = 0
    
    border_left = styled("  │ ", fg=COLORS['border'])
    border_right = styled("│", fg=COLORS['border'])
    
    click.echo(f"{border_left}{content_styled}{' ' * padding}{border_right}")


def echo_separator_close(width=60):
    """Echo closing separator."""
    border = styled("  └", fg=COLORS['border']) + styled("─" * width, fg=COLORS['border']) + styled("┘", fg=COLORS['border'])
    click.echo(border)


def echo_card_kv(key, value, width=60, key_width=15):
    """Display key-value pair in card."""
    key_str = f"{key}:".ljust(key_width)
    val_str = str(value)
    remaining = width - key_width - 1
    if len(val_str) > remaining:
        val_str = val_str[:remaining-3] + "..."
    line = f"{key_str}{val_str}"
    echo_card_line(line, width)


def echo_section(title, width=60):
    """Display section title in red."""
    echo_card_header(title, width)


def echo_section_end(width=60):
    """Close section."""
    echo_separator_close(width)
    click.echo()


def echo_check(text):
    """Echo success with checkmark."""
    click.echo(styled(f"  ✔ {text}", fg=COLORS['success']))


def echo_cross(text):
    """Echo error with cross."""
    click.echo(styled(f"  ✖ {text}", fg=COLORS['accent'], bold=True))
