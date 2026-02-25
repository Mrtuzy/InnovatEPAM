# InnovatEPAM Portal - Quick Start Guide

Innovation management system where users can register, submit ideas, and administrators can evaluate submissions.

**Current Status**: Phase 1 MVP Complete ✅
- ✅ User Registration & Authentication
- ✅ JWT Token Management
- ✅ Role-Based Access Control (Submitter/Admin)
- ✅ Protected Routes
- ✅ 115 Automated Tests (69 unit + 46 integration)

---

## 🚀 Quick Start

### En Basit Yöntem - Tek Tıkla Başlat

Çift tıklayın:
```
start.bat
```
İki ayrı terminal açılacak ve her iki sunucu da başlayacak! 🎉

**Veya ayrı ayrı:**
- `start-backend-simple.bat` - Sadece Backend
- `start-frontend-simple.bat` - Sadece Frontend

**✅ Frontend**: `http://localhost:3000`  
**✅ Backend API**: `http://localhost:8000`  
**📚 API Docs**: `http://localhost:8000/docs`

---

### Manuel Terminal Komutları

İki terminal penceresi açın ve aşağıdaki komutları çalıştırın:

**Terminal 1 - Backend:**
```cmd
cd backend
.venv\Scripts\activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```cmd
cd frontend
npm run dev
```

> **İlk çalıştırmada**: Backend için `pip install -r requirements.txt` ve `alembic upgrade head`, Frontend için `npm install` komutlarını çalıştırın.

---

### Otomatik Kurulum (PowerShell - İsteğe Bağlı)

PowerShell scriptleri ile otomatik kurulum yapabilirsiniz:

```powershell
# İlk kurulum
.\setup.ps1

# Sunucuları başlat (menü)
.\start.ps1

# Veya ayrı ayrı
.\start-backend.ps1    # Backend only
.\start-frontend.ps1   # Frontend only
.\run-tests.ps1        # Test çalıştır
```

---

### Manual Setup (Advanced)

<details>
<summary>Click to expand manual setup steps</summary>

#### Step 1: Backend Setup & Start

```powershell
# Navigate to backend directory
cd C:\Yazılım\InnovatEPAM\backend

# Activate virtual environment
& "C:\Yazılım\InnovatEPAM Portal\.venv\Scripts\Activate.ps1"

# Install dependencies (first time only)
# Option A: Using Poetry (recommended)
poetry install

# Option B: Using pip + requirements.txt
pip install -r requirements.txt

# Create database (first time only - see Database Setup below)
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload --port 8000
```

**✅ Backend running at**: `http://localhost:8000`  
**📚 API Docs**: `http://localhost:8000/docs`

#### Step 2: Frontend Setup & Start

```powershell
# Open NEW terminal
cd C:\Yazılım\InnovatEPAM\frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**✅ Frontend running at**: `http://localhost:3000`

#### Step 3: Test It!

1. Open browser: **http://localhost:3000**
2. Click "Register" → Create account
3. View Dashboard → You're in!

</details>

---

## 📋 First Time Setup

### 1. Environment Files

**Backend** - Create `backend/.env`:
```env
DATABASE_URL=sqlite:///./innovatepam.db
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ENVIRONMENT=development
DEBUG=True
```

**Frontend** - Create `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Dependency Management

The backend supports both **Poetry** (modern) and **pip** (traditional):

**Option A: Poetry (Recommended)**
```powershell
cd backend
poetry install  # Installs from pyproject.toml
```

**Option B: pip + requirements.txt**
```powershell
cd backend
pip install -r requirements.txt  # Installs from requirements.txt
```

> **Note**: The `setup.ps1` script automatically detects which method to use. Poetry is preferred if available, otherwise falls back to pip.

### 3. Database Setup

**Option A: SQLite (Quick & Easy)**
```powershell
cd backend
alembic upgrade head
# Database file created automatically at ./innovatepam.db
```

**Option B: PostgreSQL (Production)**
```powershell
# Create database
psql -U postgres
CREATE DATABASE innovatepam;
\q

# Update backend/.env:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/innovatepam

# Run migrations
cd backend
alembic upgrade head
```

---

## 🧪 Running Tests

### En Basit - Tek Komut

```cmd
test.bat
```
Tüm testleri çalıştırır ve sonuçları gösterir.

### Manuel Test Komutları

**All Tests (115 tests)**
```cmd
cd backend
.venv\Scripts\activate
pytest
```

**Specific Test Suites**
```cmd
# Unit tests only (69 tests)
pytest tests/unit/ -v

# Integration tests only (46 tests)
pytest tests/integration/ -v

# With coverage
pytest --cov=src --cov-report=html
# Open: htmlcov/index.html
```

### Frontend E2E Tests
```cmd
cd frontend
npm run test:e2e        # Run E2E tests
npm run test:e2e:ui     # Interactive mode
```

---

## 🎯 Using the Application

### Manual Testing Flow

1. **Register**: http://localhost:3000/register
   - Email: test@example.com
   - Password: Test1234! (needs uppercase, lowercase, digit, special)
   - Full Name: Test User

2. **Dashboard**: Automatically redirected after registration
   - View your profile
   - See role: "submitter"

3. **Logout**: Click logout button

4. **Login**: http://localhost:3000/login
   - Use same credentials

5. **API Testing**: http://localhost:8000/docs
   - Try endpoints in Swagger UI

---

## 🔧 Troubleshooting

### Backend Won't Start

**Port 8000 in use?**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Virtual environment not activated?**
```powershell
& "C:\Yazılım\InnovatEPAM Portal\.venv\Scripts\Activate.ps1"
```

**Missing dependencies?**
```powershell
pip install -r requirements.txt
```

### Frontend Won't Start

**Port 3000 in use?**
```powershell
# Use different port
npm run dev -- --port 3001
```

**API not reachable?**
- Check backend is running on port 8000
- Verify `VITE_API_BASE_URL` in frontend/.env

**Changes not reflecting?**
```powershell
rm -r node_modules/.vite
npm run dev
```

---

## 📦 Project Structure

```
InnovatEPAM/
├── backend/
│   ├── src/
│   │   ├── api/          # API endpoints (auth)
│   │   ├── models/       # User model
│   │   ├── services/     # AuthService
│   │   ├── repositories/ # UserRepository
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── utils/        # JWT, password hasher
│   │   └── config/       # Settings, database
│   ├── tests/
│   │   ├── unit/         # 69 tests ✅
│   │   └── integration/  # 46 tests ✅
│   └── .env              # Configure this!
│
├── frontend/
│   ├── src/
│   │   ├── components/   # LoginForm, RegistrationForm
│   │   ├── pages/        # LoginPage, DashboardPage
│   │   ├── contexts/     # AuthContext
│   │   └── routes.tsx    # Route configuration
│   └── .env              # Configure this!
│
└── specs/                # Design documents
```

---

## 📚 API Endpoints

All endpoints at: `http://localhost:8000/api/v1/auth/`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register new user | ❌ |
| POST | `/login` | Login with credentials | ❌ |
| POST | `/logout` | Logout user | ✅ |
| POST | `/refresh` | Refresh access token | ✅ |
| GET | `/me` | Get current user profile | ✅ |

**Test via Swagger**: http://localhost:8000/docs

---

## 🛠️ Development Commands

### Backend
```powershell
cd backend
& "C:\Yazılım\InnovatEPAM Portal\.venv\Scripts\Activate.ps1"

# Start server
uvicorn src.main:app --reload

# Run tests
pytest

# Create migration
alembic revision --autogenerate -m "message"

# Apply migrations
alembic upgrade head
```

### Frontend
```powershell
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm run test         # Unit tests
npm run test:e2e     # E2E tests

# Code quality
npm run lint         # Check linting
npm run format       # Format code
```

---

## 🔐 Authentication

- **JWT Tokens**: 15-minute access, 7-day refresh
- **Password Requirements**: 8+ chars, uppercase, lowercase, digit, special
- **Default Role**: submitter (for new registrations)
- **Protected Routes**: Require authentication
- **Auto Refresh**: Token refreshed on 401 response

---

## ✅ What's Implemented

### Backend (100% Complete)
- ✅ User model with validation
- ✅ Authentication service
- ✅ 5 API endpoints (register, login, logout, refresh, me)
- ✅ JWT token management (15min/7day)
- ✅ bcrypt password hashing (12 rounds)
- ✅ Role-based access control
- ✅ 69 unit tests
- ✅ 46 integration tests

### Frontend (100% Complete)
- ✅ Registration form with validation
- ✅ Login form
- ✅ Dashboard page
- ✅ Protected routes
- ✅ useAuth hook with logout
- ✅ Automatic token refresh
- ✅ Role-based UI

---

## 📖 Next Steps

**Phase 1**: ✅ User Authentication (Complete)  
**Phase 2**: ⏳ Idea Submission  
**Phase 3**: ⏳ Idea Discovery  
**Phase 4**: ⏳ Admin Evaluation

---

## 📝 Additional Resources

- **Validation Report**: `VALIDATION_REPORT.md`
- **Technical Specs**: `specs/001-portal-mvp/`
- **API Documentation**: http://localhost:8000/docs (when running)
- **Test Files**: `backend/tests/` and `frontend/tests/`

---

## 🆘 Need Help?

1. **Backend issues**: Check http://localhost:8000/docs
2. **Frontend issues**: Check browser console (F12)
3. **Database issues**: Check `.env` DATABASE_URL
4. **Test failures**: Run `pytest -v` for details

---

**Ready to start! 🚀**

Just run backend → run frontend → open browser at http://localhost:3000
