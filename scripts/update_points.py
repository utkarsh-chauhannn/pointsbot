import json
import os
import sys
from collections import defaultdict

POINTS_FILE = "points.json"
LEADERBOARD_FILE = "leaderboard.md"

# Points per event type
EVENT_POINTS = {
    "push": 5,
    "pull_request": 10,
    "issues": 7,
    "issue_comment": 3,
    "pull_request_review": 5
}

# Load GitHub event from event.json
def load_event(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Load existing points data
def load_points():
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save points to file
def save_points(data):
    with open(POINTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Generate and save leaderboard
def save_leaderboard(points_data):
    sorted_users = sorted(points_data.items(), key=lambda x: x[1], reverse=True)
    with open(LEADERBOARD_FILE, "w") as f:
        f.write("# 🏆 Leaderboard\n\n")
        f.write("| Rank | Contributor | Points |\n")
        f.write("|------|-------------|--------|\n")
        for i, (user, pts) in enumerate(sorted_users, start=1):
            f.write(f"| {i} | {user} | {pts} |\n")

def get_actor_username(event):
    return event.get("sender", {}).get("login", "unknown")

def get_event_type():
    return os.getenv("GITHUB_EVENT_NAME", "unknown")

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_points.py <event.json>")
        sys.exit(1)

    event_file = sys.argv[1]
    event_data = load_event(event_file)
    event_type = get_event_type()
    username = get_actor_username(event_data)

    if username == "unknown":
        print("⚠️ Could not determine username. Exiting.")
        sys.exit(1)

    # Load and update points
    points = load_points()
    current_points = points.get(username, 0)
    earned = EVENT_POINTS.get(event_type, 0)

    points[username] = current_points + earned
    print(f"✅ {username} earned {earned} points for {event_type} — total: {points[username]}")

    save_points(points)
    save_leaderboard(points)

if __name__ == "__main__":
    main()
