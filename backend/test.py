import requests

repo = input("Enter repository (owner/repo): ")
url = f"https://api.github.com/repos/{repo}"

response = requests.get(url)

data = response.json()
issues_url = f"https://api.github.com/repos/{repo}/issues"
issues_response = requests.get(issues_url)
issues_data = issues_response.json()

beginner_labels = [
    "good first issue",
    "help wanted"
]
found_issues = False
count = 0

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
        print("Issue:")
        print(issue["title"])

        print("Reason:")
        for reason in reasons:
            print("✓", reason)

        print("Labels:")
        for label in issue["labels"]:
            print(label["name"])

        print("Link:")
        print(issue["html_url"])
    count = count + 1
    if count == 5:
        break

if not found_issues:
    print("No beginner-friendly issues found.")
    print("Try another repository.")

print("Repository:", data["name"])
print("Language:", data["language"])
print("Stars:", data["stargazers_count"])
print("Description:", data["description"])
print("Open Issues:", data["open_issues_count"])