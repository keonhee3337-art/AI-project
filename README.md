# 🤖 MBB Case Consultant Bot (AI-Powered)

**An automated case interview partner that simulates a Senior Partner critique using GPT-4o.**

![Project Status](https://img.shields.io/badge/Status-Prototype-blue)
![Tech Stack](https://img.shields.io/badge/Stack-Python_|_SQL_|_OpenAI-green)

## 💼 The Business Problem
Aspiring consultants spend hundreds of hours practicing case interviews, often relying on peers who lack the experience to provide rigorous, structured feedback. This creates a "blind spot" in preparation where generic frameworks (e.g., "Revenue vs Cost") go unchallenged until the actual interview.

## 🚀 The Solution
I built a **CLI-based AI Agent** that acts as a ruthless "Mock Partner." It does not just chat; it evaluates logical structures against MBB standards (MECE, Hypothesis-Driven).

### Key Features
* **Strategy Engine:** Uses `SQLite` to track user performance data (simulated member engagement).
* **Visualization Module:** Auto-generates trend analysis charts (`Matplotlib`) to diagnose business problems.
* **AI Critique Core:** A custom-prompted OpenAI agent that detects "generic" frameworks and enforces deep segmentation.

---

## 🛠️ Technical Architecture

### 1. Data Layer (SQL)
* **Schema:** relational design (Members -> Events -> Attendance).
* **Logic:** Uses Window Functions (`LAG`) to calculate month-over-month growth momentum.

### 2. Intelligence Layer (Python + OpenAI)
* **System Prompting:** Configured with a "Hostile Partner" persona to prioritize critical feedback over politeness.
* **Security:** API keys managed via `.env` variable injection (Git-secured).

---

## 📸 Demo
*(Please see `demo_screenshot.png` in the repository for a live execution example)*

> "The structure you proposed is overly generic... consider breaking down revenue streams into customer segments." 
> — *Bot Output*

---

## 💻 How to Run This
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/](https://github.com/)keonhee3337-art/AI-project.git