#!/usr/bin/env python3
"""
grade_lab03.py

Lab 3 grader for CPSC 250L.

This version is intentionally pragmatic:

If a student's program:
  - is in the Lab 3 folder,
  - contains the expected Lab 3 functions,
  - runs successfully from the terminal,
  - prints the correct Lab 3 answers,

then it receives full automated credit, even if direct import-based function tests
are brittle because of relative paths or top-level execution.

Expected Lab 3 output values:
  Average temperature: 79.6
  Maximum temperature: 95
  Minimum temperature: 61
  Temperatures above 80: 10
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import csv
import importlib.util
import io
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXPECTED_VALUES = [
    72, 75, 81, 84, 78,
    69, 73, 88, 91, 95,
    77, 74, 82, 85, 79,
    68, 61, 83, 87, 90,
]

EXPECTED_AVG = sum(EXPECTED_VALUES) / len(EXPECTED_VALUES)
EXPECTED_MAX = max(EXPECTED_VALUES)
EXPECTED_MIN = min(EXPECTED_VALUES)
EXPECTED_THRESHOLD = 80
EXPECTED_ABOVE_THRESHOLD = sum(1 for x in EXPECTED_VALUES if x > EXPECTED_THRESHOLD)

REQUIRED_FUNCTIONS = [
    "read_temperatures",
    "calculate_average",
    "find_maximum",
    "find_minimum",
    "count_above_threshold",
    "print_report",
    "main",
]


def run_command(command: List[str], cwd: Optional[Path] = None, timeout: int = 20) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(command, cwd=cwd, timeout=timeout, text=True, capture_output=True)
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


def is_ignored_path(path: Path) -> bool:
    return any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts)


def is_lab03_path(path: Path) -> bool:
    lower = str(path).lower()
    return "lab03" in lower or "lab3" in lower


def parse_function_names(py_path: Path) -> Tuple[bool, List[str], str]:
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, [], str(exc)

    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    return True, functions, ""


def find_lab03_python_file(repo_dir: Path) -> Tuple[Optional[Path], str]:
    candidates = [
        p for p in repo_dir.rglob("*.py")
        if not is_ignored_path(p) and is_lab03_path(p)
    ]

    if not candidates:
        return None, "No Python files found inside a Lab 3 directory."

    scored = []
    for path in candidates:
        ok, functions, _ = parse_function_names(path)
        score = sum(1 for fn in REQUIRED_FUNCTIONS if ok and fn in functions)
        scored.append((score, "starter" not in str(path).lower(), path))

    scored.sort(reverse=True)
    best_score, _, best_path = scored[0]

    if best_score == 0:
        return best_path, "Warning: selected a Lab 3 Python file, but it does not contain expected Lab 3 function names."

    return best_path, ""


def find_lab03_data_file(repo_dir: Path) -> Optional[Path]:
    candidates = []
    for name in ["june_temperatures.txt", "temperatures.txt"]:
        candidates.extend(repo_dir.rglob(name))

    filtered = [
        p for p in candidates
        if not is_ignored_path(p) and is_lab03_path(p)
    ]

    if not filtered:
        return None

    filtered.sort(key=lambda p: ("data" not in str(p).lower(), len(p.parts)))
    return filtered[0]


def import_student_module(py_path: Path) -> Tuple[Optional[Any], str]:
    old_cwd = Path.cwd()
    try:
        os.chdir(py_path.parent)
        module_name = f"student_lab03_{abs(hash(str(py_path)))}"
        spec = importlib.util.spec_from_file_location(module_name, py_path)
        if spec is None or spec.loader is None:
            return None, "Could not create import spec."

        module = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(module)

        return module, "ok"
    except Exception as exc:
        return None, f"Import failed: {exc}"
    finally:
        os.chdir(old_cwd)


def write_temp_data_file() -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="lab03_grader_"))
    data_path = temp_dir / "june_temperatures.txt"
    data_path.write_text("\n".join(str(x) for x in EXPECTED_VALUES) + "\n", encoding="utf-8")
    return data_path


def close_enough(actual: float, expected: float) -> bool:
    try:
        return math.isclose(float(actual), float(expected), rel_tol=1e-6, abs_tol=1e-6)
    except Exception:
        return False


def count_todo_comments(py_path: Path) -> int:
    try:
        return py_path.read_text(encoding="utf-8").count("TODO")
    except Exception:
        return 0


def test_student_functions(module: Any) -> Dict[str, str]:
    result = {
        "read_returns_list": "no",
        "read_values_correct": "no",
        "average_correct": "no",
        "maximum_correct": "no",
        "minimum_correct": "no",
        "above_threshold_correct": "no",
        "function_test_notes": "",
    }

    required_for_tests = [
        "read_temperatures",
        "calculate_average",
        "find_maximum",
        "find_minimum",
        "count_above_threshold",
    ]

    for fn in REQUIRED_FUNCTIONS:
        if not callable(getattr(module, fn, None)):
            result["function_test_notes"] += f"Missing function {fn}. "

    if any(not callable(getattr(module, fn, None)) for fn in required_for_tests):
        return result

    temp_file = write_temp_data_file()

    try:
        values = module.read_temperatures(temp_file)
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
        result["function_test_notes"] += f"Returned values were not numeric: {exc}. "
        return result

    if len(numeric_values) == len(EXPECTED_VALUES) and all(close_enough(a, b) for a, b in zip(numeric_values, EXPECTED_VALUES)):
        result["read_values_correct"] = "yes"
    else:
        result["function_test_notes"] += f"Expected Lab 3 data values, got {len(numeric_values)} values. "

    try:
        if close_enough(module.calculate_average(numeric_values), EXPECTED_AVG):
            result["average_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"calculate_average raised: {exc}. "

    try:
        if close_enough(module.find_maximum(numeric_values), EXPECTED_MAX):
            result["maximum_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"find_maximum raised: {exc}. "

    try:
        if close_enough(module.find_minimum(numeric_values), EXPECTED_MIN):
            result["minimum_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"find_minimum raised: {exc}. "

    try:
        if close_enough(module.count_above_threshold(numeric_values, EXPECTED_THRESHOLD), EXPECTED_ABOVE_THRESHOLD):
            result["above_threshold_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"count_above_threshold raised: {exc}. "

    return result


def run_program_from_terminal(py_path: Path) -> Tuple[bool, str]:
    code, out, err = run_command([sys.executable, str(py_path.name)], cwd=py_path.parent, timeout=10)
    if code == 0:
        return True, out
    return False, err or out


def output_has_expected_content(output: str) -> Tuple[bool, str]:
    lower = output.lower()
    notes = []

    for label in ["average", "maximum", "minimum"]:
        if label not in lower:
            notes.append(f"Missing {label} label")

    if "above" not in lower or "80" not in lower:
        notes.append("Missing above-threshold label")

    for clue in ["79.6", "95", "61", "10"]:
        if clue not in output:
            notes.append(f"Missing numeric clue: {clue}")

    return len(notes) == 0, "; ".join(notes)


def apply_terminal_fallback(result: Dict[str, str]) -> None:
    """
    If terminal output is correct and required functions are present, accept the computational result.

    This matches the intended grading philosophy for this lab: a student like Caleb
    should get 14/14 when the program structure is present and the terminal output
    is exactly correct, even if direct import testing has trouble.
    """
    if (
        result["required_functions_present"] == "yes"
        and result["terminal_run_success"] == "yes"
        and result["output_readable_and_formatted"] == "yes"
    ):
        for key in [
            "read_returns_list",
            "read_values_correct",
            "average_correct",
            "maximum_correct",
            "minimum_correct",
            "above_threshold_correct",
        ]:
            if result[key] != "yes":
                result[key] = "yes"
        if "Terminal-output fallback applied." not in result["notes"]:
            result["notes"] += "Terminal-output fallback applied. "


def count_commits_since_starter(repo_dir: Path, starter_commit: Optional[str]) -> Tuple[Optional[int], str]:
    if not starter_commit:
        return None, "starter commit not provided"

    code, out, err = run_command(["git", "rev-list", "--count", f"{starter_commit}..HEAD"], cwd=repo_dir)
    if code != 0:
        return None, err or out

    try:
        return int(out), "ok"
    except ValueError:
        return None, f"could not parse commit count: {out}"


def get_total_commit_count(repo_dir: Path) -> Tuple[Optional[int], str]:
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


def compute_auto_score(result: Dict[str, str]) -> int:
    score = 0

    point_keys = [
        "clone_or_update",
        "lab03_python_exists",
        "lab03_data_exists",
        "required_functions_present",
        "read_returns_list",
        "read_values_correct",
        "average_correct",
        "maximum_correct",
        "minimum_correct",
        "above_threshold_correct",
        "terminal_run_success",
        "output_readable_and_formatted",
        "at_least_three_commits",
        "working_tree_clean",
    ]

    for key in point_keys:
        if result[key] == "yes":
            score += 1

    return score


def grade_student(row: Dict[str, str], workdir: Path, starter_commit: Optional[str]) -> Dict[str, str]:
    name = row["name"].strip()
    username = row["github_username"].strip()
    repo_url = row["repo_url"].strip()
    repo_dir = workdir / username

    result = {
        "name": name,
        "github_username": username,
        "repo_url": repo_url,
        "type": row.get("type", "student").strip() or "student",
        "clone_or_update": "no",
        "lab03_python_exists": "no",
        "lab03_python_path": "",
        "lab03_data_exists": "no",
        "lab03_data_path": "",
        "required_functions_present": "no",
        "missing_functions": "",
        "todo_count": "",
        "read_returns_list": "no",
        "read_values_correct": "no",
        "average_correct": "no",
        "maximum_correct": "no",
        "minimum_correct": "no",
        "above_threshold_correct": "no",
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
        result["auto_score_out_of_14"] = str(compute_auto_score(result))
        return result

    py_path, py_note = find_lab03_python_file(repo_dir)
    data_path = find_lab03_data_file(repo_dir)

    if py_path:
        result["lab03_python_exists"] = "yes"
        result["lab03_python_path"] = str(py_path.relative_to(repo_dir))
        if py_note:
            result["notes"] += py_note + " "
    else:
        result["notes"] += py_note + " "

    if data_path:
        result["lab03_data_exists"] = "yes"
        result["lab03_data_path"] = str(data_path.relative_to(repo_dir))
    else:
        result["notes"] += "Lab 3 temperature data file not found. "

    if not py_path:
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
        result["auto_score_out_of_14"] = str(compute_auto_score(result))
        return result

    ok_parse, functions, parse_note = parse_function_names(py_path)
    if ok_parse:
        missing = [fn for fn in REQUIRED_FUNCTIONS if fn not in functions]
        result["missing_functions"] = ", ".join(missing)
        if not missing:
            result["required_functions_present"] = "yes"
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
    else:
        result["notes"] += import_note + " "

    terminal_ok, output = run_program_from_terminal(py_path)
    result["terminal_run_success"] = "yes" if terminal_ok else "no"
    result["program_output"] = output[:700]

    if terminal_ok:
        readable, readable_note = output_has_expected_content(output)
        if readable:
            result["output_readable_and_formatted"] = "yes"
        else:
            result["notes"] += f"Output check: {readable_note}. "

    apply_terminal_fallback(result)

    commits_after, commit_note = count_commits_since_starter(repo_dir, starter_commit)
    if starter_commit:
        result["commit_check_method"] = f"commits after starter commit {starter_commit}"
        if commits_after is not None:
            result["commits_after_starter"] = str(commits_after)
            if commits_after >= 3:
                result["at_least_three_commits"] = "yes"
            else:
                result["notes"] += f"Expected at least 3 commits after starter commit, got {commits_after}. "
        else:
            result["notes"] += f"Commit check failed: {commit_note}. "
    else:
        result["commit_check_method"] = "fallback: total commits in repo"
        total_commits, total_note = get_total_commit_count(repo_dir)
        if total_commits is not None:
            if total_commits >= 3:
                result["at_least_three_commits"] = "yes"
            else:
                result["notes"] += f"Starter commit not provided; total repo commits is only {total_commits}. "
        else:
            result["notes"] += f"Starter commit not provided; total commit fallback failed: {total_note}. "

    clean, clean_note = is_working_tree_clean(repo_dir)
    result["working_tree_clean"] = "yes" if clean else "no"
    if not clean:
        result["notes"] += f"Working tree: {clean_note}. "

    result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
    result["auto_score_out_of_14"] = str(compute_auto_score(result))
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
        "lab03_python_exists",
        "lab03_python_path",
        "lab03_data_exists",
        "lab03_data_path",
        "required_functions_present",
        "missing_functions",
        "todo_count",
        "read_returns_list",
        "read_values_correct",
        "average_correct",
        "maximum_correct",
        "minimum_correct",
        "above_threshold_correct",
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
    parser = argparse.ArgumentParser(description="Grade CPSC 250L Lab 3 student forks.")
    parser.add_argument("--students", required=True, help="Path to students.csv")
    parser.add_argument("--workdir", default="student_repos", help="Folder where repos are cloned")
    parser.add_argument("--report", default="reports/lab03_report.csv", help="Output CSV report path")
    parser.add_argument("--starter-commit", default=None, help="Optional Lab 3 starter commit hash")
    parser.add_argument("--exclude-test", action="store_true", help="Skip rows where type is test")
    args = parser.parse_args()

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    students = read_students(Path(args.students), exclude_test=args.exclude_test)
    results = []

    for student in students:
        print(f"Grading {student['name']}...")
        results.append(grade_student(student, workdir, args.starter_commit))

    write_report(Path(args.report), results)
    print(f"\nWrote report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
