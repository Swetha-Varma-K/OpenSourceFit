import requests

repo = input("Enter repository (owner/repo): ")
skill = input("Enter your skill: ")
skills_list = skill.lower().split(",")
url = f"https://api.github.com/repos/{repo}"

response = requests.get(url)

data = response.json()
if skill.lower() == str(data["language"]).lower():
    match_score = 100
else:
    match_score = 0
issues_url = f"https://api.github.com/repos/{repo}/issues?per_page=100"
issues_response = requests.get(issues_url)
issues_data = issues_response.json()
print("Issues received:", len(issues_data))

beginner_labels = [
    "good first issue",
    "help wanted"
]

found_issues = False
recommended_count = 0

for issue in issues_data:
    if "pull_request" in issue:
        continue

    reasons = []
    is_beginner = False

    for label in issue["labels"]:
        if label["name"] in beginner_labels:
            is_beginner = True
            reasons.append(label["name"])

    if is_beginner:
        found_issues = True
        recommended_count = recommended_count + 1

        print("Issue Number:", issue["number"])
        print("Issue:")
        print(issue["title"])

        print("Reason:")
        for reason in reasons:
            print("✓", reason)

        print("Link:")
        print(issue["html_url"])

    if recommended_count == 5:
        break

if not found_issues:
    print("No beginner-friendly issues found.")
    print("Try another repository.")

print("Recommendations Found:", recommended_count)
print("Match Score:", match_score, "%")
print("Repository:", data["name"])
print("Language:", data["language"])
print("Stars:", data["stargazers_count"])
print("Description:", data["description"])
print("Open Issues:", data["open_issues_count"])