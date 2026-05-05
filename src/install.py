#!/usr/bin/env python3
"""
Create a local virtual environment and install all required libraries.

This file intentionally uses only the Python standard library so it can run
before the project dependencies are installed.
"""

import ctypes
import os
import re
import subprocess
import time
import sys
import venv
import shutil
from datetime import datetime
from pathlib import Path


MINIMUM_PYTHON_VERSION = (3, 10)
PROJECT_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = PROJECT_DIR / ".venv"
REQUIREMENTS_FILE = PROJECT_DIR / "requirements.txt"
LOG_DIR = PROJECT_DIR / "logs"
INSTALL_LOG_FILE = LOG_DIR / "install.log"


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"


def enable_windows_ansi() -> None:
    if (os.name != "nt"):
        return

    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()

        if (kernel32.GetConsoleMode(handle, ctypes.byref(mode))):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


def supports_color() -> bool:
    if (os.environ.get("NO_COLOR")):
        return False

    return sys.stdout.isatty()


USE_COLOR = supports_color()


def color(text: str, style: str) -> str:
    if (not USE_COLOR):
        return text

    return f"{style}{text}{Style.RESET}"


def write_header(title: str) -> None:
    print(color("=" * 64, Style.CYAN))
    print(color(title, Style.BOLD + Style.CYAN))
    print(color("=" * 64, Style.CYAN))
    print(f"Project folder:      {PROJECT_DIR}")
    print(f"Virtual environment: {VENV_DIR}")
    print(f"Installation log:    {INSTALL_LOG_FILE}")
    print()


def write_step(index: int, total: int, message: str) -> None:
    print(color(f"[{index}/{total}] {message}", Style.CYAN))


def write_ok(message: str) -> None:
    print(color(f"[ OK ] {message}", Style.GREEN))


def write_warn(message: str) -> None:
    print(color(f"[WARN] {message}", Style.YELLOW))


def write_error(message: str) -> None:
    print(color(f"[ERROR] {message}", Style.RED))


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


def venv_python_path() -> Path:
    if (os.name == "nt"):
        return (VENV_DIR / "Scripts" / "python.exe")

    return (VENV_DIR / "bin" / "python")


def reset_log_file() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with INSTALL_LOG_FILE.open("w", encoding="utf-8", errors="replace") as log_file:
        log_file.write("PHOTO-CAT dependency installation log\n")
        log_file.write(f"Started: {datetime.now().isoformat(timespec='seconds')}\n")
        log_file.write(f"Project folder: {PROJECT_DIR}\n")
        log_file.write(f"Virtual environment: {VENV_DIR}\n")
        log_file.write("\n")


def append_log(message: str) -> None:
    with INSTALL_LOG_FILE.open("a", encoding="utf-8", errors="replace") as log_file:
        log_file.write(message)
        if (not message.endswith("\n")):
            log_file.write("\n")


def tail_log(max_lines: int = 40) -> list[str]:
    if (not INSTALL_LOG_FILE.is_file()):
        return []

    lines = INSTALL_LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-max_lines:]


def run_logged(command: list[str], description: str) -> bool:
    append_log("=" * 80)
    append_log(description)
    append_log("> " + " ".join(str(part) for part in command))
    append_log("=" * 80)

    with INSTALL_LOG_FILE.open("a", encoding="utf-8", errors="replace") as log_file:
        process = subprocess.run(
            command,
            cwd=PROJECT_DIR,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )

    append_log("")
    append_log(f"Exit code: {process.returncode}")
    append_log("")

    return (process.returncode == 0)


def run_logged_with_progress(
    command: list[str],
    description: str,
    start_percent: int,
    end_percent: int,
    detail: str,
    complete: bool = False,
) -> bool:
    append_log("=" * 80)
    append_log(description)
    append_log("> " + " ".join(str(part) for part in command))
    append_log("=" * 80)

    spinner_frames = ["-", "\\", "|", "/"]
    start_percent = max(0, min(int(start_percent), 100))
    end_percent = max(start_percent, min(int(end_percent), 100))
    span = max(1, end_percent - start_percent)

    with INSTALL_LOG_FILE.open("a", encoding="utf-8", errors="replace") as log_file:
        process = subprocess.Popen(
            command,
            cwd=PROJECT_DIR,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
        )

        frame_index = 0
        started_at = time.monotonic()
        while (process.poll() is None):
            elapsed = time.monotonic() - started_at
            animated_percent = start_percent + min(span - 1, int(elapsed * max(4, span / 2)))
            progress_bar(animated_percent, detail, spinner_frames[frame_index % len(spinner_frames)])
            frame_index += 1
            time.sleep(0.12)

        exit_code = int(process.returncode or 0)

    append_log("")
    append_log(f"Exit code: {exit_code}")
    append_log("")

    if (exit_code == 0):
        progress_bar(end_percent, detail, complete=complete)
        return True

    sys.stdout.write("\n")
    sys.stdout.flush()
    return False

def print_failure_details() -> None:
    write_error("Dependency installation failed.")
    print(f"Detailed log: {INSTALL_LOG_FILE}")

    log_tail = tail_log()
    if (log_tail):
        print()
        print(color("Last log lines:", Style.YELLOW))
        print("-" * 64)
        for line in log_tail:
            print(line)
        print("-" * 64)


def read_requirements() -> list[str]:
    requirements: list[str] = []

    for raw_line in REQUIREMENTS_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()

        if ((not line) or line.startswith("#")):
            continue

        requirements.append(line)

    return requirements


def display_requirement_name(requirement: str) -> str:
    cleaned = requirement.split(";", 1)[0].strip()
    cleaned = re.split(r"[<>=!~]", cleaned, maxsplit=1)[0].strip()
    return (cleaned or requirement)


def install_packages_one_by_one(python_exe: Path, requirements: list[str]) -> bool:
    total = len(requirements)

    for index, requirement in enumerate(requirements, start=1):
        package_name = display_requirement_name(requirement)
        start_percent = int(round(((index - 1) / total) * 100.0))
        end_percent = int(round((index / total) * 100.0))
        detail = f"{index}/{total} [{package_name}]"

        if (not run_logged_with_progress(
            [
                str(python_exe),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                requirement,
            ],
            f"Installing dependency: {requirement}",
            start_percent,
            end_percent,
            detail,
            complete=(index == total),
        )):
            print_failure_details()
            return False

    return True

def main() -> int:
    enable_windows_ansi()
    reset_log_file()

    if (sys.version_info < MINIMUM_PYTHON_VERSION):
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        required_version = f"{MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]}"
        write_error(f"Python {required_version} or newer is required. You are using Python {current_version}.")
        print("Install Python from https://www.python.org/downloads/ and run this again.")
        return 1

    if (not REQUIREMENTS_FILE.is_file()):
        write_error(f"requirements.txt was not found here: {REQUIREMENTS_FILE}")
        return 1

    write_header("PHOTO-CAT - dependency installation")

    write_step(1, 3, "Preparing the local virtual environment...")
    progress_bar(0, "[virtual environment]")
    if (not VENV_DIR.exists()):
        try:
            venv.create(VENV_DIR, with_pip=True)
        except Exception as exc:
            write_error("Could not create the virtual environment.")
            print("On Linux, you may need to install the python3-venv package first.")
            print(f"Details: {exc}")
            append_log(f"ERROR: could not create virtual environment: {exc}")
            return 1

        progress_bar(100, "[virtual environment]", complete=True)
        write_ok("Virtual environment created.")
    else:
        progress_bar(100, "[virtual environment]", complete=True)
        write_ok("Virtual environment already exists. Reusing it.")

    python_exe = venv_python_path()
    if (not python_exe.is_file()):
        write_error(f"Could not find the virtual environment Python here: {python_exe}")
        print("Delete the .venv folder and run the installer again.")
        return 1

    write_step(2, 3, "Updating installation tools...")
    tools = ["pip", "setuptools", "wheel"]
    for index, tool_name in enumerate(tools, start=1):
        start_percent = int(round(((index - 1) / len(tools)) * 100.0))
        end_percent = int(round((index / len(tools)) * 100.0))
        detail = f"{index}/{len(tools)} [{tool_name}]"

        if (not run_logged_with_progress(
            [
                str(python_exe),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--upgrade",
                tool_name,
            ],
            f"Upgrading {tool_name}",
            start_percent,
            end_percent,
            detail,
            complete=(index == len(tools)),
        )):
            print_failure_details()
            return 1

    write_ok("Installation tools are ready.")

    write_step(3, 3, "Installing PHOTO-CAT dependencies...")
    print(color("This may take a few minutes on the first run.", Style.DIM))

    requirements = read_requirements()
    if (not requirements):
        write_error("requirements.txt is empty. There are no dependencies to install.")
        return 1

    if (not install_packages_one_by_one(python_exe, requirements)):
        return 1

    write_ok("Dependencies installed successfully.")
    print()
    print(color("=" * 64, Style.GREEN))
    print(color("PHOTO-CAT is ready.", Style.BOLD + Style.GREEN))
    print(color("=" * 64, Style.GREEN))
    print(f"Detailed installation log: {INSTALL_LOG_FILE}")
    print()
    return 0


if (__name__ == "__main__"):
    raise SystemExit(main())
