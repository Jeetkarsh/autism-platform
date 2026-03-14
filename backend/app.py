#!/usr/bin/env python3
"""
Autism Platform Backend - Flask REST API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    return data

# ===== DATA STORE =====

# Daily Tips (age-appropriate)
DAILY_TIPS = [
    {"id": 1, "age_range": "0-3", "title": "Sensory Play Time", "description": "Use textured toys to help your child explore different sensations.", "category": "sensory"},
    {"id": 2, "age_range": "0-3", "title": "Eye Contact Game", "description": "Play peek-a-boo to encourage visual engagement.", "category": "social"},
    {"id": 3, "age_range": "0-3", "title": "Sound Exploration", "description": "Use musical toys to introduce different sounds and rhythms.", "category": "sensory"},
    {"id": 4, "age_range": "3-6", "title": "Emotion Cards", "description": "Use picture cards to help identify and name emotions.", "category": "emotional"},
    {"id": 5, "age_range": "3-6", "title": "Social Story Time", "description": "Create simple social stories about sharing and taking turns.", "category": "social"},
    {"id": 6, "age_range": "3-6", "title": "Routine Visual Support", "description": "Use picture schedules to make daily routines predictable.", "category": "cognitive"},
    {"id": 7, "age_range": "6+", "title": "Conversation Practice", "description": "Role-play different social scenarios to build conversation skills.", "category": "social"},
    {"id": 8, "age_range": "6+", "title": "Self-Advocacy Skills", "description": "Teach your child to express their needs and preferences.", "category": "independence"},
]

# Milestones by age
MILESTONES = [
    {"id": 1, "age_range": "0-3", "area": "social", "title": "Responds to name", "description": "Child turns when name is called"},
    {"id": 2, "age_range": "0-3", "area": "communication", "title": "First words", "description": "Says 1-3 meaningful words"},
    {"id": 3, "age_range": "0-3", "area": "motor", "title": "Points to objects", "description": "Uses finger to point at items of interest"},
    {"id": 4, "age_range": "3-6", "area": "social", "title": "Parallel play", "description": "Plays alongside other children"},
    {"id": 5, "age_range": "3-6", "area": "communication", "title": "Two-word phrases", "description": "Combines words meaningfully"},
    {"id": 6, "age_range": "3-6", "area": "cognitive", "title": "Sorts by color/shape", "description": "Groups objects by category"},
    {"id": 7, "age_range": "6+", "area": "social", "title": "Initiates conversation", "description": "Starts conversations with peers"},
    {"id": 8, "age_range": "6+", "area": "emotional", "title": "Identifies emotions", "description": "Recognizes and names complex emotions"},
]

# Therapist mock data
THERAPISTS = [
    {"id": "t1", "name": "Dr. Priya Sharma", "-specialization": "Child Psychologist", "location": "Mumbai", "experience": "15 years", "rating": 4.8, "languages": ["Hindi", "English", "Marathi"]},
    {"id": "t2", "name": "Dr. Anil Patel", "specialization": "Speech Therapist", "location": "Delhi", "experience": "12 years", "rating": 4.9, "languages": ["Hindi", "English", "Gujarati"]},
    {"id": "t3", "name": "Ms. Kavita Reddy", "specialization": "Occupational Therapist", "location": "Hyderabad", "experience": "10 years", "rating": 4.7, "languages": ["Telugu", "English"]},
    {"id": "t4", "name": "Dr. Sneha Joshi", "specialization": "ABA Therapist", "location": "Pune", "experience": "8 years", "rating": 4.9, "languages": ["Marathi", "English", "Hindi"]},
    {"id": "t5", "name": "Dr. Rajesh Kumar", "specialization": "Child Psychiatrist", "location": "Bangalore", "experience": "20 years", "rating": 4.8, "languages": ["Kannada", "English", "Hindi"]},
]

# Resource Library
RESOURCES = [
    {"id": 1, "type": "article", "title": "Understanding Autism Spectrum", "category": "basics", "read_time": "5 min"},
    {"id": 2, "type": "article", "title": "Early Intervention: Why It Matters", "category": "treatment", "read_time": "7 min"},
    {"id": 3, "type": "video", "title": "Sensory Integration Techniques", "category": "therapy", "duration": "12 min"},
    {"id": 4, "type": "article", "title": "Building Communication Skills", "category": "communication", "read_time": "6 min"},
    {"id": 5, "type": "video", "title": "ABA Therapy Basics for Parents", "category": "treatment", "duration": "15 min"},
    {"id": 6, "type": "article", "title": "School Inclusion: A Guide", "category": "education", "read_time": "8 min"},
]

# Forum Categories
FORUM_CATEGORIES = [
    {"id": "0-3", "name": "0-3 Years", "description": "Parents of toddlers and infants", "icon": "👶"},
    {"id": "3-6", "name": "3-6 Years", "description": "Parents of preschoolers", "icon": "🧒"},
    {"id": "6+", "name": "6+ Years", "description": "Parents of school-age children", "icon": "🎒"},
    {"id": "diagnosis", "name": "Diagnosis Journey", "description": "Sharing experiences and advice", "icon": "🏥"},
    {"id": "therapy", "name": "Therapy & Treatment", "description": "OT, PT, Speech, ABA", "icon": "💊"},
]

# Forum Posts (mock)
FORUM_POSTS = [
    {"id": "p1", "category": "0-3", "title": "Starting therapy - any tips?", "author": "Parent123", "replies": 12, "last_activity": "2h ago"},
    {"id": "p2", "category": "3-6", "title": "Best schools in Bangalore?", "author": "ConcernedParent", "replies": 8, "last_activity": "5h ago"},
    {"id": "p3", "category": "therapy", "title": "Speech therapy progress", "author": "HopefulMom", "replies": 15, "last_activity": "1d ago"},
    {"id": "p4", "category": "diagnosis", "title": "Our diagnosis journey", "author": "NewBeginnings", "replies": 23, "last_activity": "3h ago"},
]

# ===== API ENDPOINTS =====

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

# ==== PARENTS/PROFILES ====

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    profiles = load_json('profiles.json', [])
    return jsonify(profiles)

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    data = request.json
    profiles = load_json('profiles.json', [])
    
    profile = {
        "id": str(uuid.uuid4())[:8],
        "child_name": data.get('child_name'),
        "age": data.get('age'),
        "diagnosis_stage": data.get('diagnosis_stage'),
        "goals": data.get('goals', []),
        "created_at": datetime.now().isoformat()
    }
    
    profiles.append(profile)
    save_json('profiles.json', profiles)
    return jsonify(profile), 201

# ==== DAILY TIPS ====

@app.route('/api/tips')
def get_tips():
    age_range = request.args.get('age_range')
    if age_range:
        tips = [t for t in DAILY_TIPS if t['age_range'] == age_range]
    else:
        tips = DAILY_TIPS
    return jsonify(tips)

# ==== MILESTONES ====

@app.route('/api/milestones')
def get_milestones():
    age_range = request.args.get('age_range')
    if age_range:
        result = [m for m in MILESTONES if m['age_range'] == age_range]
    else:
        result = MILESTONES
    return jsonify(result)

# ==== JOURNAL/PROGRESS ====

@app.route('/api/journal', methods=['GET'])
def get_journal():
    journal = load_json('journal.json', [])
    return jsonify(journal)

@app.route('/api/journal', methods=['POST'])
def create_journal_entry():
    data = request.json
    journal = load_json('journal.json', [])
    
    entry = {
        "id": str(uuid.uuid4())[:8],
        "date": datetime.now().isoformat(),
        "type": data.get('type'),  # milestone, observation, appointment
        "title": data.get('title'),
        "notes": data.get('notes'),
        "mood": data.get('mood')  # happy, neutral, difficult
    }
    
    journal.insert(0, entry)
    save_json('journal.json', journal)
    return jsonify(entry), 201

# ==== APPOINTMENTS ====

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = load_json('appointments.json', [])
    return jsonify(appointments)

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    appointments = load_json('appointments.json', [])
    
    appointment = {
        "id": str(uuid.uuid4())[:8],
        "date": data.get('date'),
        "time": data.get('time'),
        "therapist": data.get('therapist'),
        "type": data.get('type'),
        "notes": data.get('notes', ''),
        "status": "scheduled"
    }
    
    appointments.append(appointment)
    save_json('appointments.json', appointments)
    return jsonify(appointment), 201

# ==== THERAPISTS ====

@app.route('/api/therapists')
def get_therapists():
    location = request.args.get('location')
    specialization = request.args.get('specialization')
    
    result = THERAPISTS
    
    if location:
        result = [t for t in result if location.lower() in t['location'].lower()]
    if specialization:
        result = [t for t in result if specialization.lower() in t.get('specialization', '').lower()]
    
    return jsonify(result)

# ==== RESOURCES ====

@app.route('/api/resources')
def get_resources():
    category = request.args.get('category')
    
    if category:
        result = [r for r in RESOURCES if r['category'] == category]
    else:
        result = RESOURCES
    
    return jsonify(result)

# ==== FORUM ====

@app.route('/api/forum/categories')
def get_forum_categories():
    return jsonify(FORUM_CATEGORIES)

@app.route('/api/forum/posts')
def get_forum_posts():
    category = request.args.get('category')
    
    if category:
        result = [p for p in FORUM_POSTS if p['category'] == category]
    else:
        result = FORUM_POSTS
    
    return jsonify(result)

# ==== SUBSCRIPTION ====

@app.route('/api/subscription/status', methods=['GET'])
def get_subscription_status():
    # Mock - in production would check actual payment status
    return jsonify({
        "tier": "free",
        "expires_at": None,
        "features": {
            "unlimited_profiles": False,
            "advanced_tracking": False,
            "community_access": True,
            "therapist_directory": True,
            "resource_library": True
        }
    })

@app.route('/api/subscription/upgrade', methods=['POST'])
def upgrade_subscription():
    # Mock upgrade - in production would integrate with payment
    return jsonify({
        "success": True,
        "tier": "premium",
        "message": "Subscription upgraded to ₹499/month"
    })

# ===== INIT =====
if __name__ == '__main__':
    ensure_data_dir()
    print("=" * 50)
    print("Autism Platform Backend")
    print("=" * 50)
    print("Running on http://localhost:5000")
    app.run(debug=True, port=5000)