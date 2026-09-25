<div align="center">

# 🪐 GITHUB TELEMETRY API

**Next-Generation Serverless Backend for Real-Time Developer Metrics**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python 3.10+](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)

*High-performance, asynchronous GitHub data extraction built for scale.*

---

</div>

## 🚀 Overview

The **GitHub Telemetry API** is a high-speed, serverless backend designed to fetch, analyze, and validate GitHub repository metrics for large batches of students. By leveraging **GitHub's GraphQL API** and **FastAPI's asynchronous engine**, this microservice bypasses standard REST limitations, executing complex queries in milliseconds. 

Engineered specifically for **Vercel Serverless deployment**, it utilizes Personal Access Tokens to guarantee a 5,000 request/hour rate limit, ensuring absolute stability in production environments.

## ✨ Core Features

- ⚡ **Asynchronous Core:** Powered by `httpx` and `asyncio` for non-blocking network requests.
- 🌌 **GraphQL Precision:** Single-query data fetching reduces payload size and eliminates waterfall requests.
- 🧠 **Intelligent Validation Algorithm:** Automatically filters out "noise" (empty repos, forks, boilerplate) by analyzing root directory structures and ignoring default files (`README.md`, `.gitignore`, `LICENSE`).
- ☁️ **Edge-Ready Architecture:** Pre-configured `vercel.json` for seamless, zero-config serverless deployment.
- 🛡️ **CORS Secured:** Fully customizable middleware for secure cross-origin resource sharing.

---

## 📡 API Reference

### 1. Retrieve Single User Telemetry
Fetch validated metrics and repository details for a single developer.

- **Endpoint:** `GET /{username}`
- **Response Time:** `~400ms`

**Example Response:**
```json
{
  "github_username": "yukith1411",
  "github": {
    "total_repos_count": 12,
    "valid_projects_count": 8,
    "repos": [
      {
        "name": "neural-network-visualizer",
        "stars": 42,
        "language": "Python",
        "root_files_count": 5
      }
    ]
  }
}
