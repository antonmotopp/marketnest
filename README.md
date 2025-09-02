# Marketnest

Marketnest is a clone of Marktplaats, designed as an online marketplace where users can buy and sell items. The platform focuses on user trust, simple interactions, and efficient search and ranking mechanisms.

✨ Features

🔐 Authentication – Users can register, log in, and log out.

📢 Advertisements – Users can post, edit, and delete their advertisements.

🔎 Search & Filters – Users can search and filter advertisements by category and recency.

📄 Advertisement Details – Users can view detailed information about an advertisement.

💬 Communication – Users can communicate with other users about products.

🏷️ Status Updates – Users can mark items as reserved or sold.

⭐ Ratings – After transactions, users can rate each other as buyers or sellers.

🗂️ Categories – All advertisements must belong to a category (e.g., electronics, furniture, etc.).

📊 Ranking System – Advertisements are ranked by recency and influenced by user ratings.

🔍 Smart Search – Search prioritizes newer advertisements while also considering user ratings.

🛠️ Tech Stack

Frontend: Html

Backend: Pyhton FastApi

Authentication: JWT


# Git Commit Style Guide

This guide shows the recommended format for commit messages in this project.

## 1. Commit Format

- `<type>` – commit type (required)  
- `<scope>` – module, folder, or feature affected (optional)  
- `<short description>` – concise description **in imperative tense**, max 50 characters  

---

## 2. Commit Types

| Type      | Use case |
|-----------|----------|
| feat      | Adding a new feature |
| fix       | Bug fixes |
| docs      | Documentation changes |
| style     | Code formatting, whitespace, no logic change |
| refactor  | Code changes that neither fix bugs nor add features |
| test      | Adding or modifying tests |
| chore     | Updates to build process, dependencies, config |

---

## 3. Examples

### New feature
feat(auth): add JWT login
### Bug fix
fix(api): handle null server response
### Documentation
docs(readme): update installation instructions
### Tests
test(user): add unit tests for registration
### Refactoring
refactor(database): simplify query logic
### Chore
chore(deps): update npm packages

---

## 4. Rules

1. Short description **≤ 50 characters**  
2. Use **imperative tense** ("Add", "Fix", "Update")  
3. Include scope only if it makes the commit clearer  
4. Avoid vague messages ("Fixed stuff", "Update")  
5. Separate commits for different tasks, don’t mix multiple features in one commit
