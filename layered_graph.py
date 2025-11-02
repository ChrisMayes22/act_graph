import os
import json
import glob
import matplotlib.pyplot as plt
import inquirer  # pip install inquirer

plt.style.use('ggplot')


def load_tests():
    """
    Load ALL .json test files in the current directory.
    Each JSON must have at least: { "name": "...", "questions": [...] }
    """
    tests = {}
    for path in glob.glob("*.json"):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            # must have a name and questions to count as a test
            if "name" in data and "questions" in data:
                tests[data["name"]] = data
        except Exception as e:
            # skip files that aren't valid test jsons
            print(f"Skipping {path}: {e}")
    return tests


def build_question_map(test_data):
    """Return {1: 'Detail', 2: 'Inference', ...}"""
    return {q['number']: q['type'] for q in test_data['questions']}


def total_questions_by_type(test_data):
    """Return {'Detail': 14, 'Inference': 12, ...}"""
    totals = {}
    for q in test_data['questions']:
        qtype = q['type']
        totals[qtype] = totals.get(qtype, 0) + 1
    return totals


def prompt_for_test(tests_dict):
    """Display a dropdown of available tests."""
    if not tests_dict:
        raise RuntimeError("No test JSON files found in current directory.")
    test_names = list(tests_dict.keys())
    questions = [
        inquirer.List(
            'test_name',
            message="Select a test:",
            choices=test_names
        )
    ]
    answers = inquirer.prompt(questions)
    return answers['test_name']


def collect_missed_questions(question_map):
    """Prompt user for missed question numbers."""
    missed = []
    while True:
        raw = input("Enter missed question # (or 'q' to finish): ").strip()
        if raw.lower() == 'q':
            break
        if not raw.isdigit():
            print("Please enter a valid question number (or 'q').")
            continue
        qnum = int(raw)
        if qnum not in question_map:
            print("That question number is not in this test.")
            continue
        missed.append(qnum)
    return missed


def count_missed_by_type(missed_questions, question_map):
    """Return missed counts by type."""
    missed_counts = {}
    for qnum in missed_questions:
        qtype = question_map[qnum]
        missed_counts[qtype] = missed_counts.get(qtype, 0) + 1
    return missed_counts


def plot_per_type_stacked(test_name, totals_by_type, missed_by_type):
    """
    Sort by total # of questions.
    Each bar = total questions of that type.
    Green = correct, Red = missed.
    Displays 'x/n' label on top of each bar.
    """
    # Sort by total number of questions (descending)
    sorted_items = sorted(
        totals_by_type.items(),
        key=lambda x: x[1],
        reverse=True
    )

    types = [t for t, _ in sorted_items]
    totals = [totals_by_type[t] for t in types]
    missed = [missed_by_type.get(t, 0) for t in types]
    correct = [totals[i] - missed[i] for i in range(len(types))]

    x_pos = range(len(types))
    fig, ax = plt.subplots(figsize=(12, 8))

    # Correct section (bottom)
    ax.bar(x_pos, correct, color='green', label='Correct')

    # Missed section (top)
    ax.bar(x_pos, missed, bottom=correct, color='red', label='Missed')

    # Add labels 'x/n' on top of each full bar
    for i, (c, m, total) in enumerate(zip(correct, missed, totals)):
        label = f"{c}/{total}"
        ax.text(i, c + m + 0.2, label, ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(types, rotation=25, ha='right')
    ax.set_ylabel("Number of Questions")
    ax.set_xlabel("Question Type")
    ax.set_title(f"Errors for {test_name}")
    ax.legend()

    # pad top so labels don't get cut off
    ymax = max(totals) + 1
    ax.set_ylim(0, ymax)

    plt.tight_layout(pad=1.5)
    plt.show()


def main():
    tests = load_tests()
    chosen_test_name = prompt_for_test(tests)
    test_data = tests[chosen_test_name]

    question_map = build_question_map(test_data)
    totals_by_type = total_questions_by_type(test_data)

    missed_questions = collect_missed_questions(question_map)
    missed_by_type = count_missed_by_type(missed_questions, question_map)

    plot_per_type_stacked(chosen_test_name, totals_by_type, missed_by_type)


if __name__ == "__main__":
    main()
