from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import requests

repo = input("Enter repository (owner/repo): ")

issues_url = f"https://api.github.com/repos/{repo}/issues?per_page=10"

response = requests.get(issues_url)

issues_data = response.json()

print("Issues received:", len(issues_data))

model = SentenceTransformer("all-MiniLM-L6-v2")

user = input("Enter your interest: ")
beginner_labels = [
    "good first issue",
    "help wanted"
]

issue_texts = []

for issue in issues_data:

    is_beginner = False

    for label in issue["labels"]:
        if label["name"] in beginner_labels:
            is_beginner = True

    if is_beginner:
        text = issue["title"]

        if issue["body"]:
            text = text + " " + issue["body"]

        issue_texts.append(text)

if issue_texts:
    print(issue_texts[0])
else:
    print("No beginner-friendly issues found.")

print("Beginner-friendly issues:", len(issue_texts))
if len(issue_texts) == 0:
    print("No beginner-friendly issues to rank.")
    exit()
results = []

user_embedding = model.encode(user)
issue_embeddings = model.encode(issue_texts)

similarity = cos_sim(
    user_embedding,
    issue_embeddings
)

for i in range(len(issue_texts)):
    score = similarity[0][i].item()
    results.append((score, issue_texts[i]))

results.sort(reverse=True)

print("\nTop Recommendations:\n")

for score, title in results:
    print(title)
    print("Score:", score)
    print()