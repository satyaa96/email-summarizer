# 📧 Email Summarizer with Gmail API & Cohere

This project is an intelligent email summarization tool that automatically fetches unread emails from a user's Gmail inbox and generates short, clear summaries using Cohere's large language model.

---

## 🔍 Project Overview

In today's fast-paced world, people receive dozens of emails daily, many of which are long or not urgent. This project was designed to reduce that burden by summarizing unread emails from the last 24 hours into concise, readable bullet points. Users can quickly understand their inbox without going through each email manually.

---

## 🚀 Key Features

- ✅ Authenticates securely with Gmail via OAuth2
- 📥 Fetches unread emails from the last 24 hours
- 🤖 Uses Cohere’s language model to generate natural summaries
- 📤 (In Progress) Option to send summarized content back to the user's inbox
- 🧪 Built for testing productivity automation and NLP applications

---

## 📁 Tech Stack

- **Python** – Main programming language
- **Gmail API** – For reading emails
- **Cohere API** – For AI-based summarization
- **OAuth 2.0** – For secure authentication
- **dotenv** – To manage API keys securely

---

## 💡 Example Use Case

Imagine starting your day and instead of opening 15 different emails, you receive a single summary like this:

1. [Team Standup Notes – Project Orion]
Ankita shared the standup summary. Today's focus is on integrating the front-end with the new API endpoints. You're expected to push the logging feature by EOD.

2. [Client Feedback – Email Summarizer POC]
The client appreciated the fast response time but suggested improving the subject line clarity in summary emails. A meeting is scheduled tomorrow at 11:00 AM to discuss next steps.

3. [HR – Timesheet Reminder]
Friendly reminder to submit your timesheet by 6:00 PM today to avoid any payroll delays.

