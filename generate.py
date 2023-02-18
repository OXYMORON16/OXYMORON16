#!/usr/bin/env python
import datetime
import random

# GitHub username
username = "OXYMORON16"

# Generate a random date within the last year
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)
random_date = start_date + datetime.timedelta(days=random.randrange((end_date - start_date).days))

# Generate random commit data
commit_count = random.randrange(1, 6)
commits = []
for i in range(commit_count):
    hour = random.randrange(0, 24)
    minute = random.randrange(0, 60)
    second = random.randrange(0, 60)
    commits.append(f"{random_date}T{hour:02d}:{minute:02d}:{second:02d}Z")

# Generate the output string
output = ""
for i in range(365):
    if i > 0:
        output += "\n"
    date = start_date + datetime.timedelta(days=i)
    if date == random_date:
        output += f"{date} {''.join(commits)}"
    else:
        output += f"{date} "

# Write the output string to a file
with open(f"tmp/{username}.txt", "w") as f:
    f.write(output)
