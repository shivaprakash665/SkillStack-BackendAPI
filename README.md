# 🎯 SkillStack - Learning Progress Tracker

A comprehensive full-stack application for tracking learning goals, study sessions, and skill development. Built with React frontend and Flask backend.

![React](https://img.shields.io/badge/React-18.2+-61DAFB?logo=react)
![Flask](https://img.shields.io/badge/Flask-2.3+-000000?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57?logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-563D7C?logo=bootstrap)

## ✨ Features

### 🎯 Advanced Goal Management
- Create learning goals with detailed descriptions
- Break down goals into subtopics and track progress
- Set deadlines and monitor completion rates
- Visual progress tracking with interactive boards

### 📚 Comprehensive Session Logging
- Log study sessions with duration and detailed notes
- Track time spent on specific subtopics
- View study patterns with analytics
- Daily and weekly progress monitoring

### 📊 Advanced Analytics Dashboard
- Interactive progress charts and statistics
- Study time visualization with charts
- Category breakdown of learning activities
- Real-time progress tracking

### 📜 Certificate Management
- Upload and manage completion certificates
- Secure file storage and retrieval
- Associate certificates with learning achievements

### 🔐 User Authentication
- Secure user registration and login
- Session management
- Protected routes and API endpoints

### 🎨 Modern UI/UX
- Responsive design with Tailwind CSS
- Interactive modals and forms
- Real-time updates and smooth animations
- Mobile-friendly interface

## 🛠️ Tech Stack

### Frontend (`SKILLSTACK-FRONTENDUI`)
- **React 18** with Vite
- **React Router** for navigation
- **Axios** for API communication
- **Bootstrap** for styling
- **Chart.js** for data visualization

### Backend (`SKILLSTACK-BACKENDAPI`)
- **Python Flask** RESTful API
- **SQLite** database with SQLAlchemy
- **JWT** for authentication
- **Flask-CORS** for cross-origin requests
- **File upload** handling for certificates

## 📁 Project Structure

### Frontend Architecture

SKILLSTACK-FRONTENDUI/
├── src/

│ ├── components/

│ │ ├── analytics/ # Dashboard and charts

│ │ │ ├── AnalyticsDashboard.jsx

│ │ │ ├── CategoryBreakdown.jsx

│ │ │ ├── ProgressCharts.jsx

│ │ │ ├── StatsCards.jsx

│ │ │ └── StudyTimeChart.jsx

│ │ ├── auth/ # Authentication components

│ │ │ ├── Login.jsx
│ │ │ └── Register.jsx

│ │ ├── certificates/ # Certificate management

│ │ │ ├── Certificates.jsx

│ │ │ └── CertificateUpload.jsx

│ │ ├── common/ # Shared components

│ │ │ ├── Header.jsx

│ │ │ ├── Home.jsx

│ │ │ ├── LoadingSpinner.jsx

│ │ │ ├── Modal.jsx

│ │ │ └── Sidebar.jsx

│ │ ├── dashboard/ # Main dashboard

│ │ │ ├── Dashboard.css

│ │ │ ├── Dashboard.jsx

│ │ │ └── RecentGoals.jsx

│ │ ├── goals/ # Goal management

│ │ │ ├── AddLearningGoal.jsx

│ │ │ ├── AddSubtopicModal.jsx

│ │ │ ├── LearningGoalCard.jsx

│ │ │ ├── LearningGoalDetail.jsx

│ │ │ ├── LearningGoalList.jsx

│ │ │ ├── NotesModal.jsx

│ │ │ ├── SubtopicBoard.jsx

│ │ │ └── SubtopicCard.jsx

│ │ └── layout/ # Layout components

│ ├── sessions/ # Study session management
│ └── ...


### Backend Architecture

SKILLSTACK-BACKENDAPI/
├── controllers/ # Business logic layer

│ ├── ai_controller.py # AI-powered features

│ ├── auth_controller.py # Authentication logic

│ ├── certificate_controller.py

│ ├── learning_goal_controller.py

│ ├── session_controller.py

│ └── study_log_controller.py

├── models/ # Data models

│ ├── init.py

│ ├── certificate.py

│ ├── db.py # Database configuration

│ ├── learning_goal.py

│ ├── session.py

│ ├── study_log.py

│ └── user.py

├── routes/ # API route definitions
│ ├── auth_routes.py

│ └── learning_routes.py

├── middleware/ # Custom middleware

├── uploads/ # Certificate file storage

├── instance/
│ └── skillstack.db # SQLite database

├── app.py # Flask application entry point

├── config.py # Configuration settings

└── .env # Environment variables


## 🗄️ Database Models

### Core Entities
- **Users** - User accounts and authentication
- **LearningGoals** - Main learning objectives with deadlines
- **Subtopics** - Breakdown of goals into manageable parts
- **StudyLogs** - Individual study sessions with duration and notes
- **Sessions** - User session management
- **Certificates** - Uploaded achievement proofs

## 🚀 Installation & Setup

### Backend Setup
```bash
cd SKILLSTACK-BACKENDAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
python app.py

Backend API: http://localhost:5000
```
###Frontend Setup
```bash
cd SKILLSTACK-FRONTENDUI

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend: http://localhost:5173

📡 API Endpoints
Authentication
POST /api/auth/register - User registration

POST /api/auth/login - User login

POST /api/auth/logout - User logout

Learning Goals
GET /api/goals - Get all goals for user

POST /api/goals - Create new learning goal

GET /api/goals/:id - Get goal details

PUT /api/goals/:id - Update goal

DELETE /api/goals/:id - Delete goal

Study Sessions
POST /api/sessions - Log study session

GET /api/sessions/goal/:goal_id - Get sessions for goal

GET /api/sessions/analytics - Get study analytics

Certificates
POST /api/certificates/upload - Upload certificate

GET /api/certificates - Get user certificates

🎯 Key Features in Detail
Subtopic Management
Break down complex goals into manageable subtopics

Track progress at granular level

Visual board for organizing learning tasks

Advanced Analytics
Study time trends and patterns

Completion rate tracking

Category-based progress analysis

Interactive charts and visualizations


