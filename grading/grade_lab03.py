#!/usr/bin/env python3
"""
grade_lab03.py

Automated Lab 3 checker for CPSC 250L student forks.

This grader is designed for Lab 3's temperature report program.

It checks the automatable parts of the Lab 3 checkoff:

  - repository can be cloned/updated
  - temperature_report.py exists
  - june_temperatures.txt exists somewhere in the repo
  - program uses functions
  - expected functions are present
  - program reads data from a file
  - statistics are computed correctly
  - output is formatted/readable
  - program runs from the terminal
  - code has at least some comments/docstrings
  - Git history shows meaningful commits
  - working tree is clean

Expected students.csv format:

name,github_username,repo_url,type
Edward Test,edwardbrash,https://github.com/edwardbrash/cpsc250L.git,test
Alice Smith,asmith,https://github.com/asmith/cpsc250L.git,student

The type column is optional. Use --exclude-test to skip rows marked type=test.

Recommended use:

python grade_lab03.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab03_report.csv

With known Lab 3 starter commit:

python grade_lab03.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab03_report.csv \
  --starter-commit LAB3_STARTER_COMMIT_HASH
"""

from __future__ import annotations

import argparse
import ast
import csv
import math
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


TEST_VALUES = [18.5, 22.0, 31.2, 29.8, 35.0, 30.0, 27.5, 33.3]
EXPECTED_AVG = sum(TEST_VALUES) / len(TEST_VALUES)
EXPECTED_MIN = min(TEST_VALUES)
EXPECTED_MAX = max(TEST_VALUES)
EXPECTED_ABOVE_30 = sum(1 for value in TEST_VALUES if value > 30)

EXPECTED_FUNCTIONS = [
    "read_temperatures",
    "calculate_average",
    "find_maximum",
    "find_minimum",
    "count_above_threshold",
    "print_report",
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

    filtered.sort(
        key=lambda p: (
            "lab03" not in str(p).lower() and "lab3" not in str(p).lower(),
            len(p.parts),
        )
    )
    return filtered[0]


def find_june_temperatures(repo_dir: Path) -> Optional[Path]:
    # Prefer the expected filename, but allow fallback to any file that looks like data.
    exact = find_file(repo_dir, "june_temperatures.txt")
    if exact:
        return exact

    candidates = list(repo_dir.rglob("*temperature*.txt")) + list(repo_dir.rglob("*temperatures*.txt"))
    filtered = [
        p for p in candidates
        if ".git" not in p.parts
        and ".venv" not in p.parts
        and "venv" not in p.parts
        and "__pycache__" not in p.parts
    ]
    if not filtered:
        return None

    filtered.sort(key=lambda p: (len(p.parts), str(p)))
    return filtered[0]


def parse_python(py_path: Path) -> Tuple[Optional[ast.Module], str]:
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
        return tree, "ok"
    except Exception as exc:
        return None, str(exc)


def get_function_names(tree: ast.Module) -> List[str]:
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def has_comments_or_docstrings(py_path: Path, tree: ast.Module) -> Tuple[bool, str]:
    text = py_path.read_text(encoding="utf-8")
    comment_lines = [
        line for line in text.splitlines()
        if line.strip().startswith("#")
    ]

    module_docstring = ast.get_docstring(tree)
    function_docstrings = [
        ast.get_docstring(node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and ast.get_docstring(node)
    ]

    if module_docstring or function_docstrings or len(comment_lines) >= 2:
        return True, "comments/docstrings found"

    return False, "few or no comments/docstrings found"


def function_call_count(tree: ast.Module) -> int:
    return sum(isinstance(node, ast.FunctionDef) for node in tree.body)


def load_functions_without_running_main(py_path: Path) -> Tuple[Optional[Any], str]:
    """
    Load imports and function definitions from a student file without executing top-level main().

    This matters because the sample correct solution calls main() directly at the bottom
    instead of using if __name__ == "__main__": main().
    """
    tree, parse_note = parse_python(py_path)
    if tree is None:
        return None, f"Parse failed: {parse_note}"

    allowed_nodes = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef)):
            allowed_nodes.append(node)

    safe_tree = ast.Module(body=allowed_nodes, type_ignores=[])
    ast.fix_missing_locations(safe_tree)

    module = types.ModuleType("student_temperature_report")
    module.__file__ = str(py_path)

    try:
        code = compile(safe_tree, filename=str(py_path), mode="exec")
        exec(code, module.__dict__)
        return module, "ok"
    except Exception as exc:
        return None, f"Function-only load failed: {exc}"


def make_test_data_file() -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="lab03_grader_"))
    data_path = temp_dir / "june_temperatures.txt"

    lines = [
        "18.5",
        "22.0",
        "not_a_number",
        "31.2",
        "",
        "29.8",
        "35.0",
        "30.0",
        "27.5",
        "33.3",
    ]

    data_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return data_path


def close_enough(actual: float, expected: float, tol: float = 1e-6) -> bool:
    try:
        return math.isclose(float(actual), float(expected), rel_tol=tol, abs_tol=tol)
    except Exception:
        return False


def test_student_functions(module: Any) -> Dict[str, str]:
    result = {
        "read_data_correct": "no",
        "average_correct": "no",
        "minimum_correct": "no",
        "maximum_correct": "no",
        "threshold_count_correct": "no",
        "function_test_notes": "",
    }

    data_path = make_test_data_file()

    try:
        values = module.read_temperatures(data_path)
    except Exception as exc:
        result["function_test_notes"] += f"read_temperatures raised: {exc}. "
        return result

    try:
        numeric_values = [float(x) for x in values]
    except Exception as exc:
        result["function_test_notes"] += f"read_temperatures returned non-numeric data: {exc}. "
        return result

    if len(numeric_values) == len(TEST_VALUES) and all(
        close_enough(a, b) for a, b in zip(numeric_values, TEST_VALUES)
    ):
        result["read_data_correct"] = "yes"
    else:
        result["function_test_notes"] += (
            f"Expected read_temperatures to return {TEST_VALUES}, got {numeric_values}. "
        )

    try:
        avg = module.calculate_average(TEST_VALUES)
        if close_enough(avg, EXPECTED_AVG):
            result["average_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Average expected {EXPECTED_AVG:.6f}, got {avg}. "
    except Exception as exc:
        result["function_test_notes"] += f"calculate_average raised: {exc}. "

    try:
        minimum = module.find_minimum(TEST_VALUES)
        if close_enough(minimum, EXPECTED_MIN):
            result["minimum_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Minimum expected {EXPECTED_MIN}, got {minimum}. "
    except Exception as exc:
        result["function_test_notes"] += f"find_minimum raised: {exc}. "

    try:
        maximum = module.find_maximum(TEST_VALUES)
        if close_enough(maximum, EXPECTED_MAX):
            result["maximum_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Maximum expected {EXPECTED_MAX}, got {maximum}. "
    except Exception as exc:
        result["function_test_notes"] += f"find_maximum raised: {exc}. "

    try:
        count = module.count_above_threshold(TEST_VALUES, 30)
        if count == EXPECTED_ABOVE_30:
            result["threshold_count_correct"] = "yes"
        else:
            result["function_test_notes"] += f"Count above 30 expected {EXPECTED_ABOVE_30}, got {count}. "
    except Exception as exc:
        result["function_test_notes"] += f"count_above_threshold raised: {exc}. "

    return result


def run_program_from_terminal(py_path: Path) -> Tuple[bool, str]:
    """
    Run the program from the folder containing temperature_report.py.

    This matches the likely PyCharm/terminal use case and supports solutions that
    read '../data/june_temperatures.txt' relative to the lab folder.
    """
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

    # Flexible label clues. We do not require exact wording.
    label_clues = [
        ("average", ["average"]),
        ("maximum", ["maximum", "max"]),
        ("minimum", ["minimum", "min"]),
        ("above threshold", ["above"]),
    ]

    for label, alternatives in label_clues:
        if not any(word in lowered for word in alternatives):
            notes.append(f"Missing output clue: {label}")

    # A readable report should have at least three non-empty lines.
    nonempty_lines = [line for line in output.splitlines() if line.strip()]
    if len(nonempty_lines) < 3:
        notes.append("Output has fewer than three non-empty lines")

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
        "temperature_report_exists": "no",
        "temperature_report_path": "",
        "june_temperatures_exists": "no",
        "june_temperatures_path": "",
        "uses_functions": "no",
        "required_functions_present": "no",
        "missing_functions": "",
        "commented_appropriately": "no",
        "comment_notes": "",
        "read_data_correct": "no",
        "average_correct": "no",
        "minimum_correct": "no",
        "maximum_correct": "no",
        "threshold_count_correct": "no",
        "terminal_run_success": "no",
        "output_readable_and_formatted": "no",
        "program_output": "",
        "commits_after_starter": "",
        "meaningful_commit_evidence": "no",
        "commit_check_method": "",
        "working_tree_clean": "no",
        "recent_commits": "",
        "auto_score_out_of_14": "0",
        "manual_pyCharm_run_out_of_2": "",
        "manual_review_out_of_4": "",
        "total_score_out_of_20": "",
        "notes": "",
    }

    ok, message = clone_or_update_repo(repo_url, repo_dir)
    result["clone_or_update"] = "yes" if ok else "no"
    if not ok:
        result["notes"] = message
        return result

    score = 1

    py_path = find_file(repo_dir, "temperature_report.py")
    data_path = find_june_temperatures(repo_dir)

    if py_path:
        result["temperature_report_exists"] = "yes"
        result["temperature_report_path"] = str(py_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "temperature_report.py not found. "

    if data_path:
        result["june_temperatures_exists"] = "yes"
        result["june_temperatures_path"] = str(data_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "june_temperatures.txt or similar data file not found. "

    if not py_path:
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
        return result

    tree, parse_note = parse_python(py_path)
    if tree is None:
        result["notes"] += f"Could not parse Python file: {parse_note}. "
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:700]
        return result

    functions = get_function_names(tree)
    if len(functions) >= 3:
        result["uses_functions"] = "yes"
        score += 1

    missing = [fn for fn in EXPECTED_FUNCTIONS if fn not in functions]
    result["missing_functions"] = ", ".join(missing)
    if not missing:
        result["required_functions_present"] = "yes"
        score += 1

    commented, comment_note = has_comments_or_docstrings(py_path, tree)
    result["commented_appropriately"] = "yes" if commented else "no"
    result["comment_notes"] = comment_note
    if commented:
        score += 1

    module, load_note = load_functions_without_running_main(py_path)
    if module is not None:
        test_results = test_student_functions(module)
        for key, value in test_results.items():
            if key in result:
                result[key] = value
        result["notes"] += test_results.get("function_test_notes", "")

        for key in [
            "read_data_correct",
            "average_correct",
            "minimum_correct",
            "maximum_correct",
            "threshold_count_correct",
        ]:
            if result[key] == "yes":
                score += 1
    else:
        result["notes"] += load_note + " "

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
    else:
        result["notes"] += "Terminal run failed. "

    commits_after, commit_note = count_commits_since_starter(repo_dir, starter_commit)
    if starter_commit:
        result["commit_check_method"] = f"commits after starter commit {starter_commit}"
        if commits_after is not None:
            result["commits_after_starter"] = str(commits_after)
            if commits_after >= 2:
                result["meaningful_commit_evidence"] = "yes"
                score += 1
            else:
                result["notes"] += f"Expected at least 2 commits after starter commit, got {commits_after}. "
        else:
            result["notes"] += f"Commit check failed: {commit_note}. "
    else:
        result["commit_check_method"] = "fallback: total commits in repo"
        total_commits, total_note = get_total_commit_count(repo_dir)
        if total_commits is not None:
            if total_commits >= 3:
                result["meaningful_commit_evidence"] = "yes"
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
        "temperature_report_exists",
        "temperature_report_path",
        "june_temperatures_exists",
        "june_temperatures_path",
        "uses_functions",
        "required_functions_present",
        "missing_functions",
        "commented_appropriately",
        "comment_notes",
        "read_data_correct",
        "average_correct",
        "minimum_correct",
        "maximum_correct",
        "threshold_count_correct",
        "terminal_run_success",
        "output_readable_and_formatted",
        "program_output",
        "commits_after_starter",
        "meaningful_commit_evidence",
        "commit_check_method",
        "working_tree_clean",
        "recent_commits",
        "auto_score_out_of_14",
        "manual_pyCharm_run_out_of_2",
        "manual_review_out_of_4",
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
    parser.add_argument(
        "--starter-commit",
        default=None,
        help="Optional Lab 3 starter commit hash from the instructor repo",
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
