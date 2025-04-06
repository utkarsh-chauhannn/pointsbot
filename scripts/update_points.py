import json
import sys
import os

# Define points for each event type
POINTS = {
    "push": 5,                # Code pushed
    "pull_request": 10,       # PR opened
    "issues": 3,              # Issue opened
    "issue_comment": 2,       # Comment added
    "pull_request_review": 4  # Review done
}

# Get event file
event_file = sys.argv[1] if len(sys.argv) > 1 else "sample_event.json"

# Load GitHub event
with open(event_file) as f:
    event = json.load(f)

# Detect event type automatically
event_type = os.getenv("GITHUB_EVENT_NAME", "unknown")

# Load or initialize points
try:
    with open("points.json") as f:
        points = json.load(f)
except FileNotFoundError:
    points = {}

# Get actor
actor = (
    event.get("sender", {}) or
    event.get("pull_request", {}).get("user", {}) or
    {}
).get("login")

# Update points if valid
if actor and event_type in POINTS:
    points[actor] = points.get(actor, 0) + POINTS[event_type]
    print(f"✅ Added {POINTS[event_type]} points to {actor} for {event_type}")
else:
    print(f"⚠️ Skipping event '{event_type}' for actor '{actor}'")

# Save updated points
with open("points.json", "w") as f:
    json.dump(points, f, indent=2, sort_keys=True)

# Write markdown leaderboard
with open("leaderboard.md", "w") as f:
    f.write("# 🏆 GSoC-style Leaderboard\n\n")
    for i, (user, score) in enumerate(sorted(points.items(), key=lambda x: x[1], reverse=True), 1):
        f.write(f"{i}. **{user}** — {score} points\n")

print("📊 Leaderboard generated.")
