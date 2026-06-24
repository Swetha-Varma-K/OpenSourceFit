import requests
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

def analyze_repository(repo, skill):

    skills_list = [s.strip().lower() for s in skill.split(",")]
    user_text = skill
    model = SentenceTransformer("all-MiniLM-L6-v2")
    url = f"https://api.github.com/repos/{repo}"

    response = requests.get(url)

    if response.status_code != 200:
        return {
        "error": "Repository not found"
      }

    data = response.json()

    difficulty = "Beginner"

    if data["stargazers_count"] > 10000:
        difficulty = "Intermediate"

    if data["stargazers_count"] > 50000:
        difficulty = "Advanced"

    beginner_score = 100

    if data["stargazers_count"] > 10000:
        beginner_score -= 20

    if data["stargazers_count"] > 50000:
        beginner_score -= 30

    if data["open_issues_count"] > 1000:
        beginner_score -= 20

    reasons = []

    if data["stargazers_count"] > 50000:
        reasons.append("✗ High competition")

    if data["open_issues_count"] > 1000:
        reasons.append("✗ Large and complex project")

    if data["description"]:
        reasons.append("✓ Project has documentation")

    print("\n📦", repo)
    print("Difficulty:", difficulty)
    print("Beginner-Friendliness Score:", beginner_score, "/100")

    print("\nWhy:")
    for reason in reasons:
        print(reason)

    print("\nLanguage:", data["language"])
    print("Stars:", data["stargazers_count"])
    print("Description:", data["description"])
    print("Open Issues:", data["open_issues_count"])

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
    print("Matched Skills:")
    if matched_skill_names:
        for skill in matched_skill_names:
            print("✓", skill)
    else:
        print("No matching skills found")
    print("Match Score:", match_score, "%")

    issues_url = f"https://api.github.com/repos/{repo}/issues?per_page=100"
    issues_response = requests.get(issues_url)
    issues_data = issues_response.json()

    beginner_labels = [
        "good first issue",
    "help wanted",
    "good first contribution",
    "beginner",
    "beginner friendly",
    "new contributor"
    ]
    issue_texts = []
    issue_titles = []
    issue_links = []
    issue_labels = []
    recommendations = []

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

            text = issue["title"]

            if issue["body"]:
                text = text + " " + issue["body"]

            issue_texts.append(text)
            issue_titles.append(issue["title"])
            issue_links.append(issue["html_url"])

            labels = []

            for label in issue["labels"]:
                labels.append(label["name"])

            issue_labels.append(labels)

            if recommended_count == 5:
                break

    if not found_issues:
        print("No beginner-friendly issues found.")
        print("Try another repository.")

    if len(issue_texts) > 0:
        user_embedding = model.encode(user_text)
        issue_embeddings = model.encode(issue_texts)
        similarity = cos_sim(
            user_embedding,
            issue_embeddings
        )
        results = []
        for i in range(len(issue_titles)):
            score = similarity[0][i].item()
            results.append((score, issue_titles[i], issue_links[i]))
        results.sort(reverse=True)
        print("\nTop Matches For Your Skills:\n")

        rank = 1

        for score, title, link in results[:5]:
            match_percent = round((score + 1) * 50)

            recommendations.append({
                "title": title,
                "match": match_percent,
                "link": link
            })

            print(str(rank) + ". 🟢 " + str(match_percent) + "% Match")
            print(title)
            print("Why matched:")
            print("✓ Beginner-friendly issue")
            print("View on GitHub:")
            print(link)
            print()

            rank = rank + 1

    return {
        "difficulty": difficulty,
        "beginner_score": beginner_score,
        "language": data["language"],
        "stars": data["stargazers_count"],
        "description": data["description"],
        "open_issues": data["open_issues_count"],
        "recommendations": recommendations
    }

if __name__ == "__main__":
    repo = input("Enter repository (owner/repo): ")
    skill = input("Enter your skill: ")

    analyze_repository(repo, skill)