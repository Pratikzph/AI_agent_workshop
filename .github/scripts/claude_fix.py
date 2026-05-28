import os
import json
import subprocess
from openai import OpenAI
from github import Github

GITHUB_TOKEN  = os.environ["GITHUB_TOKEN"]
REPO_NAME     = os.environ["REPO"]
ISSUE_NUMBER  = int(os.environ["ISSUE_NUMBER"])
ISSUE_TITLE   = os.environ.get("ISSUE_TITLE", "")
ISSUE_BODY    = os.environ.get("ISSUE_BODY", "")
COMMENT_BODY  = os.environ.get("COMMENT_BODY", "")

# GitHub Models — no separate API key, uses GITHUB_TOKEN
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
)

gh   = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)
issue = repo.get_issue(ISSUE_NUMBER)


def get_repo_files():
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    return [f for f in result.stdout.strip().split("\n") if f]


def read_file(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return None


# Collect repo context (cap size so we stay within token limits)
files = get_repo_files()
file_contents = {}
total_chars = 0
for path in files:
    if total_chars > 40_000:
        break
    content = read_file(path)
    if content:
        file_contents[path] = content
        total_chars += len(content)

files_section = "\n\n".join(
    f"### {p}\n```\n{c}\n```" for p, c in file_contents.items()
)

prompt = f"""You are a software engineer. A GitHub issue has been raised and you must fix it.

## Issue #{ISSUE_NUMBER}: {ISSUE_TITLE}

{ISSUE_BODY}

## Trigger comment
{COMMENT_BODY}

## Current repository files

{files_section}

## Task
Analyse the issue and return a JSON object (no other text) with this exact structure:
{{
  "branch_name": "fix/issue-{ISSUE_NUMBER}-short-description",
  "pr_title": "fix: concise description",
  "pr_body": "## Summary\\nWhat was fixed.\\n\\n## Changes\\n- `file`: reason\\n\\n## How to verify\\nSteps to confirm the fix works.\\n\\nCloses #{ISSUE_NUMBER}",
  "files": [
    {{
      "path": "relative/path/to/file",
      "content": "complete new file content here"
    }}
  ]
}}

Rules:
- Only include files that actually need changing.
- If nothing in the repo needs changing (e.g. it is a question, not a bug), set "files" to [].
- Return only valid JSON. No markdown fences, no explanation.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=4096,
)

raw = response.choices[0].message.content.strip()

# Strip accidental code fences
if raw.startswith("```"):
    raw = raw.split("```", 2)[1]
    if raw.startswith("json"):
        raw = raw[4:]
    raw = raw.rsplit("```", 1)[0].strip()

fix = json.loads(raw)

if not fix.get("files"):
    issue.create_comment(
        "I looked at the issue but found no code changes needed. "
        "Could you provide more details or a minimal reproduction?"
    )
    print("No files to change — commented on issue.")
    exit(0)

# Configure git
subprocess.run(["git", "config", "user.name",  "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

branch = fix["branch_name"]
subprocess.run(["git", "checkout", "-b", branch], check=True)

for change in fix["files"]:
    path = change["path"]
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(change["content"])
    subprocess.run(["git", "add", path], check=True)

subprocess.run(["git", "commit", "-m", f"fix: resolve issue #{ISSUE_NUMBER}"], check=True)
subprocess.run(["git", "push", "origin", branch], check=True)

pr = repo.create_pull(
    title=fix["pr_title"],
    body=fix["pr_body"],
    head=branch,
    base="main",
)

issue.create_comment(
    f"I've analysed the issue and opened a pull request with a fix: {pr.html_url}"
)
print(f"PR created: {pr.html_url}")
