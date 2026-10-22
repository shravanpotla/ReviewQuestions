def get_num(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Enter a valid number.")
n = get_num("Enter number of teams: ")

while n < 2:
    print("Minimum 2 teams required.")
    n = get_num("Enter number of teams: ")
teams = []

for i in range(n):
    while True:
        name = input("Enter team name: ").strip()

        if not name:
            print("Team name cannot be empty.")
        elif name.lower() in [t.lower() for t in teams]:
            print("Team already exists.")
        else:
            teams.append(name)
            break
stats = {}

for team in teams:
    stats[team] = {
        "played": 0,
        "won": 0,
        "lost": 0,
        "tied": 0,
        "points": 0,
        "runs": 0,
        "given": 0,
        "faced": 0,
        "bowled": 0,
        "nrr": 0.0
    }
for i in range(n):
    for j in range(i + 1, n):
        for match in range(2):

            team1 = teams[i]
            team2 = teams[j]

            print("Match:", team1, "vs", team2)

            runs1 = get_num(team1 + " runs: ")
            wickets1 = get_num(team1 + " wickets: ")
            overs1 = get_num(team1 + " completed overs: ")
            balls1 = get_num(team1 + " remaining balls: ")

            runs2 = get_num(team2 + " runs: ")
            wickets2 = get_num(team2 + " wickets: ")
            overs2 = get_num(team2 + " completed overs: ")
            balls2 = get_num(team2 + " remaining balls: ")

            if (
                runs1 < 0 or runs2 < 0
                or not 0 <= wickets1 <= 10
                or not 0 <= wickets2 <= 10
                or not 0 <= overs1 <= 20
                or not 0 <= overs2 <= 20
                or not 0 <= balls1 <= 5
                or not 0 <= balls2 <= 5
                or (overs1 == 20 and balls1 > 0)
                or (overs2 == 20 and balls2 > 0)
            ):
                print("Invalid match data. Skipping this match.")
                continue

            total1 = overs1 * 6 + balls1
            total2 = overs2 * 6 + balls2

            if wickets1 == 10:
                total1 = 120

            if wickets2 == 10:
                total2 = 120

            stats[team1]["played"] += 1
            stats[team2]["played"] += 1

            stats[team1]["runs"] += runs1
            stats[team1]["given"] += runs2
            stats[team1]["faced"] += total1
            stats[team1]["bowled"] += total2

            stats[team2]["runs"] += runs2
            stats[team2]["given"] += runs1
            stats[team2]["faced"] += total2
            stats[team2]["bowled"] += total1

            if runs1 > runs2:
                stats[team1]["won"] += 1
                stats[team1]["points"] += 2
                stats[team2]["lost"] += 1

            elif runs2 > runs1:
                stats[team2]["won"] += 1
                stats[team2]["points"] += 2
                stats[team1]["lost"] += 1

            else:
                stats[team1]["tied"] += 1
                stats[team2]["tied"] += 1
                stats[team1]["points"] += 1
                stats[team2]["points"] += 1


for team in teams:
    s = stats[team]

    if s["faced"] > 0 and s["bowled"] > 0:
        run_rate = s["runs"] * 6 / s["faced"]
        given_rate = s["given"] * 6 / s["bowled"]
        s["nrr"] = run_rate - given_rate


for i in range(n - 1):
    for j in range(n - i - 1):

        team1 = teams[j]
        team2 = teams[j + 1]

        p1 = stats[team1]["points"]
        p2 = stats[team2]["points"]

        nrr1 = stats[team1]["nrr"]
        nrr2 = stats[team2]["nrr"]

        if p1 < p2 or (p1 == p2 and nrr1 < nrr2):
            teams[j], teams[j + 1] = teams[j + 1], teams[j]


print("\nFINAL POINTS TABLE")
print("-" * 100)

print("Pos Team Played Won Lost Tied Points Runs Given NRR")

for i in range(n):
    team = teams[i]
    s = stats[team]

    print(
        i + 1,
        team,
        s["played"],
        s["won"],
        s["lost"],
        s["tied"],
        s["points"],
        s["runs"],
        s["given"],
        round(s["nrr"], 3)
    )
