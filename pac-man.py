import sys

try:
    import pygame
except ImportError:
    print("❌ [ERROR] Missing dependency: pygame")
    print("Install it with: pip install pygame")
    sys.exit(1)


def main() -> None:
    """
    Run the function-calling pipeline.

    The program validates the input files
    """

    args = parse()
