# 💼 HeroJobs – AI-Powered Youth Employment & Career Roadmap Platform

HeroJobs is a fullstack web platform that empowers **students, job seekers, and employers** to connect through skill-based career matching.  
It helps youth explore career paths, manage their skills, and discover relevant job and learning opportunities — while enabling employers to post openings and reach the right candidates.  
This project supports **SDG 8: Decent Work & Economic Growth**.

---

## 🚀 Key Features

### 👤 For Job Seekers
- Create and manage your professional profile  
- Add, edit, and delete skills  
- Upload project or experience summaries  
- Store and update your CV  
- Get personalized job and learning recommendations  

### 🏢 For Employers
- Register as an employer  
- Post and manage jobs  
- Define job requirements (skills, role, experience, etc.)  
- Filter and review candidates  
- Get insights on skill trends  

### 💼 Jobs & Opportunities
- 20+ preloaded job entries  
- Job listing page with advanced filters for:
  - Role / Career track  
  - Location  
  - Job type  

### 🎓 Learning Resources
- Curated list of 20+ upskilling materials  
- Filterable by skill or topic  

### 🧩 Skill-Based Matching Engine
- Matches users’ skills with jobs and learning resources  
- Explains matches clearly (e.g., “Matched by skills: Python, Django”)

### 🖥️ Personalized Dashboards
- **Job Seeker Dashboard:** Profile, Skills, Recommended Jobs & Learning  
- **Employer Dashboard:** Job Management, Candidate Review, Insights  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Django Framework) |
| **Database** | MySQL |
| **Deployment** | Localhost / Web server ready |

---

## ⚙️ Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/tohidrupok/herojob-iiuc-tech-fest-2025.git
cd herojob-iiuc-tech-fest-2025
2. Create a Virtual Environment
Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install --upgrade pip
pip install -r requirements.txt
4. Configure Database
If you’re using MySQL, edit your herojob/settings.py:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'herojob_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
5. Run the Server
python manage.py runserver
Then visit:
👉 http://127.0.0.1:8000/

🔐 Admin Panel
Access the admin dashboard at:
👉 http://127.0.0.1:8000/admin/
Use your superuser credentials to log in.

📂 Project Structure

herojob-iiuc-tech-fest-2025/
├── herojob/                # Main Django project folder
├── apps/                   # Custom apps (users, jobs, etc.)
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── db.sqlite3              # Default DB (can replace with MySQL)
├── requirements.txt        # Dependencies
├── manage.py               # Django entry point
└── README.md               # Project documentation
📈 Future Enhancements
AI-powered job recommendations (using ML models)

Resume parser & skill extractor

Integration with LinkedIn API

Realtime chat between employers & candidates

🤝 Contributors
@tohidrupok
@md.asrafulmolla
@rasheduzzamanrakib
Team Falcon (IIUC Tech Fest 2025)

