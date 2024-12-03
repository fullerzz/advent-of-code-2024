from pathlib import Path
from typing import Literal

from rich.console import Console
from rich.panel import Panel

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


def report_is_safe_part2(report: str) -> bool:  # noqa: C901
    # TODO: This isn't working because an issue with a single level could trigger violation_count to be incremented twice
    levels = report.split(" ")
    violation_count = 0
    increasing, decreasing = False, False
    for i in range(len(levels)):
        curr = int(levels[i])
        prev, nxt = None, None
        if i > 0:
            prev = int(levels[i - 1])
        if i < len(levels) - 2:
            nxt = int(levels[i + 1])
        violation = False
        if prev:  # If there's an element to the left in the list
            valid_trend = True
            if curr < prev:
                decreasing = True
                valid_trend = check_trend(increasing, decreasing, "decreasing")
            elif curr > prev:
                increasing = True
                valid_trend = check_trend(increasing, decreasing, "increasing")

            if not valid_trend:
                violation = True
            if not valid_difference(int(prev), int(curr)):
                violation = True
        if nxt:
            valid_trend = True
            if nxt < curr:
                decreasing = True
                valid_trend = check_trend(increasing, decreasing, "decreasing")
            elif nxt > curr:
                increasing = True
                valid_trend = check_trend(increasing, decreasing, "increasing")

            if not valid_trend:
                violation = True
            if not valid_difference(int(curr), int(nxt)):
                violation = True
        if violation:
            violation_count += 1
        if violation_count > 1:
            return False
    return True


def calculate_safe_reports_part2(reports: list[str]) -> int:
    count = 0
    for report in reports:
        if report_is_safe_part2(report):
            count += 1

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
