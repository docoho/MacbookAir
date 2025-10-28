#!/usr/bin/env python3
"""Entry point script providing basic hello world functionality."""

def hello_world() -> str:
    """Return the classic greeting string."""
    return "Hello, world!"


def main() -> None:
    """Execute the script when run directly."""
    print(hello_world())


if __name__ == "__main__":
    main()
