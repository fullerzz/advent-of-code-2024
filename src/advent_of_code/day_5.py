from pathlib import Path

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

console = Console()


class Elem(BaseModel):
    val: int
    prereqs: list[int] = []


def read_input() -> list[str]:
    input_path = Path("input") / "day5.txt"
    console.print("[bold cyan]Reading input file: [/bold cyan]" + str(input_path))
    with input_path.open() as f:
        return f.readlines()


def parse_rules(lines: list[str]) -> dict[int, list[int]]:
    rules: dict[int, list[int]] = {}
    for line in lines:
        console.print(line)
        if line.find("|") == -1 or line == "\n":
            break
        parts = line.split("|")
        prereq = int(parts[0].strip())
        val = int(parts[1].strip())
        existing_prereqs = rules.get(val, [])
        existing_prereqs.append(prereq)
        rules[val] = existing_prereqs
    return rules


def part_1(lines: list[str]) -> None:
    rules = parse_rules(lines)
    console.print(Panel(f"[bold green]{rules=} [/]", title="[bold cyan]Day 1 - Part 1[/]", expand=False))


def part_2() -> None:
    pass


def main() -> None:
    lines = read_input()
    part_1(lines)
    part_2()


if __name__ == "__main__":
    main()
