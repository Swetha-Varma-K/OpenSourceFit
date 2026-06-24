from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded!")

user = "documentation typo fixing"

issue = [
    "docs: fix typos in errorhandling.rst and views.rst",
    "Add OAuth authentication support",
    "Improve database query performance",
    "Recipe for chocolate cake"
]

user_embedding = model.encode(user)
issue_embedding = model.encode(issue)

similarity = cos_sim(
    user_embedding,
    issue_embedding
)

results = []

for i in range(len(issue)):
    score = similarity[0][i].item()
    results.append((score, issue[i]))

results.sort(reverse=True)

print("\nTop Recommendations:\n")

for score, issue_title in results:
    print(issue_title)
    print("Score:", score)
    print()