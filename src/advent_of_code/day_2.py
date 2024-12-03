import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def read_input() -> list[str]:
    input_path = Path("input") / "day2.txt"
    console.print("[bold cyan]Reading input file: [/bold cyan]" + str(input_path))
    with input_path.open() as f:
        return f.read().splitlines()


def check_trend(increasing: bool, decreasing: bool, trend: Literal["increasing", "decreasing"]) -> bool:
    if trend == "increasing" and decreasing is True:  # noqa: SIM114
        return False
    elif trend == "decreasing" and increasing is True:  # noqa: SIM103
        return False
    else:
        return True


def valid_difference(elem_a: int, elem_b: int) -> bool:
    difference = abs(elem_a - elem_b)
    return difference >= 1 and difference <= 3


def check_rules_curr_next(curr: int, nxt: int, increasing: bool, decreasing: bool) -> bool:
    if nxt < curr:
        decreasing = True
        valid_trend = check_trend(increasing, decreasing, "decreasing")
    elif nxt > curr:
        increasing = True
        valid_trend = check_trend(increasing, decreasing, "increasing")
    else:
        return False
    if not valid_trend:
        return False
    # Assume trend is valid at this point, so check difference between current and next
    return valid_difference(int(curr), int(nxt))


def report_is_safe(report: str) -> bool:
    levels = report.split(" ")
    increasing, decreasing = False, False
    for i in range(len(levels)):
        curr = int(levels[i])
        prev, nxt = None, None
        if i > 0:
            prev = int(levels[i - 1])
        if i < len(levels) - 2:
            nxt = int(levels[i + 1])

        if prev:  # If there's an element to the left in the list
            if curr < prev:
                decreasing = True
                valid_trend = check_trend(increasing, decreasing, "decreasing")
            elif curr > prev:
                increasing = True
                valid_trend = check_trend(increasing, decreasing, "increasing")
            else:
                return False
            if not valid_trend:
                return False
            # Assume trend is valid at this point, so check difference between prev and current
            if not valid_difference(int(prev), int(curr)):
                return False
        if nxt and check_rules_curr_next(curr, nxt, increasing, decreasing) is False:
            return False
    return True


def calculate_safe_reports(reports: list[str]) -> int:
    count = 0
    for report in reports:
        if report_is_safe(report):
            count += 1
    return count


def part_1() -> None:
    reports = read_input()
    safe_report_count = calculate_safe_reports(reports)
    console.print(Panel(f"[bold green]{safe_report_count=} [/]", title="[bold cyan]Day 2 - Part 1[/]", expand=False))


@dataclass
class Level:
    prev: int | None
    curr: int
    next: int | None


def output_level(levels: list[Level], problem_index: int | None = None) -> None:
    panels: list[Panel] = []
    for index, level in enumerate(levels):
        if problem_index and index == problem_index:
            panels.append(Panel(f"[bold red]{level.curr}[/]", title=f"[red]{index}[/]", expand=False))
        else:
            panels.append(Panel(f"[bold cyan]{level.curr}[/]", title=f"{index}", expand=False))
    columns = Columns(panels, equal=True, expand=False)
    console.print(columns)


def output_break() -> None:
    console.print("\n⭐ 🦄 ✨ 🧙 ⭐ 🦄 ✨ 🧙 ⭐ 🦄 ✨ 🧙 ⭐ 🦄 ✨ 🧙\n")


def evaluate_report_safety_part2(levels: list[Level]) -> bool:
    for index, level in enumerate(levels):
        if level.prev is not None and level.prev < level.curr:
            # Increasing from prev -> curr
            if level.next is not None and level.next < level.curr:
                # Increase -> Decrease
                raise ValueError(f"Increase->Decrease: {index + 1}")
            if level.prev == level.curr:
                raise ValueError(f"SameValue: {index}")
        elif level.prev is not None and level.prev > level.curr:
            # Decreasing from prev -> curr
            if level.next is not None and level.next > level.curr:
                # Decrease Increase -> Decrease
                raise ValueError(f"Decrease->Increase: {index}")
        if level.next is not None:
            if level.next == level.curr:
                raise ValueError(f"SameValue: {index + 1}")
            # Perform difference validation
            difference = abs(level.next - level.curr)
            if difference < 1 or difference > 3:
                raise ValueError(f"InvalidDifference: {index}")

    return True


def tokenize_line(report: str) -> list[Level]:
    level_ints = [int(level) for level in report.split(" ")]
    levels: list[Level] = []
    for index, level in enumerate(level_ints):
        prev, next = None, None
        if index > 1:
            prev = level_ints[index - 1]
        if index < len(level_ints) - 2:
            next = level_ints[index + 1]
        levels.append(Level(prev=prev, curr=level, next=next))
    return levels


def calculate_safe_reports_part2(reports: list[str]) -> int:
    count = 0
    for report in reports:
        levels = tokenize_line(report)
        try:
            safe = evaluate_report_safety_part2(levels)
            if safe:
                count += 1
        except ValueError as e:
            problem_index = int(str(e).split(": ")[-1])
            output_level(levels, problem_index=problem_index)
            problem_level = levels[problem_index]
            levels.remove(problem_level)
            output_level(levels)
            safe = False
            try:
                safe = evaluate_report_safety_part2(levels)
                if safe:
                    console.print(":heavy_check_mark: [bold green]Safe after removing problem child![/]👶")
                    count += 1
            except ValueError as e:
                console.print(f":x: [bold red]Dangerous! {e!s}[/]")
                problem_index = int(str(e).split(": ")[-1])
                output_level(levels, problem_index)
            output_break()
    return count


def part_2() -> None:
    reports = read_input()
    safe_report_count = calculate_safe_reports_part2(reports)
    console.print(Panel(f"[bold green]{safe_report_count=} [/]", title="[bold cyan]Day 2 - Part 2[/]", expand=False))


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()
