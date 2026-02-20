"""Display utilities for styled terminal output."""

import click
import shutil

# Color palette - Anthropic dark theme inspired
COLORS = {
    'bg': '\033[48;2;13;13;13m',
    'fg': '\033[38;2;224;224;224m',
    'fg_dim': '\033[38;2;150;150;150m',
    'accent': '\033[38;2;190;65;65m',
    'accent_bold': '\033[38;2;220;80;80m',
    'success': '\033[38;2;50;180;90m',
    'warning': '\033[38;2;220;180;50m',
    'border': '\033[38;2;60;60;60m',
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


def styled(text, fg=None, bold=False, dim=False):
    """Apply style to text."""
    fg = fg or COLORS['fg']
    b = BOLD if bold else ""
    d = DIM if dim else ""
    return f"{b}{d}{fg}{text}{RESET}"


def echo(text, fg=None, bold=False):
    """Echo styled text to console."""
    fg = fg or COLORS['fg']
    click.echo(styled(text, fg=fg, bold=bold))


def echo_error(text):
    """Echo error message."""
    click.echo(styled(f"  ✖ {text}", fg=COLORS['accent'], bold=True), err=True)


def echo_success(text):
    """Echo success message."""
    click.echo(styled(f"  ✔ {text}", fg=COLORS['success']))


def echo_separator(width=60):
    """Echo a separator line."""
    click.echo(styled("  ┌" + "─" * width + "┐", fg=COLORS['border']))


def echo_separator_close(width=60):
    """Echo closing separator."""
    click.echo(styled("  └" + "─" * width + "┘", fg=COLORS['border']))


def echo_card_header(title, width=60):
    """Display card header with title."""
    padding = width - len(title) - 4
    left = padding // 2
    right = padding - left
    line = "─" * left + " " + title + " " + "─" * right
    click.echo(styled(f"  ┌{line}┐", fg=COLORS['border'], bold=True))


def echo_card_line(content, width=60, fg=None):
    """Display card content line."""
    fg = fg or COLORS['fg']
    padding = width - len(content)
    line = content + " " * padding
    click.echo(styled(f"  │ {line}│", fg=fg))


def echo_card_kv(key, value, width=60, key_width=20):
    """Display key-value pair in card."""
    key_str = f"{key}:".ljust(key_width)
    val_str = str(value)
    remaining = width - key_width - 3
    if len(val_str) > remaining:
        val_str = val_str[:remaining-3] + "..."
    line = f"{key_str}{val_str}"
    padding = width - len(line)
    click.echo(styled(f"  │ {line}{' '*padding}│", fg=COLORS['fg']))


def echo_section(title):
    """Display section title."""
    click.echo()
    echo_card_header(title)


def echo_section_end(width=60):
    """Close section."""
    echo_separator_close(width)
    click.echo()


def echo_panel(title, content_lines, width=60):
    """Display a full panel."""
    echo_card_header(title, width)
    for line in content_lines:
        if isinstance(line, tuple):
            text, fg = line
        else:
            text, fg = line, COLORS['fg']
        echo_card_line(text, width, fg)
    echo_separator_close(width)


def echo_stat_card(label, value, change=None, trend=None):
    """Display stat card like Anthropic dashboard."""
    width = 28
    change_str = f"{change:+.0f}%" if change else ""
    change_fg = COLORS['success'] if trend == 'up' else COLORS['accent'] if trend == 'down' else COLORS['fg_dim']
    
    lines = [
        "",
        f"  {label}",
        "",
        f"  {BOLD}{value}{RESET}",
        "",
    ]
    if change:
        lines.append(f"  {styled(change_str, fg=change_fg)}{' '*(width-8-len(change_str))}")
    else:
        lines.append(" " * width)
    lines.append("")
    
    click.echo(styled(f"  ┌{'─'*width}┐", fg=COLORS['border']))
    for i, line in enumerate(lines):
        content = line.ljust(width-2)
        fg = COLORS['fg_dim'] if i == 1 else COLORS['fg']
        if i == 3:
            content = f"  {BOLD}{value}{RESET}{' '*(width-2-len(str(value)))}"
            click.echo(styled(f"  │{content}│", fg=COLORS['fg']))
        else:
            click.echo(styled(f"  │{content}│", fg=fg))
    click.echo(styled(f"  └{'─'*width}┘", fg=COLORS['border']))


def echo_status_bar(current, total, label="Progress"):
    """Display progress bar."""
    width = 50
    filled = int(width * current / total) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    percent = int(100 * current / total) if total > 0 else 0
    click.echo(styled(f"  {label}: [{bar}] {percent}%", fg=COLORS['fg_dim']))


def echo_check(text):
    """Echo success with checkmark."""
    click.echo(styled(f"  ✔ {text}", fg=COLORS['success']))


def echo_cross(text):
    """Echo error with cross."""
    click.echo(styled(f"  ✖ {text}", fg=COLORS['accent'], bold=True))
