import os
from collections import defaultdict
from lxml import etree

result_dir = "test-results"
test_outcomes = defaultdict(set)

for root, _, files in os.walk(result_dir):
    for file in files:
        if file.endswith(".xml"):
            path = os.path.join(root, file)
            tree = etree.parse(path)
            for testcase in tree.xpath("//testcase"):
                name = testcase.get("classname") + "::" + testcase.get("name")
                if testcase.xpath("failure") or testcase.xpath("error"):
                    test_outcomes[name].add("fail")
                else:
                    test_outcomes[name].add("pass")

flaky_tests = [name for name, outcomes in test_outcomes.items() if len(outcomes) > 1]

if flaky_tests:
    print("Flaky tests detected:")
    for t in flaky_tests:
        print(f"- {t}")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        f.write("## 🌀 Flaky Tests Detected\n")
        for t in flaky_tests:
            f.write(f"- {t}\n")
else:
    print("No flaky tests detected.")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        f.write("✅ No flaky tests detected.\n")
