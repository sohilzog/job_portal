# 🧑‍💼 Job Portal – Django Web Application

A full-featured **Job Portal web application** built using **Django**, designed to connect **Job Seekers** and **Employers**, with a powerful **Admin panel** for approvals, monitoring, and notifications.

This project focuses on real-world workflows like user approval, job posting approval, application tracking, email notifications, and role-based dashboards.

---

## 🚀 Features

### 🔐 Authentication & Roles
- Custom user model with **role-based login**
- Roles:
  - Admin
  - Employer
  - Job Seeker
- Admin approval required for Employer & Job Seeker accounts
- Secure password validation and updates

---

### 👨‍💼 Admin Module
- Approve / Disapprove Employers & Job Seekers
- Auto-generated credentials sent via email on approval
- Approve / Reject job postings
- View all jobs and applications
- Admin notifications for:
  - New users
  - New job postings
  - New applications
- Verify / Unverify users
- Update admin email & password

---

### 🏢 Employer Module
- Employer dashboard with:
  - Total jobs
  - Total applicants
- Post, edit, and delete job listings
- View applicants for each job
- Update application status:
  - Viewed
  - Profile Visited
  - Accepted
  - Rejected
- Automatic email & notification to seekers
- Profile management (company details, website, password)

---

### 🧑‍🎓 Job Seeker Module
- Job seeker dashboard with:
  - Job listings
  - Filters (job type, location, posted date)
- Profile completion check before applying
- Upload resume & profile picture
- Apply for jobs
- Track application status
- Notifications for:
  - Profile visited
  - Application viewed
  - Accepted / Rejected
- Email alerts for important updates
- Notification preference settings (preferred company/title)

---

### 📧 Notifications & Emails
- Email notifications using Django Email Backend
- In-app notifications for seekers
- Auto notifications when:
  - Profile is visited
  - Application status changes
  - Matching job is posted

---

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySql
- **Authentication**: Django Auth + Custom User Model
- **Email**: SMTP (Gmail / Custom SMTP)
- **Version Control**: Git & GitHub

---


