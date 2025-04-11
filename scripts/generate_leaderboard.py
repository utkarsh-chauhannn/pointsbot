import json

POINTS_FILE = "points.json"
LEADERBOARD_FILE = "leaderboard.md"

def load_points():
    try:
        with open(POINTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def generate_leaderboard(points):
    sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)

    leaderboard = ["# 🏆 Contributor Leaderboard\n"]
    leaderboard.append("| Rank | Username | Points |")
    leaderboard.append("|------|----------|--------|")

    for idx, (user, pts) in enumerate(sorted_points, start=1):
        leaderboard.append(f"| {idx} | [{user}](https://github.com/{user}) | {pts} |")

    return "\n".join(leaderboard)

def save_leaderboard(content):
    with open(LEADERBOARD_FILE, "w") as f:
        f.write(content)

def main():
    points = load_points()
    leaderboard_md = generate_leaderboard(points)
    save_leaderboard(leaderboard_md)
    print("✅ Leaderboard generated successfully.")

if __name__ == "__main__":
    main()
