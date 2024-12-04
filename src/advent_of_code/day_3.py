import contextlib
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, computed_field
from rich.console import Console
from rich.panel import Panel

console = Console()


class Mul(BaseModel):
    raw_left: str = Field(min_length=1, max_length=3)
    raw_right: str = Field(min_length=1, max_length=3)

    @computed_field  # type: ignore
    @property
    def product(self) -> int:
        return int(self.raw_left) * int(self.raw_right)


def read_input() -> str:
    input_path = Path("input") / "day3.txt"
    console.print("[bold cyan]Reading input file: [/bold cyan]" + str(input_path))
    with input_path.open() as f:
        return f.read()


def extract_left(substr: str) -> str:
    text = substr.replace("mul(", "", 1)
    parts = text.split(",")
    if len(parts) == 1:
        return ""
    return parts[0]


def extract_right(substr: str) -> str:
    text = substr.replace("mul(", "", 1)
    parts = text.split(",", 1)
    if len(parts) == 1:
        return ""
    possible_num = parts[1].strip()
    closing_parentheses = possible_num.find(")")
    if closing_parentheses == -1:
        return ""
    return possible_num[0:closing_parentheses]


def extract_instructions(text: str, validate: bool = False) -> list[Mul]:
    index = text.find("mul(")
    muls = []
    do_index = 0
    dont_index = -1
    while index != -1:
        left = extract_left(text[index : index + 12])
        right = extract_right(text[index : index + 12])
        with contextlib.suppress(ValidationError):
            mul = Mul(raw_left=left, raw_right=right)
            if validate:
                do_index = extract_next_do(text, do_index, index)
                dont_index = extract_next_dont(text, dont_index, index)
                validate_instruction(index, text, do_index, dont_index)
            muls.append(mul)
        index = text.find("mul(", index + 4)
    return muls


def part_1(text: str) -> None:
    instructions = extract_instructions(text)
    total = sum(mul.product for mul in instructions)
    console.print(Panel(f"[bold green]{total=} [/]", title="[bold cyan]Day 3 - Part 1[/]", expand=False))


def extract_next_do(text: str, curr: int, instruction_index: int) -> int:
    return text.find("do()", curr + 1, instruction_index)


def extract_next_dont(text: str, curr: int, instruction_index: int) -> int:
    if curr == -1:
        return text.find("dont()")
    return text.find("dont()", curr + 1, instruction_index)


def validate_instruction(instruction_index: int, text: str, do_index: int, dont_index: int) -> bool:
    return do_index >= dont_index


def part_2(text: str) -> None:
    instructions = extract_instructions(text, validate=True)
    total = sum(mul.product for mul in instructions)
    console.print(Panel(f"[bold green]{total=} [/]", title="[bold cyan]Day 3 - Part 2[/]", expand=False))


def main() -> None:
    text = read_input()
    part_1(text)
    part_2(text)


if __name__ == "__main__":
    main()
