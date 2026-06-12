import requests

repo = input("Enter repository (owner/repo): ")
url = f"https://api.github.com/repos/{repo}"

response = requests.get(url)

data = response.json()
issues_url = f"https://api.github.com/repos/{repo}/issues"
issues_response = requests.get(issues_url)
issues_data = issues_response.json()

count = 0

for issue in issues_data:
    if "pull_request" in issue:
        continue

    is_beginner = False
    for label in issue["labels"]:
        if label["name"] == "good first issue":
            is_beginner = True
    if is_beginner:
        print("GOOD FIRST ISSUE FOUND")
        print(issue["title"])
        print(issue["html_url"])
    count = count + 1
    if count == 5:
        break
print("Repository:", data["name"])
print("Language:", data["language"])
print("Stars:", data["stargazers_count"])
print("Description:", data["description"])
print("Open Issues:", data["open_issues_count"])