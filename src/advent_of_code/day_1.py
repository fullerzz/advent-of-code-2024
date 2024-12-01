from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def read_input() -> list[str]:
    input_path = Path("input") / "day1.txt"
    console.print("[bold cyan]Reading input file: [/bold cyan]" + str(input_path))
    with input_path.open() as f:
        return f.read().splitlines()


def separate_input(input_lines: list[str]) -> tuple[list[int], list[int]]:
    list_a = []
    list_b = []
    for line in input_lines:
        vals = line.split("   ")
        list_a.append(int(vals[0]))
        list_b.append(int(vals[1]))
    return list_a, list_b


def calculate_distance(list_a: list[int], list_b: list[int]) -> int:
    distance = 0
    for val_a, val_b in zip(list_a, list_b, strict=True):
        distance = distance + abs(val_a - val_b)
    return distance


def part_1() -> None:
    input_lines = read_input()
    list_a, list_b = separate_input(input_lines)

    list_a.sort()
    list_b.sort()

    distance = calculate_distance(list_a, list_b)
    console.print(Panel(f"[bold green]{distance=} [/]", title="[bold cyan]Day 1 - Part 1[/]", expand=False))


def create_val_map(list_a: list[int]) -> dict[int, int]:
    val_map = {}
    for val in list_a:
        val_map[val] = 0
    return val_map


def count_occurrences_in_list_b(val: int, list_b: list[int]) -> int:
    return sum(1 for element in list_b if element == val)


def calculate_similarity_score(list_a: list[int], list_b: list[int]) -> int:
    total = 0
    for val in list_a:
        total = total + (val * count_occurrences_in_list_b(val, list_b))
    return total


def part_2() -> None:
    input_lines = read_input()
    list_a, list_b = separate_input(input_lines)
    list_a.sort()
    list_b.sort()
    score = calculate_similarity_score(list_a, list_b)
    console.print(Panel(f"[bold green]{score=} [/]", title="[bold purple]Day 1 - Part 2[/]", expand=False))


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()
