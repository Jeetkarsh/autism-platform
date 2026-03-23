import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Heart, Baby, BookOpen, Users, Calendar, Video, CreditCard, Plus, ChevronRight, Star, Clock, MessageCircle, Building2, Landmark, Smartphone, Search, MapPin, Phone } from 'lucide-react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Navigation
function Navbar() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', icon: Heart, label: 'Home' },
    { path: '/tips', icon: Star, label: 'Tips' },
    { path: '/tracker', icon: Calendar, label: 'Tracker' },
    { path: '/community', icon: Users, label: 'Forum' },
    { path: '/resources', icon: BookOpen, label: 'Learn' },
    { path: '/therapists', icon: Building2, label: 'Centers' },
    { path: '/ngos', icon: Users, label: 'NGOs' },
    { path: '/schemes', icon: Landmark, label: 'Schemes' },
    { path: '/apps', icon: Smartphone, label: 'Apps' },
  ]
  
  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">
        <Heart className="brand-icon" />
        <span>Autism<span className="brand-accent">Saarthi</span></span>
      </Link>
      <div className="nav-links">
        {navItems.slice(0, 5).map(item => (
          <Link 
            key={item.path} 
            to={item.path} 
            className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <item.icon size={18} />
            <span>{item.label}</span>
          </Link>
        ))}
        {navItems.slice(5).map(item => (
          <Link 
            key={item.path} 
            to={item.path} 
            className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
          >
            <item.icon size={18} />
          </Link>
        ))}
      </div>
    </nav>
  )
}

// Home Page
function Home() {
  const [profiles, setProfiles] = useState([])
  const [showOnboarding, setShowOnboarding] = useState(false)
  const [newProfile, setNewProfile] = useState({ child_name: '', age: '', diagnosis_stage: '', goals: [] })
  
  useEffect(() => {
    fetchProfiles()
  }, [])
  
  const fetchProfiles = async () => {
    try {
      const res = await fetch(`${API_BASE}/profiles`)
      const data = await res.json()
      setProfiles(data)
    } catch (e) {
      console.log('Using demo data')
    }
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE}/profiles`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newProfile)
      })
      const profile = await res.json()
      setProfiles([...profiles, profile])
      setShowOnboarding(false)
    } catch (e) {
      console.error(e)
    }
  }
  
  return (
    <div className="page">
      <header className="hero">
        <h1>Welcome to AutismSaarthi 🌟</h1>
        <p>Your companion in the autism journey</p>
      </header>
      
      {!showOnboarding && profiles.length === 0 && (
        <div className="card onboarding-prompt">
          <Baby size={48} className="icon-primary" />
          <h2>Let's get started</h2>
          <p>Create your child's profile to get personalized support</p>
          <button className="btn btn-primary" onClick={() => setShowOnboarding(true)}>
            <Plus size={18} /> Add Child Profile
          </button>
        </div>
      )}
      
      {showOnboarding && (
        <div className="card">
          <h2>👶 Add Your Child</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label>Child's Name</label>
              <input 
                type="text" 
                value={newProfile.child_name}
                onChange={e => setNewProfile({...newProfile, child_name: e.target.value})}
                placeholder="Enter name"
                required
              />
            </div>
            <div className="form-group">
              <label>Age</label>
              <select 
                value={newProfile.age}
                onChange={e => setNewProfile({...newProfile, age: e.target.value})}
                required
              >
                <option value="">Select age</option>
                <option value="0-3">0-3 years</option>
                <option value="3-6">3-6 years</option>
                <option value="6+">6+ years</option>
              </select>
            </div>
            <div className="form-group">
              <label>Diagnosis Stage</label>
              <select 
                value={newProfile.diagnosis_stage}
                onChange={e => setNewProfile({...newProfile, diagnosis_stage: e.target.value})}
              >
                <option value="">Select stage</option>
                <option value="suspected">Suspected</option>
                <option value="diagnosed">Recently Diagnosed</option>
                <option value="early">Early Intervention</option>
                <option value="ongoing">Ongoing Therapy</option>
              </select>
            </div>
            <div className="form-group">
              <label>Goals (select multiple)</label>
              <div className="checkbox-group">
                {['Communication', 'Social Skills', 'Behavior', 'Motor Skills', 'Academic'].map(goal => (
                  <label key={goal} className="checkbox-label">
                    <input 
                      type="checkbox"
                      checked={newProfile.goals.includes(goal)}
                      onChange={e => {
                        const goals = e.target.checked 
                          ? [...newProfile.goals, goal]
                          : newProfile.goals.filter(g => g !== goal)
                        setNewProfile({...newProfile, goals})
                      }}
                    />
                    {goal}
                  </label>
                ))}
              </div>
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-secondary" onClick={() => setShowOnboarding(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary">Save Profile</button>
            </div>
          </form>
        </div>
      )}
      
      {profiles.length > 0 && (
        <div className="profiles-section">
          <h2>Your Children</h2>
          {profiles.map(profile => (
            <div key={profile.id} className="card profile-card">
              <div className="profile-avatar">
                <Baby size={32} />
              </div>
              <div className="profile-info">
                <h3>{profile.child_name}</h3>
                <span className="badge">{profile.age} years</span>
                <span className="badge badge-secondary">{profile.diagnosis_stage || 'Not specified'}</span>
              </div>
              <ChevronRight className="chevron" />
            </div>
          ))}
          <button className="btn btn-outline" onClick={() => setShowOnboarding(true)}>
            <Plus size={18} /> Add Another Child
          </button>
        </div>
      )}
      
      <div className="quick-links">
        <h2>Quick Access</h2>
        <div className="quick-links-grid">
          <Link to="/therapists" className="quick-link-card">
            <Building2 size={24} />
            <span>Find Centers</span>
          </Link>
          <Link to="/schemes" className="quick-link-card">
            <Landmark size={24} />
            <span>Gov Schemes</span>
          </Link>
          <Link to="/apps" className="quick-link-card">
            <Smartphone size={24} />
            <span>Apps</span>
          </Link>
          <Link to="/ngos" className="quick-link-card">
            <Users size={24} />
            <span>NGOs</span>
          </Link>
        </div>
      </div>
      
      <div className="subscription-banner">
        <CreditCard size={24} />
        <div>
          <h3>Unlock Premium</h3>
          <p>Get unlimited profiles, advanced tracking & more</p>
        </div>
        <span className="price">₹499/mo</span>
      </div>
    </div>
  )
}

// Daily Tips Page
function Tips() {
  const [tips, setTips] = useState([])
  const [ageFilter, setAgeFilter] = useState('all')
  
  useEffect(() => {
    fetchTips()
  }, [ageFilter])
  
  const fetchTips = async () => {
    try {
      const url = ageFilter === 'all' ? `${API_BASE}/tips` : `${API_BASE}/tips?age_range=${ageFilter}`
      const res = await fetch(url)
      const data = await res.json()
      setTips(data)
    } catch (e) {
      setTips([
        {id: 1, age_range: "0-3", title: "Sensory Play Time", description: "Use textured toys to help your child explore different sensations.", category: "sensory"},
        {id: 2, age_range: "3-6", title: "Emotion Cards", description: "Use picture cards to help identify and name emotions.", category: "emotional"},
        {id: 3, age_range: "6+", title: "Conversation Practice", description: "Role-play different social scenarios to build conversation skills.", category: "social"},
      ])
    }
  }
  
  return (
    <div className="page">
      <h1>📋 Daily Tips</h1>
      
      <div className="filter-bar">
        {['all', '0-3', '3-6', '6+'].map(age => (
          <button 
            key={age} 
            className={`chip ${ageFilter === age ? 'active' : ''}`}
            onClick={() => setAgeFilter(age)}
          >
            {age === 'all' ? 'All Ages' : age + ' years'}
          </button>
        ))}
      </div>
      
      <div className="tips-grid">
        {tips.map(tip => (
          <div key={tip.id} className="card tip-card">
            <div className="tip-header">
              <span className="tip-age">{tip.age_range} years</span>
              <span className="tip-category">{tip.category}</span>
            </div>
            <h3>{tip.title}</h3>
            <p>{tip.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// Progress Tracker Page
function Tracker() {
  const [journal, setJournal] = useState([])
  const [milestones, setMilestones] = useState([])
  const [appointments, setAppointments] = useState([])
  const [showEntry, setShowEntry] = useState(false)
  const [newEntry, setNewEntry] = useState({ type: 'observation', title: '', notes: '', mood: 'happy' })
  
  useEffect(() => {
    fetchData()
  }, [])
  
  const fetchData = async () => {
    try {
      const [j, m, a] = await Promise.all([
        fetch(`${API_BASE}/journal`).then(r => r.json()),
        fetch(`${API_BASE}/milestones`).then(r => r.json()),
        fetch(`${API_BASE}/appointments`).then(r => r.json()),
      ])
      setJournal(j)
      setMilestones(m)
      setAppointments(a)
    } catch (e) {
      setMilestones([
        {id: 1, age_range: "0-3", area: "social", title: "Responds to name", description: "Child turns when name is called"},
        {id: 2, age_range: "3-6", area: "social", title: "Parallel play", description: "Plays alongside other children"},
        {id: 3, age_range: "6+", area: "social", title: "Initiates conversation", description: "Starts conversations with peers"},
      ])
      setAppointments([
        {id: "a1", date: "2026-03-20", time: "10:00", therapist: "Dr. Priya Sharma", type: "Speech Therapy"}
      ])
    }
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_BASE}/journal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newEntry)
      })
      const entry = await res.json()
      setJournal([entry, ...journal])
      setShowEntry(false)
      setNewEntry({ type: 'observation', title: '', notes: '', mood: 'happy' })
    } catch (e) {
      console.error(e)
    }
  }
  
  return (
    <div className="page">
      <div className="page-header">
        <h1>📊 Progress Tracker</h1>
        <button className="btn btn-primary" onClick={() => setShowEntry(!showEntry)}>
          <Plus size={18} /> Add Entry
        </button>
      </div>
      
      {showEntry && (
        <div className="card">
          <h2>New Journal Entry</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label>Type</label>
              <select value={newEntry.type} onChange={e => setNewEntry({...newEntry, type: e.target.value})}>
                <option value="observation">Observation</option>
                <option value="milestone">Milestone</option>
                <option value="appointment">Appointment Note</option>
              </select>
            </div>
            <div className="form-group">
              <label>Title</label>
              <input type="text" value={newEntry.title} onChange={e => setNewEntry({...newEntry, title: e.target.value})} required />
            </div>
            <div className="form-group">
              <label>Notes</label>
              <textarea value={newEntry.notes} onChange={e => setNewEntry({...newEntry, notes: e.target.value})} rows={4} />
            </div>
            <div className="form-group">
              <label>Mood</label>
              <div className="mood-selector">
                {['happy', 'neutral', 'difficult'].map(mood => (
                  <button 
                    key={mood}
                    type="button"
                    className={`mood-btn ${newEntry.mood === mood ? 'active' : ''}`}
                    onClick={() => setNewEntry({...newEntry, mood})}
                  >
                    {mood === 'happy' ? '😊' : mood === 'neutral' ? '😐' : '😔'} {mood}
                  </button>
                ))}
              </div>
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-secondary" onClick={() => setShowEntry(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary">Save</button>
            </div>
          </form>
        </div>
      )}
      
      <section>
        <h2>📅 Upcoming Appointments</h2>
        {appointments.length === 0 ? (
          <p className="empty">No appointments scheduled</p>
        ) : (
          appointments.map(apt => (
            <div key={apt.id} className="card appointment-card">
              <div className="apt-date">
                <span className="day">{apt.date?.split('-')[2]}</span>
                <span className="month">{apt.date?.split('-')[1]}</span>
              </div>
              <div className="apt-details">
                <h3>{apt.type}</h3>
                <p>{apt.therapist} • {apt.time}</p>
              </div>
            </div>
          ))
        )}
      </section>
      
      <section>
        <h2>🎯 Milestones</h2>
        <div className="milestones-grid">
          {milestones.map(m => (
            <div key={m.id} className="card milestone-card">
              <span className="milestone-area">{m.area}</span>
              <h3>{m.title}</h3>
              <p>{m.description}</p>
              <span className="milestone-age">{m.age_range}</span>
            </div>
          ))}
        </div>
      </section>
      
      <section>
        <h2>📝 Recent Journal</h2>
        {journal.length === 0 ? (
          <p className="empty">No entries yet</p>
        ) : (
          journal.slice(0, 5).map(entry => (
            <div key={entry.id} className="card journal-card">
              <div className="journal-header">
                <span className="journal-type">{entry.type}</span>
                <span className="journal-date">{new Date(entry.date).toLocaleDateString()}</span>
              </div>
              <h3>{entry.title}</h3>
              <p>{entry.notes}</p>
            </div>
          ))
        )}
      </section>
    </div>
  )
}

// Community Forum Page
function Community() {
  const [categories, setCategories] = useState([])
  const [posts, setPosts] = useState([])
  const [selectedCat, setSelectedCat] = useState(null)
  
  useEffect(() => {
    fetchData()
  }, [])
  
  const fetchData = async () => {
    try {
      const [c, p] = await Promise.all([
        fetch(`${API_BASE}/forum/categories`).then(r => r.json()),
        fetch(`${API_BASE}/forum/posts`).then(r => r.json()),
      ])
      setCategories(c)
      setPosts(p)
    } catch (e) {
      setCategories([
        {id: "0-3", name: "0-3 Years", icon: "👶"},
        {id: "3-6", name: "3-6 Years", icon: "🧒"},
        {id: "6+", name: "6+ Years", icon: "🎒"},
      ])
      setPosts([
        {id: "p1", category: "0-3", title: "Starting therapy tips", author: "Parent123", replies: 12, last_activity: "2h ago"},
        {id: "p2", category: "3-6", title: "Best schools?", author: "ConcernedParent", replies: 8, last_activity: "5h ago"},
      ])
    }
  }
  
  const displayedPosts = selectedCat ? posts.filter(p => p.category === selectedCat) : posts
  
  return (
    <div className="page">
      <h1>💬 Parent Forum</h1>
      
      <div className="categories-scroll">
        <button className={`chip ${!selectedCat ? 'active' : ''}`} onClick={() => setSelectedCat(null)}>All</button>
        {categories.map(cat => (
          <button key={cat.id} className={`chip ${selectedCat === cat.id ? 'active' : ''}`} onClick={() => setSelectedCat(cat.id)}>
            {cat.icon} {cat.name}
          </button>
        ))}
      </div>
      
      <div className="posts-list">
        {displayedPosts.map(post => (
          <div key={post.id} className="card post-card">
            <div className="post-header">
              <span className="post-category">{post.category}</span>
              <span className="post-time">{post.last_activity}</span>
            </div>
            <h3>{post.title}</h3>
            <div className="post-meta">
              <span>👤 {post.author}</span>
              <span>💬 {post.replies} replies</span>
            </div>
          </div>
        ))}
      </div>
      
      <button className="fab">
        <MessageCircle size={24} />
      </button>
    </div>
  )
}

// Resources Page
function Resources() {
  const [resources, setResources] = useState([])
  
  useEffect(() => {
    fetchResources()
  }, [])
  
  const fetchResources = async () => {
    try {
      const res = await fetch(`${API_BASE}/resources`)
      const data = await res.json()
      setResources(data)
    } catch (e) {
      setResources([
        {id: 1, type: "article", title: "Understanding Autism Spectrum", category: "basics", read_time: "5 min"},
        {id: 2, type: "video", title: "Sensory Integration Techniques", category: "therapy", duration: "12 min"},
        {id: 3, type: "community", title: "Autism Parents Forum", category: "support", members: "50,000+"},
      ])
    }
  }
  
  return (
    <div className="page">
      <h1>📚 Learning Resources</h1>
      
      <div className="resources-grid">
        {resources.map(res => (
          <div key={res.id} className="card resource-card">
            <div className="resource-icon">
              {res.type === 'video' ? <Video size={24} /> : res.type === 'community' ? <Users size={24} /> : <BookOpen size={24} />}
            </div>
            <div className="resource-content">
              <span className="resource-type">{res.type}</span>
              <h3>{res.title}</h3>
              <p>{res.read_time || res.duration || res.members}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Therapists/Centers Page
function Therapists() {
  const [therapists, setTherapists] = useState([])
  const [location, setLocation] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  
  useEffect(() => {
    fetchTherapists()
  }, [location])
  
  const fetchTherapists = async () => {
    try {
      const url = location ? `${API_BASE}/therapists?location=${location}` : `${API_BASE}/therapists`
      const res = await fetch(url)
      const data = await res.json()
      setTherapists(data)
    } catch (e) {
      setTherapists([
        {id: "t1", name: "NIMHANS", specialization: "Comprehensive Autism Care", location: "Bangalore", experience: "40+ years", rating: 4.9, phone: "+91-80-26995000", type: "Landmark Hospital"},
        {id: "t2", name: "Manipal Hospitals", specialization: "Child Development Center", location: "Bangalore", experience: "25+ years", rating: 4.8, phone: "+91-80-22242222", type: "Private Hospital"},
      ])
    }
  }
  
  const filtered = therapists.filter(t => 
    t.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    t.specialization.toLowerCase().includes(searchTerm.toLowerCase())
  )
  
  return (
    <div className="page">
      <h1>🏥 Diagnostic & Therapy Centers</h1>
      
      <div className="search-box">
        <Search size={18} />
        <input 
          type="text" 
          placeholder="Search centers..." 
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
      </div>
      
      <div className="filter-bar">
        <button className={`chip ${!location ? 'active' : ''}`} onClick={() => setLocation('')}>All</button>
        {['Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Kolkata', 'Hyderabad'].map(loc => (
          <button key={loc} className={`chip ${location === loc ? 'active' : ''}`} onClick={() => setLocation(loc)}>{loc}</button>
        ))}
      </div>
      
      <div className="therapists-list">
        {filtered.map(t => (
          <div key={t.id} className="card therapist-card">
            <div className="therapist-avatar">{t.name.split(' ').map(n => n[0]).join('')}</div>
            <div className="therapist-info">
              <h3>{t.name}</h3>
              <p className="specialization">{t.specialization}</p>
              <p className="location">📍 {t.location} • {t.experience} • {t.type}</p>
              {t.phone && <p className="phone">📞 {t.phone}</p>}
              <div className="rating">⭐ {t.rating}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// NGOs Page
function NGOs() {
  const [ngos, setNgos] = useState([])
  
  useEffect(() => {
    fetchNgos()
  }, [])
  
  const fetchNgos = async () => {
    try {
      const res = await fetch(`${API_BASE}/ngos`)
      const data = await res.json()
      setNgos(data)
    } catch (e) {
      setNgos([
        {id: "n1", name: "SOPAN", focus: "Parent support, early intervention", location: "Mumbai", phone: "+91-22-26406801"},
        {id: "n2", name: "Samarpan", focus: "Special education, vocational training", location: "Mumbai", phone: "+91-22-26400111"},
      ])
    }
  }
  
  return (
    <div className="page">
      <h1>🤝 NGO Partners</h1>
      
      <div className="ngos-list">
        {ngos.map(ngo => (
          <div key={ngo.id} className="card ngo-card">
            <div className="ngo-header">
              <h3>{ngo.name}</h3>
              <span className="ngo-type">{ngo.type}</span>
            </div>
            <p className="ngo-focus">{ngo.focus}</p>
            <div className="ngo-footer">
              <span>📍 {ngo.location}</span>
              {ngo.phone && <span>📞 {ngo.phone}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Landmark Schemes Page
function Schemes() {
  const [schemes, setSchemes] = useState([])
  
  useEffect(() => {
    fetchSchemes()
  }, [])
  
  const fetchSchemes = async () => {
    try {
      const res = await fetch(`${API_BASE}/schemes`)
      const data = await res.json()
      setSchemes(data)
    } catch (e) {
      setSchemes([
        {id: "s1", name: "Samagra Shiksha", description: "Inclusive education scheme", benefits: "Free education, special provisions", website: "samagra.education.gov.in"},
        {id: "s2", name: "Niramaya", description: "Health insurance forPwD", benefits: "₹1 lakh coverage", website: "nird.in"},
      ])
    }
  }
  
  return (
    <div className="page">
      <h1>🏛️ Landmark Schemes</h1>
      
      <div className="schemes-list">
        {schemes.map(scheme => (
          <div key={scheme.id} className="card scheme-card">
            <div className="scheme-header">
              <Landmark size={24} className="scheme-icon" />
              <h3>{scheme.name}</h3>
            </div>
            <p className="scheme-desc">{scheme.description}</p>
            <div className="scheme-benefits">
              <strong>Benefits:</strong> {scheme.benefits}
            </div>
            <div className="scheme-eligibility">
              <strong>Eligibility:</strong> {scheme.eligibility}
            </div>
            <a href={`https://${scheme.website}`} target="_blank" rel="noopener noreferrer" className="btn btn-outline scheme-website">
              🌐 Visit Website
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}

// Apps Page
function Apps() {
  const [apps, setApps] = useState([])
  
  useEffect(() => {
    fetchApps()
  }, [])
  
  const fetchApps = async () => {
    try {
      const res = await fetch(`${API_BASE}/apps`)
      const data = await res.json()
      setApps(data)
    } catch (e) {
      setApps([
        {id: "a1", name: "Avaz", description: "Indian AAC app", platform: "iOS/Android", price: "Free / ₹1,499 Pro", language: "12 Indian languages"},
        {id: "a2", name: "Proloquo2Go", description: "AAC app for non-verbal", platform: "iOS", price: "₹4,900", language: "English, Spanish"},
      ])
    }
  }
  
  return (
    <div className="page">
      <h1>📱 Recommended Apps</h1>
      
      <div className="apps-grid">
        {apps.map(app => (
          <div key={app.id} className="card app-card">
            <div className="app-icon">
              <Smartphone size={28} />
            </div>
            <div className="app-info">
              <h3>{app.name}</h3>
              <p className="app-desc">{app.description}</p>
              <div className="app-meta">
                <span>📱 {app.platform}</span>
                <span>💰 {app.price}</span>
              </div>
              {app.language && <div className="app-lang">🌐 {app.language}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Main App
function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/tips" element={<Tips />} />
            <Route path="/tracker" element={<Tracker />} />
            <Route path="/community" element={<Community />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/therapists" element={<Therapists />} />
            <Route path="/ngos" element={<NGOs />} />
            <Route path="/schemes" element={<Schemes />} />
            <Route path="/apps" element={<Apps />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App