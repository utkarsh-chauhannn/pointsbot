import json
import os
import sys

POINTS_FILE = "points.json"

EVENT_POINTS = {
    "push": 5,
    "pull_request": 10,
    "issues": 7,
    "issue_comment": 3
   
}

def load_event(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def load_points():
    if os.path.exists(POINTS_FILE):
        with open(POINTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_points(data):
    with open(POINTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

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

    # Debug output to understand the event during testing
    print("DEBUG EVENT TYPE:", event_type)
    print("DEBUG USERNAME:", username)
    print("DEBUG RAW EVENT DATA:")
    print(json.dumps(event_data, indent=2))

    if username == "unknown":
        print(" Could not determine username. Exiting.")
        sys.exit(1)

    points = load_points()
    current_points = points.get(username, 0)
    earned = EVENT_POINTS.get(event_type, 0)

    if earned == 0:
        print(f" No points configured for event type '{event_type}'")
    else:
        points[username] = current_points + earned
        print(f" {username} earned {earned} points for {event_type} — total: {points[username]}")
        save_points(points)

if __name__ == "__main__":
    main()
