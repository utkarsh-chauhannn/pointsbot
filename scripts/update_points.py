import json
import sys

# Load event data (from GitHub Actions or local testing)
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        event = json.load(f)
else:
    with open("sample_event.json", "r") as f:
        event = json.load(f)

# Load current points
try:
    with open("points.json", "r") as f:
        points = json.load(f)
except FileNotFoundError:
    points = {}

# Determine user
actor = event.get("sender", {}).get("login")

# Determine action type and assign points
if "commits" in event:
    # push event
    num_commits = len(event["commits"])
    points[actor] = points.get(actor, 0) + (num_commits * 5)
elif "pull_request" in event:
    pr = event["pull_request"]
    if event.get("action") == "opened":
        points[actor] = points.get(actor, 0) + 10
    elif event.get("action") == "closed" and pr.get("merged"):
        points[actor] = points.get(actor, 0) + 20
elif "issue" in event and event.get("action") == "opened":
    points[actor] = points.get(actor, 0) + 5
elif "comment" in event and event.get("action") == "created":
    points[actor] = points.get(actor, 0) + 2
elif "review" in event and event.get("action") == "submitted":
    points[actor] = points.get(actor, 0) + 7

# Save back to file
with open("points.json", "w") as f:
    json.dump(points, f, indent=2)

print("Points updated successfully.")
