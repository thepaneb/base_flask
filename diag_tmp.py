"""Diagnóstico do run release (apagar após uso)."""

import json
import urllib.request

runs = json.load(
    urllib.request.urlopen(
        "https://api.github.com/repos/thepaneb/base_flask/actions/runs?per_page=5"
    )
)
run = next(w for w in runs["workflow_runs"] if w["name"] == "release")
print(run["id"], "|", run["head_sha"][:7], "|", run.get("conclusion"))
jobs = json.load(
    urllib.request.urlopen(
        f"https://api.github.com/repos/thepaneb/base_flask/actions/runs/{run['id']}/jobs?per_page=5"
    )
)
for job in jobs["jobs"]:
    print("##", job["name"], "|", job.get("conclusion"))
    for step in job.get("steps", []):
        if step.get("conclusion") not in (None, "success"):
            print("  -", step["name"], "|", step.get("conclusion"))
