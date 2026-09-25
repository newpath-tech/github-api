import os
import asyncio
import httpx
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GitHub Project Metrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

GITHUB_QUERY = """
query getStudentRepos($username: String!) {
  user(login: $username) {
    repositories(first: 50, isFork: false, privacy: PUBLIC, orderBy: {field: UPDATED_AT, direction: DESC}) {
      totalCount
      nodes {
        name
        stargazerCount
        primaryLanguage {
          name
        }
        object(expression: "HEAD:") {
          ... on Tree {
            entries {
              name
            }
          }
        }
      }
    }
  }
}
"""

async def fetch_github_metrics(client: httpx.AsyncClient, username: str):
    if not GITHUB_TOKEN:
        return {"error": "GITHUB_TOKEN environment variable is not set."}

    headers = {
        "Authorization": f"bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "FastAPI-App"
    }

    try:
        resp = await client.post(
            GITHUB_GRAPHQL_URL,
            json={"query": GITHUB_QUERY, "variables": {"username": username}},
            headers=headers,
            timeout=5.0
        )

        if resp.status_code == 200:
            user_data = resp.json().get("data", {}).get("user")
            if not user_data:
                return {
                    "total_repos_count": 0,
                    "valid_projects_count": 0,
                    "repos": []
                }

            repo_data = user_data.get("repositories", {})
            total_count = repo_data.get("totalCount", 0)
            repos_nodes = repo_data.get("nodes", [])
            
            valid_repos = []
            ignored_defaults = {"readme.md", "license", "license.txt", ".gitignore"}

            for repo in repos_nodes:
                tree_object = repo.get("object") or {}
                entries = tree_object.get("entries", []) if isinstance(tree_object, dict) else []
                
                file_names = [e["name"].lower() for e in entries]
                total_root_items = len(entries)
                meaningful_files = [f for f in file_names if f not in ignored_defaults]

                # VALIDATION RULE: Root files/folders > 2 OR contains custom code
                is_valid = total_root_items > 2 or len(meaningful_files) > 0

                if is_valid:
                    valid_repos.append({
                        "name": repo["name"],
                        "stars": repo["stargazerCount"],
                        "language": repo.get("primaryLanguage", {}).get("name") if repo.get("primaryLanguage") else "N/A",
                        "root_files_count": total_root_items
                    })

            return {
                "total_repos_count": total_count,
                "valid_projects_count": len(valid_repos),
                "repos": valid_repos
            }
    except Exception as e:
        print(f"GitHub Fetch Error [{username}]: {e}")
        
    return {"total_repos_count": 0, "valid_projects_count": 0, "repos": []}


async def process_single_student(client: httpx.AsyncClient, student: dict):
    github_user = student.get("github")
    gh_data = await fetch_github_metrics(client, github_user)

    return {
        "student_name": student.get("name", github_user),
        "github_username": github_user,
        "github": gh_data,
        "status": "success"
    }


# --- ROUTES ---

@app.get("/{username}")
async def get_single_user_github(username: str):
    async with httpx.AsyncClient() as client:
        data = await fetch_github_metrics(client, username)
        return {
            "github_username": username,
            "github": data
        }


@app.post("/api/batch-students")
async def batch_fetch_students(students: list[dict] = Body(...)):
    if not (1 <= len(students) <= 10):
        raise HTTPException(status_code=400, detail="Batch chunk must contain between 1 and 10 students.")

    async with httpx.AsyncClient() as client:
        tasks = [process_single_student(client, student) for student in students]
        results = await asyncio.gather(*tasks)

    return {"batch_size": len(results), "results": results}