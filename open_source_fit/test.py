import requests

repo = input("Enter repository (owner/repo): ")
skill = input("Enter your skill: ")
skills_list = [s.strip().lower() for s in skill.split(",")]
url = f"https://api.github.com/repos/{repo}"

response = requests.get(url)

data = response.json()
repo_language = str(data["language"]).lower()

repo_text = (
    str(data["name"]) + " " +
    str(data["description"]) + " " +
    str(data["language"])
).lower()

matched_skill_names = []
matched_skills = 0

for skill in skills_list:
    if skill in repo_text:
        matched_skills += 1
        matched_skill_names.append(skill)

match_score = int((matched_skills / len(skills_list)) * 100)
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
print("Matched Skills:")
if matched_skill_names:
    for skill in matched_skill_names:
        print("✓", skill)
else:
    print("No matching skills found")
print("Match Score:", match_score, "%")
print("Repository:", data["name"])
print("Language:", data["language"])
print("Stars:", data["stargazers_count"])
print("Description:", data["description"])
print("Open Issues:", data["open_issues_count"])