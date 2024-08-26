import re
from collections import namedtuple
from pathlib import Path


FeedbackType = namedtuple('FeedbackType', ['format', 'name'])

ROOT = Path("D:/ExternalRepos/third_party/Paradise")

blackbox_lines = []
pattern = "SSblackbox.record_feedback\(\"([\w\s]+)\"\s*,\s*\"([\w\s_-]+)"

feedback_names = set()
feedback_types = list()

for codefile in ROOT.glob("code/**/*.dm"):
    with open(codefile, encoding='utf-8') as code:
        lines = code.readlines()
        for line in lines:
            if m := re.search(pattern, line):
                if m.group(2) not in feedback_names:
                    feedback_type = FeedbackType(m.group(1), m.group(2))
                    feedback_types.append(feedback_type)
                    feedback_names.add(feedback_type.name)
            

code_template = """
from enum import Enum

class Feedback(Enum):
"""
with open("D:/ExternalRepos/ss13_blackbox_tools/feedback.py", 'w') as f:
    f.write(code_template)
    for feedback in list(sorted(feedback_types, key=lambda x: x.name.upper())):
        f.write(f"    {feedback.name.upper().replace(' ', '_')} = \"{feedback.name}\"\n")
        
