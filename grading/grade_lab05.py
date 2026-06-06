#!/usr/bin/env python3
"""
grade_lab05.py

Automated Lab 5 checker for CPSC 250L student forks.

Lab 5: Classes, Objects, and Feature Branches

This grader checks the automatable parts of the StudentRecord lab:

  - repository can be cloned/updated
  - main.py exists
  - student_record.py exists
  - StudentRecord class exists
  - __init__ stores name, student_id, and an initially empty scores list
  - add_score() accepts valid scores
  - add_score() rejects invalid scores outside 0..100
  - calculate_average() works and returns None for no scores
  - highest_score() works and returns None for no scores
  - lowest_score() works and returns None for no scores
  - letter_grade() uses the expected scale
  - __str__() returns a readable student summary
  - main.py runs from the terminal
  - Git history shows commits touching the Lab 5 folder
  - working tree is clean

Expected students.csv format:

name,github_username,repo_url,type
Edward Test,edwardbrash,https://github.com/edwardbrash/cpsc250L.git,test
Alice Smith,asmith,https://github.com/asmith/cpsc250L.git,student

The type column is optional. Use --exclude-test to skip rows marked type=test.

Recommended use:

python grade_lab05.py \
  --students students.csv \
  --workdir student_repos \
  --report reports/lab05_report.csv

The commit check uses the folder-per-lab approach by default:

  git rev-list --count HEAD -- lab05

If your Lab 5 folder has a different name, use --lab-path.
"""

from __future__ import annotations

import argparse
import ast
import csv
import importlib.util
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXPECTED_METHODS = [
    "__init__",
    "add_score",
    "calculate_average",
    "highest_score",
    "lowest_score",
    "letter_grade",
    "__str__",
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
            "lab05" not in str(p).lower() and "lab5" not in str(p).lower(),
            len(p.parts),
        )
    )
    return filtered[0]


def parse_python(py_path: Path) -> Tuple[Optional[ast.Module], str]:
    try:
        return ast.parse(py_path.read_text(encoding="utf-8")), "ok"
    except Exception as exc:
        return None, str(exc)


def get_class_method_names(tree: ast.Module, class_name: str) -> Tuple[bool, List[str]]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            methods = [
                item.name for item in node.body
                if isinstance(item, ast.FunctionDef)
            ]
            return True, methods
    return False, []


def import_student_record(py_path: Path) -> Tuple[Optional[Any], str]:
    """
    Import student_record.py directly.

    This file should only define the StudentRecord class and should not run main().
    """
    try:
        module_name = f"student_record_{abs(hash(str(py_path)))}"
        spec = importlib.util.spec_from_file_location(module_name, py_path)
        if spec is None or spec.loader is None:
            return None, "Could not create import spec."

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, "ok"
    except Exception as exc:
        return None, f"Import failed: {exc}"


def close_enough(actual: float, expected: float, tol: float = 1e-6) -> bool:
    try:
        return math.isclose(float(actual), float(expected), rel_tol=tol, abs_tol=tol)
    except Exception:
        return False


def get_scores(obj: Any) -> Optional[List[Any]]:
    """
    Try common score attribute names.
    The template indicates scores should be stored in a list.
    """
    for attr in ["scores", "score_list", "quiz_scores"]:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if isinstance(value, list):
                return value
    return None


def test_student_record_class(module: Any) -> Dict[str, str]:
    result = {
        "class_exists": "no",
        "constructor_correct": "no",
        "scores_list_initialized": "no",
        "add_score_accepts_valid": "no",
        "add_score_rejects_invalid": "no",
        "average_correct": "no",
        "empty_average_none": "no",
        "highest_correct": "no",
        "empty_highest_none": "no",
        "lowest_correct": "no",
        "empty_lowest_none": "no",
        "letter_grade_correct": "no",
        "string_representation_readable": "no",
        "class_test_notes": "",
    }

    if not hasattr(module, "StudentRecord"):
        result["class_test_notes"] += "StudentRecord class not found. "
        return result

    result["class_exists"] = "yes"
    StudentRecord = module.StudentRecord

    try:
        empty = StudentRecord("Empty Student", "E000")
    except Exception as exc:
        result["class_test_notes"] += f"Constructor raised: {exc}. "
        return result

    # Constructor attributes
    name_ok = getattr(empty, "name", None) == "Empty Student"
    id_ok = (
        getattr(empty, "student_id", None) == "E000"
        or getattr(empty, "id", None) == "E000"
    )

    if name_ok and id_ok:
        result["constructor_correct"] = "yes"
    else:
        result["class_test_notes"] += (
            f"Constructor did not store expected name/student_id. "
            f"name={getattr(empty, 'name', None)!r}, "
            f"student_id={getattr(empty, 'student_id', None)!r}, "
            f"id={getattr(empty, 'id', None)!r}. "
        )

    empty_scores = get_scores(empty)
    if empty_scores == []:
        result["scores_list_initialized"] = "yes"
    else:
        result["class_test_notes"] += f"Expected empty scores list, got {empty_scores!r}. "

    # Empty methods
    try:
        if empty.calculate_average() is None:
            result["empty_average_none"] = "yes"
        else:
            result["class_test_notes"] += f"Empty average expected None, got {empty.calculate_average()!r}. "
    except Exception as exc:
        result["class_test_notes"] += f"calculate_average on empty student raised: {exc}. "

    try:
        if empty.highest_score() is None:
            result["empty_highest_none"] = "yes"
        else:
            result["class_test_notes"] += f"Empty highest expected None, got {empty.highest_score()!r}. "
    except Exception as exc:
        result["class_test_notes"] += f"highest_score on empty student raised: {exc}. "

    try:
        if empty.lowest_score() is None:
            result["empty_lowest_none"] = "yes"
        else:
            result["class_test_notes"] += f"Empty lowest expected None, got {empty.lowest_score()!r}. "
    except Exception as exc:
        result["class_test_notes"] += f"lowest_score on empty student raised: {exc}. "

    # Add valid scores
    try:
        alice = StudentRecord("Alice Johnson", "A001")
        for score in [85, 90, 88]:
            alice.add_score(score)

        scores = get_scores(alice)
        if scores == [85, 90, 88]:
            result["add_score_accepts_valid"] = "yes"
        else:
            result["class_test_notes"] += f"After valid adds, expected [85, 90, 88], got {scores!r}. "

        if close_enough(alice.calculate_average(), 87.6666666667):
            result["average_correct"] = "yes"
        else:
            result["class_test_notes"] += f"Alice average expected 87.6667, got {alice.calculate_average()!r}. "

        if alice.highest_score() == 90:
            result["highest_correct"] = "yes"
        else:
            result["class_test_notes"] += f"Alice highest expected 90, got {alice.highest_score()!r}. "

        if alice.lowest_score() == 85:
            result["lowest_correct"] = "yes"
        else:
            result["class_test_notes"] += f"Alice lowest expected 85, got {alice.lowest_score()!r}. "

        string_value = str(alice)
        lowered = string_value.lower()
        readable_clues = [
            "alice" in lowered,
            "a001" in lowered,
            "87" in string_value or "88" in string_value,
            "90" in string_value,
            "85" in string_value,
            "a" in lowered,
            "dummy string" not in lowered,
        ]
        if all(readable_clues):
            result["string_representation_readable"] = "yes"
        else:
            result["class_test_notes"] += f"__str__ output not sufficiently informative: {string_value!r}. "

    except Exception as exc:
        result["class_test_notes"] += f"Valid score/object tests raised: {exc}. "

    # Reject invalid scores
    try:
        invalid = StudentRecord("Invalid Tester", "I999")
        for score in [-10, 0, 100, 105, 72]:
            invalid.add_score(score)

        scores = get_scores(invalid)
        if scores == [0, 100, 72]:
            result["add_score_rejects_invalid"] = "yes"
        else:
            result["class_test_notes"] += f"Invalid-score test expected [0, 100, 72], got {scores!r}. "
    except Exception as exc:
        result["class_test_notes"] += f"Invalid score test raised: {exc}. "

    # Letter grade scale
    try:
        grade_cases = [
            ([87], "A"),
            ([86.99], "B"),
            ([77], "B"),
            ([76.99], "C"),
            ([67], "C"),
            ([66.99], "D"),
            ([57], "D"),
            ([56.99], "F"),
        ]

        grade_ok = True
        for scores, expected_grade in grade_cases:
            student = StudentRecord("Grade Tester", "G000")
            for score in scores:
                student.add_score(score)
            actual_grade = student.letter_grade()
            if actual_grade != expected_grade:
                grade_ok = False
                result["class_test_notes"] += (
                    f"letter_grade for average {scores[0]} expected {expected_grade}, got {actual_grade!r}. "
                )

        if grade_ok:
            result["letter_grade_correct"] = "yes"

    except Exception as exc:
        result["class_test_notes"] += f"Letter grade tests raised: {exc}. "

    return result


def run_main_from_terminal(main_path: Path) -> Tuple[bool, str]:
    code, out, err = run_command(
        [sys.executable, str(main_path.name)],
        cwd=main_path.parent,
        timeout=10,
    )
    if code == 0:
        return True, out
    return False, err or out


def main_output_readable(output: str) -> Tuple[bool, str]:
    lowered = output.lower()
    notes = []

    # The accepted Lab 5 output may simply print each StudentRecord object.
    # We therefore look for evidence that the three sample students were printed
    # and that the __str__ output is not still the template "dummy string".
    for name in ["alice", "ben", "carlos"]:
        if name not in lowered:
            notes.append(f"Missing {name} in main output")

    for student_id in ["a001", "b002", "c003"]:
        if student_id not in lowered:
            notes.append(f"Missing student id clue {student_id}")

    # These values appear in the sample objects' score lists.
    for clue in ["85", "90", "88", "72", "78", "80", "91", "95", "94"]:
        if clue not in output:
            notes.append(f"Missing score clue {clue}")

    if "dummy string" in lowered:
        notes.append("Output still contains dummy string")

    nonempty_lines = [line for line in output.splitlines() if line.strip()]
    if len(nonempty_lines) < 3:
        notes.append("Output has fewer than three non-empty lines")

    return len(notes) == 0, "; ".join(notes)


def count_commits_touching_path(repo_dir: Path, lab_path: Path) -> Tuple[Optional[int], str]:
    """
    Count commits that touched files under lab_path.

    This is better than total repo commits for this course because each lab lives
    in its own folder. A student who has completed Labs 1-4 but has not touched
    Lab 5 should receive zero Lab 5 commit credit.
    """
    path_arg = str(lab_path.as_posix())
    code, out, err = run_command(
        ["git", "rev-list", "--count", "HEAD", "--", path_arg],
        cwd=repo_dir,
    )

    if code != 0:
        return None, err or out

    try:
        return int(out), "ok"
    except ValueError:
        return None, f"could not parse commit count: {out}"


def get_recent_commits_touching_path(repo_dir: Path, lab_path: Path, n: int = 10) -> str:
    path_arg = str(lab_path.as_posix())
    code, out, err = run_command(
        ["git", "log", "--oneline", f"-{n}", "--", path_arg],
        cwd=repo_dir,
    )
    return out if code == 0 else err


def get_recent_commits(repo_dir: Path, n: int = 10) -> str:
    code, out, err = run_command(["git", "log", "--oneline", f"-{n}"], cwd=repo_dir)
    return out if code == 0 else err


def get_branch_info(repo_dir: Path) -> str:
    code, out, err = run_command(["git", "branch", "-a"], cwd=repo_dir)
    return out if code == 0 else err


def is_working_tree_clean(repo_dir: Path) -> Tuple[bool, str]:
    code, out, err = run_command(["git", "status", "--porcelain"], cwd=repo_dir)
    if code != 0:
        return False, err or out

    if out.strip() == "":
        return True, "clean"

    return False, out.replace("\n", " | ")


def grade_student(row: Dict[str, str], workdir: Path, lab_path_arg: str, min_lab_commits: int) -> Dict[str, str]:
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
        "main_exists": "no",
        "main_path": "",
        "student_record_exists": "no",
        "student_record_path": "",
        "student_record_class_exists": "no",
        "required_methods_present": "no",
        "missing_methods": "",
        "constructor_correct": "no",
        "scores_list_initialized": "no",
        "add_score_accepts_valid": "no",
        "add_score_rejects_invalid": "no",
        "average_correct": "no",
        "empty_average_none": "no",
        "highest_correct": "no",
        "empty_highest_none": "no",
        "lowest_correct": "no",
        "empty_lowest_none": "no",
        "letter_grade_correct": "no",
        "string_representation_readable": "no",
        "main_runs_from_terminal": "no",
        "main_output_readable": "no",
        "main_output": "",
        "lab_path_checked": "",
        "commits_touching_lab": "",
        "meaningful_commit_evidence": "no",
        "commit_check_method": "",
        "recent_lab_commits": "",
        "working_tree_clean": "no",
        "recent_commits": "",
        "branch_info": "",
        "auto_score_out_of_21": "0",
        "manual_feature_branch_review_notes": "",
                "notes": "",
    }

    ok, message = clone_or_update_repo(repo_url, repo_dir)
    result["clone_or_update"] = "yes" if ok else "no"
    if not ok:
        result["notes"] = message
        return result

    score = 0

    main_path = find_file(repo_dir, "main.py")
    record_path = find_file(repo_dir, "student_record.py")

    # Determine which lab path to use for the Git commit check.
    # By default this is lab05, but --lab-path can override it.
    if lab_path_arg:
        lab_path_for_commits = Path(lab_path_arg)
    elif record_path:
        lab_path_for_commits = record_path.parent.relative_to(repo_dir)
    elif main_path:
        lab_path_for_commits = main_path.parent.relative_to(repo_dir)
    else:
        lab_path_for_commits = Path("lab05")

    if str(lab_path_for_commits) == ".":
        lab_path_for_commits = Path(".")

    result["lab_path_checked"] = str(lab_path_for_commits)

    # If neither Lab 5 file exists, this is not a submitted Lab 5 attempt.
    # Do not award generic repo-level points such as clone/update, commit history,
    # or clean working tree. Those are useful diagnostics, but not Lab 5 credit.
    if not main_path and not record_path:
        result["notes"] += "No Lab 5 files found; no Lab 5 credit awarded. "
        lab_commit_count, lab_commit_note = count_commits_touching_path(repo_dir, lab_path_for_commits)
        if lab_commit_count is not None:
            result["commits_touching_lab"] = str(lab_commit_count)
        else:
            result["notes"] += f"Lab commit check failed: {lab_commit_note}. "
        result["commit_check_method"] = f"commits touching {lab_path_for_commits}"
        result["recent_lab_commits"] = get_recent_commits_touching_path(repo_dir, lab_path_for_commits).replace("\n", " | ")[:900]
        result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:900]
        result["branch_info"] = get_branch_info(repo_dir).replace("\n", " | ")[:900]
        result["auto_score_out_of_21"] = str(score)
        return result

    # At least one Lab 5 file exists, so the repo was reachable and contains
    # something that appears to be a Lab 5 submission.
    score += 1

    if main_path:
        result["main_exists"] = "yes"
        result["main_path"] = str(main_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "main.py not found. "

    if record_path:
        result["student_record_exists"] = "yes"
        result["student_record_path"] = str(record_path.relative_to(repo_dir))
        score += 1
    else:
        result["notes"] += "student_record.py not found. "

    if record_path:
        tree, parse_note = parse_python(record_path)
        if tree is not None:
            class_exists, methods = get_class_method_names(tree, "StudentRecord")
            result["student_record_class_exists"] = "yes" if class_exists else "no"
            if class_exists:
                score += 1

            missing = [method for method in EXPECTED_METHODS if method not in methods]
            result["missing_methods"] = ", ".join(missing)
            if not missing:
                result["required_methods_present"] = "yes"
                score += 1
        else:
            result["notes"] += f"Could not parse student_record.py: {parse_note}. "

        module, import_note = import_student_record(record_path)
        if module is not None:
            class_results = test_student_record_class(module)
            result["student_record_class_exists"] = class_results.get("class_exists", result["student_record_class_exists"])
            for key, value in class_results.items():
                if key in result:
                    result[key] = value
            result["notes"] += class_results.get("class_test_notes", "")

            for key in [
                "constructor_correct",
                "scores_list_initialized",
                "add_score_accepts_valid",
                "add_score_rejects_invalid",
                "average_correct",
                "empty_average_none",
                "highest_correct",
                "empty_highest_none",
                "lowest_correct",
                "empty_lowest_none",
                "letter_grade_correct",
                "string_representation_readable",
            ]:
                if result[key] == "yes":
                    score += 1
        else:
            result["notes"] += import_note + " "

    if main_path:
        run_ok, output = run_main_from_terminal(main_path)
        result["main_runs_from_terminal"] = "yes" if run_ok else "no"
        result["main_output"] = output[:1200]
        if run_ok:
            score += 1
            readable, output_note = main_output_readable(output)
            if readable:
                result["main_output_readable"] = "yes"
                score += 1
            else:
                result["notes"] += f"Main output check: {output_note}. "
        else:
            result["notes"] += "main.py did not run successfully from terminal. "

    lab_commit_count, lab_commit_note = count_commits_touching_path(repo_dir, lab_path_for_commits)
    result["commit_check_method"] = f"commits touching {lab_path_for_commits}"
    if lab_commit_count is not None:
        result["commits_touching_lab"] = str(lab_commit_count)
        if lab_commit_count >= min_lab_commits:
            result["meaningful_commit_evidence"] = "yes"
            score += 1
        else:
            result["notes"] += (
                f"Expected at least {min_lab_commits} commits touching {lab_path_for_commits}, "
                f"got {lab_commit_count}. "
            )
    else:
        result["notes"] += f"Lab commit check failed: {lab_commit_note}. "

    result["recent_lab_commits"] = get_recent_commits_touching_path(repo_dir, lab_path_for_commits).replace("\n", " | ")[:900]

    clean, clean_note = is_working_tree_clean(repo_dir)
    result["working_tree_clean"] = "yes" if clean else "no"
    if clean:
        score += 1
    else:
        result["notes"] += f"Working tree: {clean_note}. "

    result["recent_commits"] = get_recent_commits(repo_dir).replace("\n", " | ")[:900]
    result["branch_info"] = get_branch_info(repo_dir).replace("\n", " | ")[:900]
    result["auto_score_out_of_21"] = str(score)
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
        "main_exists",
        "main_path",
        "student_record_exists",
        "student_record_path",
        "student_record_class_exists",
        "required_methods_present",
        "missing_methods",
        "constructor_correct",
        "scores_list_initialized",
        "add_score_accepts_valid",
        "add_score_rejects_invalid",
        "average_correct",
        "empty_average_none",
        "highest_correct",
        "empty_highest_none",
        "lowest_correct",
        "empty_lowest_none",
        "letter_grade_correct",
        "string_representation_readable",
        "main_runs_from_terminal",
        "main_output_readable",
        "main_output",
        "lab_path_checked",
        "commits_touching_lab",
        "meaningful_commit_evidence",
        "commit_check_method",
        "recent_lab_commits",
        "working_tree_clean",
        "recent_commits",
        "branch_info",
        "auto_score_out_of_21",
        "manual_feature_branch_review_notes",
        "notes",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade CPSC 250L Lab 5 student forks.")
    parser.add_argument("--students", required=True, help="Path to students.csv")
    parser.add_argument("--workdir", default="student_repos", help="Folder where repos are cloned")
    parser.add_argument("--report", default="reports/lab05_report.csv", help="Output CSV report path")
    parser.add_argument(
        "--lab-path",
        default="lab05",
        help="Path to the Lab 5 folder inside each student repo. Defaults to lab05.",
    )
    parser.add_argument(
        "--min-lab-commits",
        type=int,
        default=2,
        help="Minimum number of commits touching the Lab 5 folder required for commit credit.",
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
        results.append(grade_student(student, workdir, args.lab_path, args.min_lab_commits))

    write_report(report_path, results)
    print(f"\nWrote report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
