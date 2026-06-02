#!/usr/bin/env python3
"""
grade_lab02.py

Automated Lab 2 checker for CPSC 250L student forks.

This script clones/updates each student's fork and checks the automatable parts
of Lab 2:

  - repository can be cloned/updated
  - statistics_program.py exists
  - temperatures.txt exists
  - required functions exist
  - read_temperatures() returns a list of floats
  - blank lines are ignored
  - count/min/max/average are correct
  - program runs from the terminal
  - output appears to contain the expected summary information
  - Git history shows at least three commits after a starter commit, if supplied

Expected students.csv format:

name,github_username,repo_url,type
Edward Test,edwardbrash,https://github.com/edwardbrash/cpsc250L.git,test
Alice Smith,asmith,https://github.com/asmith/cpsc250L.git,student

The type column is optional. Use --exclude-test to skip rows marked type=test.

Recommended use with a known Lab 2 starter commit:

python grade_lab02.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab02_report.csv \
  --starter-commit LAB2_STARTER_COMMIT_HASH

If you do not know the starter commit, omit --starter-commit. The script will
fall back to checking whether at least three recent commits exist in the repo,
but this is less precise.
"""

from __future__ import annotations

import argparse
import ast
import csv
import importlib.util
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXPECTED_VALUES = [
    72.4, 75.1, 73.8, 70.2, 68.9,
    71.5, 74.0, 76.3, 79.1, 82.4,
    85.0, 88.1, 86.7, 83.2, 80.5,
    77.6, 74.8, 70.9, 66.4, 61.2,
]

EXPECTED_COUNT = len(EXPECTED_VALUES)
EXPECTED_MIN = min(EXPECTED_VALUES)
EXPECTED_MAX = max(EXPECTED_VALUES)
EXPECTED_AVG = sum(EXPECTED_VALUES) / len(EXPECTED_VALUES)

REQUIRED_FUNCTIONS = [
    "read_temperatures",
    "compute_average",
    "compute_minimum",
    "compute_maximum",
    "print_summary",
    "main",
]


def run_command(
    command: List[str],
    cwd: Optional[Path] = None,
    timeout: int = 20,
) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            capture_output=True,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", f"Command timed out after {timeout} seconds: {' '.join(command)}"
    except Exception as exc:
        return 1, "", f"Command failed: {exc}"


def clone_or_update_repo(repo_url: str, repo_dir: Path) -> Tuple[bool, str]:
    if not repo_dir.exists():
        code, out, err = run_command(["git", "clone", repo_url, str(repo_dir)], timeout=60)
        if code != 0:
            return False, err or out
        return True, "cloned"

    if not (repo_dir / ".git").exists():
        return False, f"{repo_dir} exists but is not a git repository"

    run_command(["git", "fetch", "--all"], cwd=repo_dir, timeout=60)

    code, out, err = run_command(["git", "checkout", "main"], cwd=repo_dir)
    if code != 0:
        run_command(["git", "checkout", "master"], cwd=repo_dir)

    code, out, err = run_command(["git", "pull"], cwd=repo_dir, timeout=60)
    if code != 0:
        return False, err or out

    return True, "updated"


def find_file(repo_dir: Path, filename: str) -> Optional[Path]:
    candidates = list(repo_dir.rglob(filename))
    filtered = [
        p for p in candidates
        if ".git" not in p.parts
        and ".venv" not in p.parts
        and "venv" not in p.parts
        and "__pycache__" not in p.parts
    ]

    if not filtered:
        return None

    # Prefer lab02/lab2/data-relevant paths.
    filtered.sort(
        key=lambda p: (
            "lab02" not in str(p).lower() and "lab2" not in str(p).lower(),
            len(p.parts),
        )
    )
    return filtered[0]


def parse_function_names(py_path: Path) -> Tuple[bool, List[str], str]:
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, [], str(exc)

    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    return True, functions, ""


def count_todo_comments(py_path: Path) -> int:
    try:
        text = py_path.read_text(encoding="utf-8")
    except Exception:
        return 0
    return text.count("TODO")


def import_student_module(py_path: Path) -> Tuple[Optional[Any], str]:
    try:
        module_name = f"student_statistics_program_{abs(hash(str(py_path)))}"
        spec = importlib.util.spec_from_file_location(module_name, py_path)
        if spec is None or spec.loader is None:
            return None, "Could not create import spec."

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, "ok"
    except Exception as exc:
        return None, f"Import failed: {exc}"


def write_temp_data_file() -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="lab02_grader_"))
    data_path = temp_dir / "temperatures_with_blank_lines.txt"

    lines = [
        "72.4",
        "",
        "75.1",
        "  ",
        "73.8",
        "70.2",
        "68.9",
        "71.5",
        "74.0",
        "76.3",
        "79.1",
        "82.4",
        "85.0",
        "88.1",
        "86.7",
        "83.2",
        "80.5",
        "77.6",
        "74.8",
        "70.9",
        "66.4",
        "61.2",
        "",
    ]
    data_path.write_text("\n".join(lines), encoding="utf-8")
    return data_path


def close_enough(actual: float, expected: float, tol: float = 1e-6) -> bool:
    try:
        return math.isclose(float(actual), float(expected), rel_tol=tol, abs_tol=tol)
    except Exception:
        return False


def test_student_functions(module: Any) -> Dict[str, str]:
    result = {
        "read_returns_list": "no",
        "read_values_correct": "no",
        "blank_lines_ignored": "no",
        "count_correct": "no",
        "minimum_correct": "no",
        "maximum_correct": "no",
        "average_correct": "no",
        "function_test_notes": "",
    }

    temp_data = write_temp_data_file()

    try:
        values = module.read_temperatures(temp_data)
    except Exception as exc:
        result["function_test_notes"] += f"read_temperatures raised: {exc}. "
        return result

    if isinstance(values, list):
        result["read_returns_list"] = "yes"
    else:
        result["function_test_notes"] += f"read_temperatures returned {type(values).__name__}, not list. "
        return result

    try:
        numeric_values = [float(x) for x in values]
    except Exception as exc:
        result["function_test_notes"] += f"Returned list contains non-numeric values: {exc}. "
        return result

    if len(numeric_values) == EXPECTED_COUNT:
        result["blank_lines_ignored"] = "yes"
        result["count_correct"] = "yes"
    else:
        result["function_test_notes"] += f"Expected {EXPECTED_COUNT} readings, got {len(numeric_values)}. "

    if len(numeric_values) == EXPECTED_COUNT and all(
        close_enough(a, b) for a, b in zip(numeric_values, EXPECTED_VALUES)
    ):
        result["read_values_correct"] = "yes"

    try:
        minimum = module.compute_minimum(numeric_values)
        if close_enough(minimum, EXPECTED_MIN):
            result["minimum_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Minimum expected {EXPECTED_MIN}, got {minimum}. "
    except Exception as exc:
        result["function_test_notes"] += f"compute_minimum raised: {exc}. "

    try:
        maximum = module.compute_maximum(numeric_values)
        if close_enough(maximum, EXPECTED_MAX):
            result["maximum_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Maximum expected {EXPECTED_MAX}, got {maximum}. "
    except Exception as exc:
        result["function_test_notes"] += f"compute_maximum raised: {exc}. "

    try:
        average = module.compute_average(numeric_values)
        if close_enough(average, EXPECTED_AVG):
            result["average_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Average expected {EXPECTED_AVG:.6f}, got {average}. "
    except Exception as exc:
        result["function_test_notes"] += f"compute_average raised: {exc}. "

    return result


def run_program_from_terminal(py_path: Path) -> Tuple[bool, str]:
    code, out, err = run_command(
        [sys.executable, str(py_path.name)],
        cwd=py_path.parent,
        timeout=10,
    )
    if code == 0:
        return True, out
    return False, err or out


def output_has_expected_content(output: str) -> Tuple[bool, str]:
    lowered = output.lower()
    notes = []

    expected_tokens = [
        ("count/number of readings", ["number", "readings"]),
        ("minimum", ["minimum"]),
        ("maximum", ["maximum"]),
        ("average", ["average"]),
    ]

    for label, tokens in expected_tokens:
        if not all(token in lowered for token in tokens):
            notes.append(f"Missing label clue: {label}")

    numeric_clues = ["20", "61.2", "88.1"]
    for clue in numeric_clues:
        if clue not in output:
            notes.append(f"Missing numeric clue: {clue}")

    # Average may be formatted differently, so accept several representations.
    average_ok = any(clue in output for clue in ["76.42", "76.4", "76.415"])
    if not average_ok:
        notes.append("Missing average clue near 76.42")

    return len(notes) == 0, "; ".join(notes)


def count_commits_since_starter(repo_dir: Path, starter_commit: Optional[str]) -> Tuple[Optional[int], str]:
    if not starter_commit:
        return None, "starter commit not provided"

    code, out, err = run_command(
        ["git", "rev-list", "--count", f"{starter_commit}..HEAD"],
        cwd=repo_dir,
    )

    if code != 0:
        return None, err or out

    try:
        return int(out), "ok"
    except ValueError:
        return None, f"could not parse commit count: {out}"


def get_recent_commit_count(repo_dir: Path) -> Tuple[Optional[int], str]:
    code, out, err = run_command(["git", "rev-list", "--count", "HEAD"], cwd=repo_dir)
    if code != 0:
        return None, err or out

    try:
        return int(out), "ok"
    except ValueError:
        return None, f"could not parse commit count: {out}"


def get_recent_commits(repo_dir: Path, n: int = 8) -> str:
    code, out, err = run_command(["git", "log", "--oneline", f"-{n}"], cwd=repo_dir)
    return out if code == 0 else err


def is_working_tree_clean(repo_dir: Path) -> Tuple[bool, str]:
    code, out, err = run_command(["git", "status", "--porcelain"], cwd=repo_dir)
    if code != 0:
        return False, err or out

    if out.strip() == "":
        return True, "clean"

    return False, out.replace("\n", " | ")


def grade_student(row: Dict[str, str], workdir: Path, starter_commit: Optional[str]) -> Dict[str, str]:
    name = row["name"].strip()
    username = row["github_username"].strip()
    repo_url = row["repo_url"].strip()

    repo_dir = workdir / username

    result: Dict[str, str] = {
        "name": name,
        "github_username": username,
        "repo_url": repo_url,
        "type": row.get("type", "student").strip() or "student",
        "clone_or_update": "no",
        "statistics_program_exists": "no",
        "statistics_program_path": "",
        "temperatures_txt_exists": "no",
        "temperatures_txt_path": "",
        "required_functions_present": "no",
        "missing_functions": "",
        "todo_count": "",
        "read_returns_list": "no",
        "read_values_correct": "no",
        "blank_lines_ignored": "no",
        "count_correct": "no",
        "minimum_correct": "no",
        "maximum_correct": "no",
        "average_correct": "no",
        "terminal_run_success": "no",
        "output_readable_and_formatted": "no",
        "program_output": "",
        "commits_after_starter": "",
        "at_least_three_commits": "no",
        "commit_check_method": "",
        "working_tree_clean": "no",
        "recent_commits": "",
        "auto_score_out_of_14": "0",
        "manual_live_explanation_out_of_3": "",
        "manual_live_modification_out_of_3": "",
        "total_score_out_of_20": "",
        "notes": "",
    }

    ok, message = clone_or_update_repo(repo_url, repo_dir)
    result["clone_or_update"] = "yes" if ok else "no"
    if not ok:
        result["notes"] = message
        return result

    score = 1

    py_path = find_file(repo_dir, "statistics_program.py")
    data_path = find_file(repo_dir, "temperatures.txt")

    if py_path:
        result["statistics_program_exists"] = "yes"
        result["statistics_program_path"] = str(py_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "statistics_program.py not found. "

    if data_path:
        result["temperatures_txt_exists"] = "yes"
        result["temperatures_txt_path"] = str(data_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "temperatures.txt not found. "

    if not py_path:
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
        return result

    parsed_ok, functions, parse_note = parse_function_names(py_path)
    if parsed_ok:
        missing = [fn for fn in REQUIRED_FUNCTIONS if fn not in functions]
        result["missing_functions"] = ", ".join(missing)
        if not missing:
            result["required_functions_present"] = "yes"
            score += 1
    else:
        result["notes"] += f"Could not parse Python file: {parse_note}. "

    result["todo_count"] = str(count_todo_comments(py_path))

    module, import_note = import_student_module(py_path)
    if module is not None:
        test_results = test_student_functions(module)
        for key, value in test_results.items():
            if key in result:
                result[key] = value
        result["notes"] += test_results.get("function_test_notes", "")

        for key in [
            "read_returns_list",
            "read_values_correct",
            "blank_lines_ignored",
            "count_correct",
            "minimum_correct",
            "maximum_correct",
            "average_correct",
        ]:
            if result[key] == "yes":
                score += 1
    else:
        result["notes"] += import_note + " "

    terminal_ok, output = run_program_from_terminal(py_path)
    result["terminal_run_success"] = "yes" if terminal_ok else "no"
    result["program_output"] = output[:700]
    if terminal_ok:
        score += 1
        readable, readable_note = output_has_expected_content(output)
        if readable:
            result["output_readable_and_formatted"] = "yes"
            score += 1
        else:
            result["notes"] += f"Output check: {readable_note}. "

    commits_after, commit_note = count_commits_since_starter(repo_dir, starter_commit)
    if starter_commit:
        result["commit_check_method"] = f"commits after starter commit {starter_commit}"
        if commits_after is not None:
            result["commits_after_starter"] = str(commits_after)
            if commits_after >= 3:
                result["at_least_three_commits"] = "yes"
                score += 1
            else:
                result["notes"] += f"Expected at least 3 commits after starter commit, got {commits_after}. "
        else:
            result["notes"] += f"Commit check failed: {commit_note}. "
    else:
        result["commit_check_method"] = "fallback: total commits in repo"
        total_commits, total_note = get_recent_commit_count(repo_dir)
        if total_commits is not None:
            result["commits_after_starter"] = ""
            if total_commits >= 3:
                result["at_least_three_commits"] = "yes"
                score += 1
            else:
                result["notes"] += f"Starter commit not provided; total repo commits is only {total_commits}. "
        else:
            result["notes"] += f"Starter commit not provided; total commit fallback failed: {total_note}. "

    clean, clean_note = is_working_tree_clean(repo_dir)
    result["working_tree_clean"] = "yes" if clean else "no"
    if clean:
        score += 1
    else:
        result["notes"] += f"Working tree: {clean_note}. "

    result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
    result["auto_score_out_of_14"] = str(score)
    return result


def read_students(path: Path, exclude_test: bool = False) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"name", "github_username", "repo_url"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"students.csv is missing required columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    if exclude_test:
        rows = [row for row in rows if row.get("type", "student").strip().lower() != "test"]

    return rows


def write_report(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "name",
        "github_username",
        "repo_url",
        "type",
        "clone_or_update",
        "statistics_program_exists",
        "statistics_program_path",
        "temperatures_txt_exists",
        "temperatures_txt_path",
        "required_functions_present",
        "missing_functions",
        "todo_count",
        "read_returns_list",
        "read_values_correct",
        "blank_lines_ignored",
        "count_correct",
        "minimum_correct",
        "maximum_correct",
        "average_correct",
        "terminal_run_success",
        "output_readable_and_formatted",
        "program_output",
        "commits_after_starter",
        "at_least_three_commits",
        "commit_check_method",
        "working_tree_clean",
        "recent_commits",
        "auto_score_out_of_14",
        "manual_live_explanation_out_of_3",
        "manual_live_modification_out_of_3",
        "total_score_out_of_20",
        "notes",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade CPSC 250L Lab 2 student forks.")
    parser.add_argument("--students", required=True, help="Path to students.csv")
    parser.add_argument("--workdir", default="student_repos", help="Folder where repos are cloned")
    parser.add_argument("--report", default="reports/lab02_report.csv", help="Output CSV report path")
    parser.add_argument(
        "--starter-commit",
        default=None,
        help="Optional Lab 2 starter commit hash from the instructor repo",
    )
    parser.add_argument(
        "--exclude-test",
        action="store_true",
        help="Skip rows in students.csv where type is test",
    )
    args = parser.parse_args()

    students_path = Path(args.students)
    workdir = Path(args.workdir)
    report_path = Path(args.report)

    workdir.mkdir(parents=True, exist_ok=True)

    students = read_students(students_path, exclude_test=args.exclude_test)
    results = []

    for student in students:
        print(f"Grading {student['name']}...")
        results.append(grade_student(student, workdir, args.starter_commit))

    write_report(report_path, results)
    print(f"\nWrote report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
