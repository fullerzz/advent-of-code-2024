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
        if line.find("|") == -1 or line == "\n":
            break
        parts = line.split("|")
        prereq = int(parts[0].strip())
        val = int(parts[1].strip())
        existing_prereqs = rules.get(val, [])
        existing_prereqs.append(prereq)
        rules[val] = existing_prereqs
    return rules


def parse_updates(lines: list[str]) -> list[list[int]]:
    updates: list[list[int]] = []
    second_section = False
    for line in lines:
        if not second_section and (line.find("|") == -1 or line == "\n"):
            second_section = True
            continue
        if not second_section:
            continue
        update_pages = line.split(",")
        update = [int(page) for page in update_pages]
        updates.append(update)
    return updates


def prereq_met(update: list[int], prereq: int, val: int) -> bool:
    prereq_index = -1
    val_index = -1
    for index, page in enumerate(update):
        if page == val:
            val_index = index
        if page == prereq:
            prereq_index = index
    if prereq_index == -1:
        return True
    else:
        return prereq_index < val_index


def validate_update(update: list[int], rules: dict[int, list[int]]) -> bool:
    for page in update:
        page_rules = rules.get(page, [])
        if page_rules != []:
            console.print(f"Need to validate rules for {page=}")
            console.print(f"{page_rules=}")
            for rule in page_rules:
                if not prereq_met(update, rule, page):
                    return False
    return True


def validate_updates_against_rules(updates: list[list[int]], rules: dict[int, list[int]]) -> list[list[int]]:
    """
    Returns subset of updates that are valid
    """
    valid_updates: list[list[int]] = []
    for update in updates:
        if validate_update(update, rules) is True:
            valid_updates.append(update)  # noqa: PERF401
    return valid_updates


def sum_middle_page_nums(valid_updates: list[list[int]]) -> int:
    vals: list[int] = []
    for update in valid_updates:
        middle_index = int(len(update) / 2)
        vals.append(update[middle_index])
    return sum(vals)


def part_1(lines: list[str]) -> None:
    rules = parse_rules(lines)
    updates = parse_updates(lines)
    valid_updates = validate_updates_against_rules(updates, rules)
    total = sum_middle_page_nums(valid_updates)
    console.print(Panel(f"[bold green]{total=} [/]", title="[bold cyan]Day 5 - Part 1[/]", expand=False))


def part_2() -> None:
    pass


def main() -> None:
    lines = read_input()
    part_1(lines)
    part_2()


if __name__ == "__main__":
    main()
