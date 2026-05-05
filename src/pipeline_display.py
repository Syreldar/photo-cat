import shutil
import sys
import threading
import time


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[90m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"


def _supports_color() -> bool:
    return sys.stdout.isatty()


USE_COLOR = _supports_color()


def color(text: str, style: str) -> str:
    if (not _supports_color()):
        return text

    return f"{style}{text}{Style.RESET}"


def progress_bar(percent: int, detail: str = "", spinner: str = "", complete: bool = False, width: int = 34) -> None:
    percent = max(0, min(int(percent), 100))

    terminal_width = shutil.get_terminal_size((88, 20)).columns
    max_width = max(42, min(terminal_width - 1, 96))

    prefix = "  "
    percent_text = f"{percent:3d}%"

    suffix_parts = []
    if (spinner):
        suffix_parts.append(str(spinner))
    if (detail):
        suffix_parts.append(str(detail))
    suffix = "  ".join(suffix_parts)

    min_bar_width = 10
    max_bar_width = min(width, 34)
    reserved = len(prefix) + len(percent_text) + 4

    max_suffix_len = max(0, max_width - reserved - min_bar_width - 2)
    if (len(suffix) > max_suffix_len):
        suffix = suffix[:max(0, max_suffix_len - 1)] + "." if (max_suffix_len > 1) else ""

    bar_width = max_width - reserved - len(suffix)
    if (suffix):
        bar_width -= 2
    bar_width = max(min_bar_width, min(max_bar_width, bar_width))

    filled = int(round(bar_width * (percent / 100.0)))
    empty = bar_width - filled

    filled_part = "=" * filled
    empty_part = "-" * empty

    # Clear the current console line before rewriting it. The line is also
    # kept short enough to avoid wrapping when the user resizes the window.
    if (USE_COLOR):
        sys.stdout.write("\r\033[2K")
    else:
        sys.stdout.write("\r" + (" " * max_width) + "\r")

    sys.stdout.write(prefix)
    if (filled_part):
        sys.stdout.write(color(filled_part, Style.MAGENTA))
    if (empty_part):
        sys.stdout.write(color(empty_part, Style.GRAY))
    sys.stdout.write("  ")
    sys.stdout.write(color(percent_text, Style.GREEN))
    if (suffix):
        sys.stdout.write(color(f"  {suffix}", Style.DIM))
    sys.stdout.flush()

    if (complete):
        sys.stdout.write("\n")
        sys.stdout.flush()




class ActivityBar:
    def __init__(self, detail: str, start: int = 2, stop: int = 94, interval: float = 0.12):
        self.detail = detail
        self.start = start
        self.stop = stop
        self.interval = interval
        self._done = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._done.set()
        self._thread.join(timeout=1.0)
        if (exc_type is None):
            progress_bar(100, self.detail, complete=True)
        else:
            progress_bar(100, self.detail, complete=True)
        return False

    def _run(self) -> None:
        percent = self.start
        direction = 1
        while (not self._done.is_set()):
            progress_bar(percent, self.detail, complete=False)
            percent += direction
            if (percent >= self.stop):
                percent = self.stop
                direction = -1
            elif (percent <= self.start):
                percent = self.start
                direction = 1
            self._done.wait(self.interval)


def tqdm_options(desc: str, total_width: int = 88) -> dict:
    return {
        "desc": desc,
        "ncols": None,
        "bar_format": "{desc}: {percentage:3.0f}%|{bar:24}| {n_fmt}/{total_fmt}",
        "dynamic_ncols": True,
        "leave": True,
    }
