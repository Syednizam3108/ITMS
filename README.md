# Intelligent Traffic Management System (ITMS)

Advanced AI-powered traffic violation detection system using YOLOv8 for real-time monitoring, automated violation detection, and intelligent traffic management.



```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    ██╗████████╗███╗   ███╗███████╗                            │
│    ██║╚══██╔══╝████╗ ████║██╔════╝                            │
│    ██║   ██║   ██╔████╔██║███████╗                            │
│    ██║   ██║   ██║╚██╔╝██║╚════██║                            │
│    ██║   ██║   ██║ ╚═╝ ██║███████║                            │
│    ╚═╝   ╚═╝   ╚═╝     ╚═╝╚══════╝                            │
│                                                                 │
│    INTELLIGENT TRAFFIC MANAGEMENT SYSTEM                       │
│    Professional Diagrams for Academic Report                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```


## Features

- 🎯 **Helmet & No Helmet Detection** - Real-time detection of helmet violations with 90% accuracy
- 📱 **Mobile Phone Usage Detection** - Identifies drivers using phones while riding (always a violation)
- 🏍️ **Triple Riding Detection** - Detects 3+ riders on motorcycles (overloading violation)
- 🔢 **License Plate Recognition** - Automated license plate extraction and detection
- 🚦 **Motorcycle Detection** - Identifies and tracks motorcycles in traffic
- 🔔 **Real-Time Alerts** - Instant email notifications with penalty slips for critical violations
- 📊 **Analytics Dashboard** - Comprehensive statistics and monitoring metrics

## Tech Stack

### Frontend

- React 18 + TypeScript
- Vite (Build tool)
- TailwindCSS (Styling)
- React Router v6 (Navigation)
- Axios (HTTP client)
- Recharts (Analytics visualization)
- React Icons

### Backend

- FastAPI 0.104.1 (Python web framework)
- Uvicorn (ASGI server)
- MongoDB (Motor async driver)
- Ultralytics YOLOv8 8.0.227 (Object detection)
- PyTorch 2.1.1 (Deep learning)
- OpenCV 4.8.1 (Image processing)
- SendGrid (Email notifications)

### AI/ML

- YOLOv8n (Nano) - Custom trained model
- 90.3% mAP@50 accuracy
- 5,860 training images
- 6 detection classes
- NVIDIA GTX 1650 GPU training

## Model Performance

Our custom-trained YOLOv8n model achieves excellent performance:

| Metric | Score |
|--------|-------|
| **mAP@50** | 90.3% |
| **mAP@50-95** | 63.8% |
| **Precision** | 89.2% |
| **Recall** | 87.3% |

### Detection Classes

| Class | Precision | Recall | mAP@50 |
|-------|-----------|--------|---------|
| Helmet | 81.6% | 82.3% | 87.7% |
| No Helmet | 86.9% | 90.3% | 92.9% |
| Mobile Phone | 85.3% | 81.1% | 84.4% |
| Triple Riding | 94.6% | 93.3% | 96.7% |
| License Plate | 96.7% | 94.4% | 97.3% |
| Motorcycle | 78.5% | 75.5% | 76.8% |

## Installation

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 16.x or higher
- **MongoDB** (Local or Atlas)
- **Git**

### Setup Instructions

**1. Clone the repository**

```bash
git clone https://github.com/S-Rahul-Naik/Intelligent-Traffic-Management-System-ITMS-.git
cd ITMS
```

**2. Backend Setup**

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
cd backend
pip install -r requirements.txt
```

**3. Configure Environment Variables**

Create `backend/.env`:

```env
SENDGRID_API_KEY=your_sendgrid_api_key
SENDER_EMAIL=noreply@itms.gov
MONGODB_URL=mongodb://localhost:27017
```

**4. Frontend Setup**

```bash
cd frontend
npm install
```

## How to Run This Project

### Quick Start (3 Easy Steps)

**Step 1: Start MongoDB**

Make sure MongoDB is running on your system:
- **If using MongoDB Atlas (Cloud)**: No action needed
- **If using Local MongoDB**:
  ```bash
  # Windows
  mongod
  
  # Linux/Mac
  sudo systemctl start mongod
  ```

**Step 2: Start the Backend Server**

Open a terminal in the project root:

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
.venv\Scripts\activate.bat   # Windows CMD
# OR
source .venv/bin/activate    # Linux/Mac

# Navigate to backend and start server
cd backend
uvicorn main:app --reload
```

✅ Backend will start at: **`http://127.0.0.1:8000`**

**Step 3: Start the Frontend**

Open a **new terminal** in the project root:

```bash
# Navigate to frontend
cd frontend

# Start development server
npm run dev
```

✅ Frontend will start at: **`http://localhost:5173`**

### Access the Application

1. **Open your browser** and go to: `http://localhost:5173`
2. **View API Documentation**: `http://127.0.0.1:8000/docs`

### Alternative: Run Using Python Directly

If `uvicorn` command doesn't work:

```bash
cd backend
python main.py
```

---

## Running the Application (Detailed)

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Main Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /violations` - Get all violations
- `POST /violations` - Create a violation
- `POST /upload/violation` - Upload image for detection
- `GET /analytics/dashboard` - Dashboard statistics
- `WebSocket /ws/detect` - Real-time detection stream

## Project Structure

```
ITMS/
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── routers/      # API endpoints
│   │   ├── models.py     # Data models
│   │   ├── database.py   # MongoDB connection
│   │   └── yolo_detector.py  # Detection logic
│   ├── main.py           # App entry point
│   └── requirements.txt
├── frontend/             # React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
├── dataset/              # Training data
│   ├── images/
│   └── labels/
└── runs/                 # Training outputs
    └── detect/
        └── weights/
            └── best.pt   # Trained model
```

## License

This project is for educational and research purposes.

## Acknowledgments

- **Ultralytics YOLOv8** - Object detection framework
- **FastAPI** - Modern Python web framework
- **React** - Frontend library
- **MongoDB** - Database

---

**Built with ❤️ for safer roads**
