365-Day Special Calendar
Live App: 🌐 https://365calendar-cwerfegrgte3daf3.southeastasia-01.azurewebsites.net

GitHub Repo: 💻 https://github.com/Arulraj25/365-calenda

A beautiful web app that shows a special celebration for every day of the year! Built with Flask + JavaScript, deployed to Azure.

✨ Features
🗓️ Interactive Calendar - Click any date

🎨 Dynamic Animations - Fireworks, hearts, science themes

🔍 Search Function - Find special days

📊 Statistics - Track popular days

📱 Responsive Design - Works on all devices

🎲 Random Day - Discover something new

🚀 Quick Start
bash
# 1. Clone the repo
git clone https://github.com/Arulraj25/365-calenda.git
cd 365-calenda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
python app.py
# Open http://localhost:5000
☁️ Azure Deployment (2 Minutes)
Method 1: One-Click Deploy
https://aka.ms/deploytoazurebutton

Method 2: Manual Steps
Azure Portal → Create "Web App"

Configure:

Name: your-calendar-name

Runtime: Python 3.12

OS: Linux

Region: Southeast Asia

Connect GitHub in Deployment Center

Done! Your app is live at your-calendar-name.azurewebsites.net

📁 Project Structure
text
├── app.py              # Flask backend
├── index.html         # Frontend
├── style.css          # Styling
├── script.js          # Frontend logic
├── requirements.txt   # Python packages
└── startup.sh        # Azure config
🔧 API Examples
javascript
// Get today's special day
fetch('/api/today')

// Search for days
fetch('/api/search?q=chocolate')

// Get random day
fetch('/api/random')
🐳 Docker Support
bash
# Build and run with Docker
docker build -t calendar-app .
docker run -p 5000:5000 calendar-app

# Or use Docker Compose
docker-compose up -d
🛠️ Tech Stack
Backend: Python Flask

Frontend: HTML5, CSS3, JavaScript

Hosting: Azure Web Apps

CI/CD: GitHub Actions

Container: Docker

📊 Built-in Stats
Total views tracking

Most popular days

Category distribution

Real-time updates

🔗 Useful Links
Live Demo: Azure App

Source Code: GitHub

API Docs: /api/health endpoint

Issue Tracker: GitHub Issues

🤝 Contributing
Found a bug? Want a new feature?

Fork the repo

Create a branch

Submit a PR!

📄 License
MIT License - free to use and modify!

👤 Author
Arulraj
GitHub: @Arulraj25
Project: 365-Day Calendar
