#!/usr/bin/env python3
"""
grade_lab04.py

Automated Lab 4 checker for CPSC 250L student forks.

This grader checks the automatable parts of Lab 4:

  - repository can be cloned/updated
  - student_scores.py exists
  - quiz_scores.csv exists
  - program reads a CSV file
  - header row is skipped
  - student names are stored correctly
  - valid scores are converted to numbers
  - missing/invalid scores are handled
  - student averages are correct
  - letter grades are correct
  - student report output is clear
  - class summary output is clear
  - at least four commits are present, preferably after a starter commit
  - working tree is clean

Expected students.csv format:

name,github_username,repo_url,type
Edward Test,edwardbrash,https://github.com/edwardbrash/cpsc250L.git,test
Alice Smith,asmith,https://github.com/asmith/cpsc250L.git,student

The type column is optional. Use --exclude-test to skip rows marked type=test.

Recommended use:

python grade_lab04.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab04_report.csv

With known Lab 4 starter commit:

python grade_lab04.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab04_report.csv \
  --starter-commit LAB4_STARTER_COMMIT_HASH
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


EXPECTED_RECORDS = [
    {"name": "Alice Johnson", "scores": [85, 90, 88], "average": 87.6666666667, "grade": "A"},
    {"name": "Ben Carter", "scores": [72, 78, 80], "average": 76.6666666667, "grade": "C"},
    {"name": "Carlos Rivera", "scores": [91, 95, 94], "average": 93.3333333333, "grade": "A"},
    {"name": "Dana Lee", "scores": [88, None, 92], "average": 90.0, "grade": "A"},
    {"name": "Eli Morgan", "scores": [70, None, 75], "average": 72.5, "grade": "C"},
    {"name": "Fatima Ahmed", "scores": [84, 82, 86], "average": 84.0, "grade": "B"},
    {"name": "Grace Kim", "scores": [None, 89, 91], "average": 90.0, "grade": "A"},
    {"name": "Henry Smith", "scores": [65, 70, 60], "average": 65.0, "grade": "D"},
    {"name": "Isabella Brown", "scores": [92, 88, 90], "average": 90.0, "grade": "A"},
    {"name": "Jackson Davis", "scores": [55, None, None], "average": 55.0, "grade": "F"},
]

EXPECTED_NAMES = [record["name"] for record in EXPECTED_RECORDS]
EXPECTED_AVERAGES = [record["average"] for record in EXPECTED_RECORDS]
EXPECTED_GRADES = [record["grade"] for record in EXPECTED_RECORDS]
EXPECTED_CLASS_AVERAGE = sum(EXPECTED_AVERAGES) / len(EXPECTED_AVERAGES)
EXPECTED_HIGHEST = max(EXPECTED_AVERAGES)
EXPECTED_LOWEST = min(EXPECTED_AVERAGES)

EXPECTED_FUNCTIONS = [
    "clean_score",
    "calculate_average",
    "read_scores",
    "letter_grade",
    "print_student_report",
    "print_class_summary",
    "main",
]

CSV_TEXT = """name,quiz1,quiz2,quiz3
Alice Johnson,85,90,88
Ben Carter,72,78,80
Carlos Rivera,91,95,94
Dana Lee,88,,92
Eli Morgan,70,invalid,75
Fatima Ahmed,84,82,86
Grace Kim,absent,89,91
Henry Smith,65,70,60
Isabella Brown, 92 , 88 , 90
Jackson Davis,55,,invalid
"""


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
            "lab04" not in str(p).lower() and "lab4" not in str(p).lower(),
            len(p.parts),
        )
    )
    return filtered[0]


def parse_python(py_path: Path) -> Tuple[Optional[ast.Module], str]:
    try:
        return ast.parse(py_path.read_text(encoding="utf-8")), "ok"
    except Exception as exc:
        return None, str(exc)


def get_function_names(tree: ast.Module) -> List[str]:
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def load_functions_without_running_main(py_path: Path) -> Tuple[Optional[Any], str]:
    """
    Load imports and function definitions without running top-level main().

    The sample correct solution calls main() directly at the bottom, so a normal import
    would immediately try to run the program.
    """
    tree, parse_note = parse_python(py_path)
    if tree is None:
        return None, f"Parse failed: {parse_note}"

    allowed_nodes = [
        node for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]

    safe_tree = ast.Module(body=allowed_nodes, type_ignores=[])
    ast.fix_missing_locations(safe_tree)

    module = types.ModuleType("student_student_scores")
    module.__file__ = str(py_path)

    try:
        code = compile(safe_tree, filename=str(py_path), mode="exec")
        exec(code, module.__dict__)
        return module, "ok"
    except Exception as exc:
        return None, f"Function-only load failed: {exc}"


def make_test_csv() -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="lab04_grader_"))
    path = temp_dir / "quiz_scores.csv"
    path.write_text(CSV_TEXT, encoding="utf-8")
    return path


def close_enough(actual: float, expected: float, tol: float = 1e-6) -> bool:
    try:
        return math.isclose(float(actual), float(expected), rel_tol=tol, abs_tol=tol)
    except Exception:
        return False


def normalize_score_list(scores: Any) -> List[Optional[int]]:
    normalized = []
    for score in scores:
        if score is None:
            normalized.append(None)
        else:
            normalized.append(int(score))
    return normalized


def test_student_functions(module: Any) -> Dict[str, str]:
    result = {
        "clean_score_correct": "no",
        "read_csv_correct": "no",
        "header_skipped": "no",
        "names_stored_correctly": "no",
        "scores_converted_correctly": "no",
        "missing_invalid_handled": "no",
        "averages_correct": "no",
        "letter_grades_correct": "no",
        "class_summary_values_correct": "no",
        "function_test_notes": "",
    }

    # clean_score tests
    try:
        clean_cases = {
            "85": 85,
            " 92 ": 92,
            "": None,
            "   ": None,
            "invalid": None,
            "absent": None,
        }
        clean_ok = True
        for raw, expected in clean_cases.items():
            actual = module.clean_score(raw)
            if actual != expected:
                clean_ok = False
                result["function_test_notes"] += f"clean_score({raw!r}) expected {expected}, got {actual}. "
        if clean_ok:
            result["clean_score_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"clean_score raised: {exc}. "

    # average tests
    try:
        if (
            close_enough(module.calculate_average([85, 90, 88]), 87.6666666667)
            and close_enough(module.calculate_average([88, None, 92]), 90.0)
            and module.calculate_average([None, None]) is None
        ):
            average_helper_ok = True
        else:
            average_helper_ok = False
            result["function_test_notes"] += "calculate_average helper failed one or more cases. "
    except Exception as exc:
        average_helper_ok = False
        result["function_test_notes"] += f"calculate_average raised: {exc}. "

    csv_path = make_test_csv()
    try:
        records = module.read_scores(csv_path)
    except Exception as exc:
        result["function_test_notes"] += f"read_scores raised: {exc}. "
        return result

    if not isinstance(records, list):
        result["function_test_notes"] += f"read_scores returned {type(records).__name__}, not list. "
        return result

    if len(records) == len(EXPECTED_RECORDS):
        result["header_skipped"] = "yes"
    else:
        result["function_test_notes"] += f"Expected {len(EXPECTED_RECORDS)} records, got {len(records)}. "

    try:
        names = [record["name"] for record in records]
        if names == EXPECTED_NAMES:
            result["names_stored_correctly"] = "yes"
        else:
            result["function_test_notes"] += f"Student names incorrect: {names}. "
    except Exception as exc:
        result["function_test_notes"] += f"Could not extract names from records: {exc}. "

    scores_ok = True
    missing_invalid_ok = True
    averages_ok = average_helper_ok

    try:
        for record, expected in zip(records, EXPECTED_RECORDS):
            scores = normalize_score_list(record["scores"])
            expected_scores = expected["scores"]

            # Award valid conversion if the valid numeric scores are present.
            valid_scores = [score for score in scores if score is not None]
            expected_valid = [score for score in expected_scores if score is not None]
            if valid_scores != expected_valid:
                scores_ok = False
                result["function_test_notes"] += (
                    f"{expected['name']} valid scores expected {expected_valid}, got {valid_scores}. "
                )

            if scores != expected_scores:
                missing_invalid_ok = False
                # This is slightly stricter than averages; it checks that invalid/missing were preserved as None.
                result["function_test_notes"] += (
                    f"{expected['name']} score list expected {expected_scores}, got {scores}. "
                )

            if not close_enough(record["average"], expected["average"]):
                averages_ok = False
                result["function_test_notes"] += (
                    f"{expected['name']} average expected {expected['average']:.6f}, got {record['average']}. "
                )
    except Exception as exc:
        scores_ok = False
        missing_invalid_ok = False
        averages_ok = False
        result["function_test_notes"] += f"Could not inspect records: {exc}. "

    if scores_ok:
        result["scores_converted_correctly"] = "yes"
    if missing_invalid_ok:
        result["missing_invalid_handled"] = "yes"
    if averages_ok:
        result["averages_correct"] = "yes"

    if result["header_skipped"] == "yes" and result["names_stored_correctly"] == "yes" and scores_ok and averages_ok:
        result["read_csv_correct"] = "yes"

    try:
        grade_ok = True
        grade_cases = [
            (87, "A"),
            (86.99, "B"),
            (77, "B"),
            (76.99, "C"),
            (67, "C"),
            (66.99, "D"),
            (57, "D"),
            (56.99, "F"),
            (None, "N/A"),
        ]
        for average, expected_grade in grade_cases:
            actual_grade = module.letter_grade(average)
            if actual_grade != expected_grade:
                grade_ok = False
                result["function_test_notes"] += (
                    f"letter_grade({average}) expected {expected_grade}, got {actual_grade}. "
                )

        # Also check expected student grades.
        for record, expected in zip(records, EXPECTED_RECORDS):
            actual_grade = module.letter_grade(record["average"])
            if actual_grade != expected["grade"]:
                grade_ok = False
                result["function_test_notes"] += (
                    f"{expected['name']} grade expected {expected['grade']}, got {actual_grade}. "
                )

        if grade_ok:
            result["letter_grades_correct"] = "yes"
    except Exception as exc:
        result["function_test_notes"] += f"letter_grade raised: {exc}. "

    try:
        averages = [record["average"] for record in records if record["average"] is not None]
        class_average = module.calculate_average(averages)
        if (
            len(records) == 10
            and close_enough(class_average, EXPECTED_CLASS_AVERAGE)
            and close_enough(max(averages), EXPECTED_HIGHEST)
            and close_enough(min(averages), EXPECTED_LOWEST)
        ):
            result["class_summary_values_correct"] = "yes"
        else:
            result["function_test_notes"] += "Class summary values did not match expected values. "
    except Exception as exc:
        result["function_test_notes"] += f"Class summary calculation check failed: {exc}. "

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
    notes = []

    required_lines = [
        "Alice Johnson: Average = 87.67 Grade = A",
        "Ben Carter: Average = 76.67 Grade = C",
        "Carlos Rivera: Average = 93.33 Grade = A",
        "Dana Lee: Average = 90.00 Grade = A",
        "Eli Morgan: Average = 72.50 Grade = C",
        "Fatima Ahmed: Average = 84.00 Grade = B",
        "Grace Kim: Average = 90.00 Grade = A",
        "Henry Smith: Average = 65.00 Grade = D",
        "Isabella Brown: Average = 90.00 Grade = A",
        "Jackson Davis: Average = 55.00 Grade = F",
        "Number of students: 10",
        "Class average: 80.42",
        "Highest average: 93.33",
        "Lowest average: 55.00",
    ]

    for line in required_lines:
        if line not in output:
            notes.append(f"Missing expected output line: {line}")

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


def get_recent_commits(repo_dir: Path, n: int = 10) -> str:
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
        "student_scores_exists": "no",
        "student_scores_path": "",
        "quiz_scores_exists": "no",
        "quiz_scores_path": "",
        "required_functions_present": "no",
        "missing_functions": "",
        "clean_score_correct": "no",
        "read_csv_correct": "no",
        "header_skipped": "no",
        "names_stored_correctly": "no",
        "scores_converted_correctly": "no",
        "missing_invalid_handled": "no",
        "averages_correct": "no",
        "letter_grades_correct": "no",
        "class_summary_values_correct": "no",
        "terminal_run_success": "no",
        "student_report_output_clear": "no",
        "class_summary_output_clear": "no",
        "program_output": "",
        "commits_after_starter": "",
        "at_least_four_commits": "no",
        "commit_check_method": "",
        "working_tree_clean": "no",
        "recent_commits": "",
        "auto_score_out_of_18": "0",
        "manual_live_question_or_modification_out_of_2": "",
        "total_score_out_of_20": "",
        "notes": "",
    }

    ok, message = clone_or_update_repo(repo_url, repo_dir)
    result["clone_or_update"] = "yes" if ok else "no"
    if not ok:
        result["notes"] = message
        return result

    score = 1

    py_path = find_file(repo_dir, "student_scores.py")
    data_path = find_file(repo_dir, "quiz_scores.csv")

    if py_path:
        result["student_scores_exists"] = "yes"
        result["student_scores_path"] = str(py_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "student_scores.py not found. "

    if data_path:
        result["quiz_scores_exists"] = "yes"
        result["quiz_scores_path"] = str(data_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "quiz_scores.csv not found. "

    if not py_path:
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:900]
        return result

    tree, parse_note = parse_python(py_path)
    if tree is None:
        result["notes"] += f"Could not parse Python file: {parse_note}. "
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:900]
        return result

    functions = get_function_names(tree)
    missing = [fn for fn in EXPECTED_FUNCTIONS if fn not in functions]
    result["missing_functions"] = ", ".join(missing)
    if not missing:
        result["required_functions_present"] = "yes"
        score += 1

    module, load_note = load_functions_without_running_main(py_path)
    if module is not None:
        test_results = test_student_functions(module)
        for key, value in test_results.items():
            if key in result:
                result[key] = value
        result["notes"] += test_results.get("function_test_notes", "")

        for key in [
            "clean_score_correct",
            "read_csv_correct",
            "header_skipped",
            "names_stored_correctly",
            "scores_converted_correctly",
            "missing_invalid_handled",
            "averages_correct",
            "letter_grades_correct",
            "class_summary_values_correct",
        ]:
            if result[key] == "yes":
                score += 1
    else:
        result["notes"] += load_note + " "

    terminal_ok, output = run_program_from_terminal(py_path)
    result["terminal_run_success"] = "yes" if terminal_ok else "no"
    result["program_output"] = output[:1200]

    if terminal_ok:
        score += 1
        output_ok, output_notes = output_has_expected_content(output)
        if output_ok:
            result["student_report_output_clear"] = "yes"
            result["class_summary_output_clear"] = "yes"
            score += 2
        else:
            # Split partial output credit: student lines and summary lines.
            student_lines_ok = all(
                line in output for line in [
                    "Alice Johnson: Average = 87.67 Grade = A",
                    "Jackson Davis: Average = 55.00 Grade = F",
                ]
            )
            summary_lines_ok = all(
                line in output for line in [
                    "Number of students: 10",
                    "Class average: 80.42",
                    "Highest average: 93.33",
                    "Lowest average: 55.00",
                ]
            )
            if student_lines_ok:
                result["student_report_output_clear"] = "yes"
                score += 1
            if summary_lines_ok:
                result["class_summary_output_clear"] = "yes"
                score += 1
            result["notes"] += f"Output check: {output_notes}. "
    else:
        result["notes"] += "Terminal run failed. "

    commits_after, commit_note = count_commits_since_starter(repo_dir, starter_commit)
    if starter_commit:
        result["commit_check_method"] = f"commits after starter commit {starter_commit}"
        if commits_after is not None:
            result["commits_after_starter"] = str(commits_after)
            if commits_after >= 4:
                result["at_least_four_commits"] = "yes"
                score += 1
            else:
                result["notes"] += f"Expected at least 4 commits after starter commit, got {commits_after}. "
        else:
            result["notes"] += f"Commit check failed: {commit_note}. "
    else:
        result["commit_check_method"] = "fallback: total commits in repo"
        total_commits, total_note = get_total_commit_count(repo_dir)
        if total_commits is not None:
            if total_commits >= 4:
                result["at_least_four_commits"] = "yes"
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

    result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:900]
    result["auto_score_out_of_18"] = str(score)
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
        "student_scores_exists",
        "student_scores_path",
        "quiz_scores_exists",
        "quiz_scores_path",
        "required_functions_present",
        "missing_functions",
        "clean_score_correct",
        "read_csv_correct",
        "header_skipped",
        "names_stored_correctly",
        "scores_converted_correctly",
        "missing_invalid_handled",
        "averages_correct",
        "letter_grades_correct",
        "class_summary_values_correct",
        "terminal_run_success",
        "student_report_output_clear",
        "class_summary_output_clear",
        "program_output",
        "commits_after_starter",
        "at_least_four_commits",
        "commit_check_method",
        "working_tree_clean",
        "recent_commits",
        "auto_score_out_of_18",
        "manual_live_question_or_modification_out_of_2",
        "total_score_out_of_20",
        "notes",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade CPSC 250L Lab 4 student forks.")
    parser.add_argument("--students", required=True, help="Path to students.csv")
    parser.add_argument("--workdir", default="student_repos", help="Folder where repos are cloned")
    parser.add_argument("--report", default="reports/lab04_report.csv", help="Output CSV report path")
    parser.add_argument(
        "--starter-commit",
        default=None,
        help="Optional Lab 4 starter commit hash from the instructor repo",
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
