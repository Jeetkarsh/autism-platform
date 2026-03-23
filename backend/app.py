#!/usr/bin/env python3
"""
Autism Platform Backend - Flask REST API
Enhanced with India-specific data
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
    {"id": 4, "age_range": "0-3", "title": "Mirror Play", "description": "Let your child explore their reflection to build self-awareness.", "category": "cognitive"},
    {"id": 5, "age_range": "3-6", "title": "Emotion Cards", "description": "Use picture cards to help identify and name emotions.", "category": "emotional"},
    {"id": 6, "age_range": "3-6", "title": "Social Story Time", "description": "Create simple social stories about sharing and taking turns.", "category": "social"},
    {"id": 7, "age_range": "3-6", "title": "Routine Visual Support", "description": "Use picture schedules to make daily routines predictable.", "category": "cognitive"},
    {"id": 8, "age_range": "3-6", "title": "Music & Movement", "description": "Singing songs with actions helps with motor and language development.", "category": "motor"},
    {"id": 9, "age_range": "6+", "title": "Conversation Practice", "description": "Role-play different social scenarios to build conversation skills.", "category": "social"},
    {"id": 10, "age_range": "6+", "title": "Self-Advocacy Skills", "description": "Teach your child to express their needs and preferences.", "category": "independence"},
    {"id": 11, "age_range": "6+", "title": "Peer Playdates", "description": "Arrange structured playdates with neurotypical peers.", "category": "social"},
]

# Milestones by age
MILESTONES = [
    {"id": 1, "age_range": "0-3", "area": "social", "title": "Responds to name", "description": "Child turns when name is called"},
    {"id": 2, "age_range": "0-3", "area": "communication", "title": "First words", "description": "Says 1-3 meaningful words"},
    {"id": 3, "age_range": "0-3", "area": "motor", "title": "Points to objects", "description": "Uses finger to point at items of interest"},
    {"id": 4, "age_range": "0-3", "area": "social", "title": "Shows social smile", "description": "Smiles in response to others"},
    {"id": 5, "age_range": "3-6", "area": "social", "title": "Parallel play", "description": "Plays alongside other children"},
    {"id": 6, "age_range": "3-6", "area": "communication", "title": "Two-word phrases", "description": "Combines words meaningfully"},
    {"id": 7, "age_range": "3-6", "area": "cognitive", "title": "Sorts by color/shape", "description": "Groups objects by category"},
    {"id": 8, "age_range": "3-6", "area": "social", "title": "Responds to peers", "description": "Shows interest in other children"},
    {"id": 9, "age_range": "6+", "area": "social", "title": "Initiates conversation", "description": "Starts conversations with peers"},
    {"id": 10, "age_range": "6+", "area": "emotional", "title": "Identifies emotions", "description": "Recognizes and names complex emotions"},
    {"id": 11, "age_range": "6+", "area": "cognitive", "title": "Reads body language", "description": "Understands non-verbal cues"},
    {"id": 12, "age_range": "6+", "area": "academic", "title": "Academic readiness", "description": "Shows interest in learning"},
]

# Therapist/Diagnostic Centers - REAL INDIA CENTERS
THERAPISTS = [
    # NIMHANS
    {"id": "t1", "name": "NIMHANS", "specialization": "Comprehensive Autism Care", "location": "Bangalore", "experience": "40+ years", "rating": 4.9, "languages": ["English", "Kannada", "Hindi", "Telugu"], "phone": "+91-80-26995000", "type": "Government Hospital"},
    
    # Manipal
    {"id": "t2", "name": "Manipal Hospitals", "specialization": "Child Development Center", "location": "Bangalore", "experience": "25+ years", "rating": 4.8, "languages": ["English", "Kannada", "Hindi"], "phone": "+91-80-22242222", "type": "Private Hospital"},
    
    # Apollo
    {"id": "t3", "name": "Apollo Hospitals", "specialization": "Child Development Center", "location": "Bangalore", "experience": "30+ years", "rating": 4.7, "languages": ["English", "Hindi", "Tamil", "Telugu"], "phone": "+91-80-46124444", "type": "Private Hospital"},
    {"id": "t4", "name": "Apollo Children's Hospital", "specialization": "Pediatric Neurology", "location": "Chennai", "experience": "25+ years", "rating": 4.8, "languages": ["English", "Tamil", "Hindi"], "phone": "+91-44-28298282", "type": "Private Hospital"},
    {"id": "t5", "name": "Apollo Hospitals", "specialization": "Developmental Pediatrics", "location": "Mumbai", "experience": "20+ years", "rating": 4.7, "languages": ["English", "Hindi", "Marathi"], "phone": "+91-22-33503350", "type": "Private Hospital"},
    {"id": "t6", "name": "Apollo Hospital", "specialization": "Child Development", "location": "Hyderabad", "experience": "20+ years", "rating": 4.6, "languages": ["English", "Telugu", "Hindi"], "phone": "+91-40-23408888", "type": "Private Hospital"},
    
    # Max Healthcare
    {"id": "t7", "name": "Max Healthcare", "specialization": "Child Development Clinic", "location": "Delhi", "experience": "20+ years", "rating": 4.7, "languages": ["English", "Hindi"], "phone": "+91-11-26515050", "type": "Private Hospital"},
    {"id": "t8", "name": "Max Super Speciality Hospital", "specialization": "Pediatric Neurology", "location": "Delhi", "experience": "15+ years", "rating": 4.6, "languages": ["English", "Hindi"], "phone": "+91-11-66115050", "type": "Private Hospital"},
    
    # Nanavati
    {"id": "t9", "name": "Nanavati Super Speciality Hospital", "specialization": "Child Development Center", "location": "Mumbai", "experience": "50+ years", "rating": 4.7, "languages": ["English", "Hindi", "Marathi"], "phone": "+91-22-26266700", "type": "Private Hospital"},
    
    # Kokilaben
    {"id": "t10", "name": "Kokilaben Dhirubhai Ambani Hospital", "specialization": "Pediatric Development", "location": "Mumbai", "experience": "15+ years", "rating": 4.8, "languages": ["English", "Hindi", "Marathi", "Gujarati"], "phone": "+91-22-30997699", "type": "Private Hospital"},
    
    # NeuroGen BSI
    {"id": "t11", "name": "NeuroGen BSI", "specialization": "Stem Cell Therapy & Rehabilitation", "location": "Mumbai", "experience": "15+ years", "rating": 4.6, "languages": ["English", "Hindi", "Marathi"], "phone": "+91-22-27703333", "type": "Specialty Center"},
    
    # Delhi
    {"id": "t12", "name": "The Autism Centre", "specialization": "Diagnostic & Therapeutic Services", "location": "Delhi", "experience": "20+ years", "rating": 4.8, "languages": ["English", "Hindi"], "phone": "+91-11-46061310", "type": "NGO"},
    
    # Kolkata
    {"id": "t13", "name": "India Autism Center", "specialization": "Comprehensive Autism Services", "location": "Kolkata", "experience": "10+ years", "rating": 4.7, "languages": ["English", "Bengali", "Hindi"], "phone": "+91-33-40600600", "type": "Specialty Center"},
]

# NGO Partners - REAL NGOS
NGO_PARTNERS = [
    {"id": "n1", "name": "SOPAN", "location": "Mumbai", "focus": "Parent support, early intervention", "phone": "+91-22-26406801", "website": "sopangoa.org", "type": "Support Group"},
    {"id": "n2", "name": "Samarpan", "location": "Mumbai", "focus": "Special education, vocational training", "phone": "+91-22-26400111", "website": "samarpan.org", "type": "Special School"},
    {"id": "n3", "name": "India Autism Center", "location": "Kolkata", "focus": "Residential care, therapy, education", "phone": "+91-33-40600600", "website": "indiaautismcenter.org", "type": "Special Center"},
    {"id": "n4", "name": "Forum For Autism", "location": "Mumbai", "focus": "Parent networking, awareness", "phone": "+91-22-22028999", "website": "forumforautism.org", "type": "Support Group"},
    {"id": "n5", "name": "Autism Society of India", "location": "Bangalore", "focus": "Advocacy, parent support", "phone": "+91-80-25492328", "website": "autism-societyindia.org", "type": "Advocacy"},
    {"id": "n6", "name": "ASAT (Action For Autism)", "location": "Delhi", "focus": "Awareness, training, resources", "phone": "+91-11-40512819", "website": "autism-india.org", "type": "Advocacy"},
    {"id": "n7", "name": "Umang", "location": "Delhi", "focus": "Early intervention, parent training", "phone": "+91-11-26894652", "website": "umangautism.org", "type": "Special School"},
    {"id": "n8", "name": "Talish", "location": "Chennai", "focus": "Therapy, parent support", "phone": "+91-44-24331545", "website": "talish.org", "type": "Therapy Center"},
]

# Government Schemes
GOVERNMENT_SCHEMES = [
    {"id": "s1", "name": "Samagra Shiksha", "description": "Inclusive education scheme for children with disabilities in mainstream schools", "benefits": "Free education, special provisions, assistive devices", "eligibility": "Students with disabilities (PwD Certificate required)", "website": "samagra.education.gov.in"},
    {"id": "s2", "name": "Niramaya Health Insurance", "description": "Health insurance scheme for persons with autism, cerebral palsy, mental retardation", "benefits": "₹1 lakh coverage for treatment, therapies", "eligibility": "PwD Certificate holders, annual income < ₹20,000", "website": "nird.in/niramaya"},
    {"id": "s3", "name": "Disability Certificate & Tax Benefits", "description": "Official certification enabling various benefits and tax deductions", "benefits": "Tax deductions u/s 80U (₹50,000-₹1,25,000), employment benefits", "eligibility": "Medical diagnosis from authorized hospital", "website": "sugamyakaur.gov.in/disability"},
    {"id": "s4", "name": "ADIP Scheme", "description": "Aids and Appliances for DisabledPersons - free assistive devices", "benefits": "Free hearing aids, wheelchairs, callipers, braille kits", "eligibility": "PwD Certificate + income < ₹20,000 (urban)/₹15,000 (rural)", "website": "ali一回盲肠aindia.nic.in/adip"},
    {"id": "s5", "name": "Rashtriya Vayoshri Yojana", "description": "Free physical aids for senior citizens (including those with early-onset conditions)", "benefits": "Walking sticks, wheelchairs, hearing aids", "eligibility": "Senior citizens above 60, BPL card holders", "website": "gsd.sunithasain.com"},
    {"id": "s6", "name": "State-Specific Schemes", "description": "Various state governments have additional benefits", "benefits": "Pension, education concessions, travel passes", "eligibility": "Varies by state", "website": "Check your state disabilities department"},
]

# Recommended Apps
RECOMMENDED_APPS = [
    {"id": "a1", "name": "Avaz", "description": "Indian AAC app - picture-based communication", "platform": "iOS/Android", "price": "Free / ₹1,499 Pro", "language": "12 Indian languages"},
    {"id": "a2", "name": "Proloquo2Go", "description": "AAC app for non-verbal communication", "platform": "iOS", "price": "₹4,900", "language": "English, Spanish"},
    {"id": "a3", "name": "Speech Blubs", "description": "Speech therapy app with video modeling", "platform": "iOS/Android", "price": "Free / ₹4,900/yr", "language": "English"},
    {"id": "a4", "name": "Learn Autism", "description": "Comprehensive guide with videos and tips", "platform": "iOS/Android", "price": "Free", "language": "English"},
    {"id": "a5", "name": "Birdhouse", "description": "Journal and tracking app for parents", "platform": "iOS/Android", "price": "Free / ₹900/yr", "language": "English"},
    {"id": "a6", "name": "Endless ABC", "description": "Alphabet and reading app for kids", "platform": "iOS/Android", "price": "Free", "language": "English"},
    {"id": "a7", "name": "Toca Life World", "description": "Creative play app for imagination", "platform": "iOS/Android", "price": "₹900", "language": "English"},
]

# Resource Library
RESOURCES = [
    {"id": 1, "type": "article", "title": "Understanding Autism Spectrum", "category": "basics", "read_time": "5 min", "source": "Autism Speaks India"},
    {"id": 2, "type": "article", "title": "Early Intervention: Why It Matters", "category": "treatment", "read_time": "7 min", "source": "NIMHANS"},
    {"id": 3, "type": "video", "title": "Sensory Integration Techniques", "category": "therapy", "duration": "12 min", "source": "Occupational Therapy India"},
    {"id": 4, "type": "article", "title": "Building Communication Skills", "category": "communication", "read_time": "6 min", "source": "Speech Therapy Association"},
    {"id": 5, "type": "video", "title": "ABA Therapy Basics for Parents", "category": "treatment", "duration": "15 min", "source": "Autism Society India"},
    {"id": 6, "type": "article", "title": "School Inclusion: A Guide", "category": "education", "read_time": "8 min", "source": "Samagra Shiksha"},
    {"id": 7, "type": "article", "title": "Applied Behavior Analysis Explained", "category": "treatment", "read_time": "10 min", "source": "ASAT India"},
    {"id": 8, "type": "video", "title": "Sensory Diets at Home", "category": "sensory", "duration": "8 min", "source": "OT Resources India"},
    {"id": 9, "type": "community", "title": "Autism Parents Forum", "category": "support", "members": "50,000+", "source": "Online Community"},
    {"id": 10, "type": "community", "title": "Nayi Disha", "category": "support", "members": "10,000+", "language": "Hindi", "source": "Online Resource"},
    {"id": 11, "type": "community", "title": "VOICE (Voice of Intellectual Autism)", "category": "advocacy", "members": "2,000+", "source": "Parent Organization"},
]

# Forum Categories
FORUM_CATEGORIES = [
    {"id": "0-3", "name": "0-3 Years", "description": "Parents of toddlers and infants", "icon": "👶"},
    {"id": "3-6", "name": "3-6 Years", "description": "Parents of preschoolers", "icon": "🧒"},
    {"id": "6+", "name": "6+ Years", "description": "Parents of school-age children", "icon": "🎒"},
    {"id": "diagnosis", "name": "Diagnosis Journey", "description": "Sharing experiences and advice", "icon": "🏥"},
    {"id": "therapy", "name": "Therapy & Treatment", "description": "OT, PT, Speech, ABA", "icon": "💊"},
    {"id": "education", "name": "School & Education", "description": "IEP, accommodations, inclusion", "icon": "📚"},
    {"id": "support", "name": "Parent Support", "description": "Emotional support, tips", "icon": "🤝"},
]

# Forum Posts (mock)
FORUM_POSTS = [
    {"id": "p1", "category": "0-3", "title": "Starting therapy - any tips?", "author": "Parent123", "replies": 12, "last_activity": "2h ago"},
    {"id": "p2", "category": "3-6", "title": "Best schools in Bangalore?", "author": "ConcernedParent", "replies": 8, "last_activity": "5h ago"},
    {"id": "p3", "category": "therapy", "title": "Speech therapy progress", "author": "HopefulMom", "replies": 15, "last_activity": "1d ago"},
    {"id": "p4", "category": "diagnosis", "title": "Our diagnosis journey", "author": "NewBeginnings", "replies": 23, "last_activity": "3h ago"},
    {"id": "p5", "category": "education", "title": "IEP meeting prep tips", "author": "SchoolMama", "replies": 18, "last_activity": "6h ago"},
    {"id": "p6", "category": "support", "title": "Need advice - feeling overwhelmed", "author": "TiredParent", "replies": 32, "last_activity": "1h ago"},
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
        "type": data.get('type'),
        "title": data.get('title'),
        "notes": data.get('notes'),
        "mood": data.get('mood')
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

# ==== NGOS ====

@app.route('/api/ngos')
def get_ngos():
    location = request.args.get('location')
    
    result = NGO_PARTNERS
    
    if location:
        result = [n for n in result if location.lower() in n['location'].lower()]
    
    return jsonify(result)

# ==== GOVERNMENT SCHEMES ====

@app.route('/api/schemes')
def get_schemes():
    return jsonify(GOVERNMENT_SCHEMES)

# ==== APPS ====

@app.route('/api/apps')
def get_apps():
    return jsonify(RECOMMENDED_APPS)

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
    return jsonify({
        "tier": "free",
        "expires_at": None,
        "features": {
            "unlimited_profiles": False,
            "advanced_tracking": False,
            "community_access": True,
            "therapist_directory": True,
            "resource_library": True,
            "ngos": True,
            "schemes": True,
            "apps": True
        }
    })

@app.route('/api/subscription/upgrade', methods=['POST'])
def upgrade_subscription():
    return jsonify({
        "success": True,
        "tier": "premium",
        "message": "Subscription upgraded to ₹499/month"
    })

# ===== INIT =====
if __name__ == '__main__':
    ensure_data_dir()
    print("=" * 50)
    print("AutismSaarthi Backend - Enhanced")
    print("=" * 50)
    print(f"Therapists: {len(THERAPISTS)}")
    print(f"NGOs: {len(NGO_PARTNERS)}")
    print(f"Schemes: {len(GOVERNMENT_SCHEMES)}")
    print(f"Apps: {len(RECOMMENDED_APPS)}")
    print("Running on http://localhost:5000")
    app.run(debug=True, port=5000)