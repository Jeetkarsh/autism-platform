# AutismSaarthi - Autism Support Platform

Parent Education + Community Platform for India

## Tech Stack
- **Backend:** Python Flask
- **Frontend:** React + Vite
- **Design:** Mobile-first, warm blue/green colors

## Features

### 1. Parent Onboarding
- Child profile creation (name, age, diagnosis stage, goals)
- Multiple child support

### 2. Daily Tips
- Age-appropriate activities (0-3, 3-6, 6+ years)
- Categories: sensory, social, emotional, cognitive

### 3. Progress Tracker
- Milestones by age group
- Journal entries (observations, milestones)
- Appointment scheduling

### 4. Community Forum
- Categories: 0-3 years, 3-6 years, 6+ years
- Topic-specific: Diagnosis Journey, Therapy & Treatment

### 5. Resource Library
- Articles and videos
- Categories: basics, treatment, therapy, communication

### 6. Therapist Directory
- List of certified therapists
- Location, specialization, rating
- Mock data for demo

## Running the Project

### Backend (Terminal 1):
```bash
cd autism-platform/backend
python3 app.py
```
Runs on http://localhost:5000

### Frontend (Terminal 2):
```bash
cd autism-platform/frontend
npm run dev
```
Runs on http://localhost:5173

## Structure
```
autism-platform/
├── backend/
│   ├── app.py          # Flask REST API
│   └── data/           # JSON data store
└── frontend/
    ├── src/
    │   ├── App.jsx     # Main React app
    │   └── App.css     # Styles
    └── dist/           # Production build
```

## Subscription
- Free tier: Limited features
- Premium: ₹499/month (unlimited profiles, advanced tracking)