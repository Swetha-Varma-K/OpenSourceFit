import requests

repo = input("Enter repository (owner/repo): ")
url = f"https://api.github.com/repos/{repo}"

response = requests.get(url)

data = response.json()

print("Repository:", data["name"])
print("Language:", data["language"])
print("Stars:", data["stargazers_count"])
print("Description:", data["description"])
print("Open Issues:", data["open_issues_count"])