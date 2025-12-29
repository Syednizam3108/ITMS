# Intelligent Traffic Management System - Backend

## FastAPI Backend Server with MongoDB

### Prerequisites

1. **Python 3.10+** (Note: Python 3.14 may show Pydantic warnings)
2. **MongoDB** - See [MONGODB_SETUP.md](MONGODB_SETUP.md) for installation options:
   - Local MongoDB installation
   - MongoDB Atlas (free cloud tier)
   - MongoDB in Docker

### Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure MongoDB connection:
Create a `.env` file:
```
MONGODB_URL=mongodb://localhost:27017
```

### Run the server

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Endpoints

- **GET /**: Welcome message
- **GET /health**: Health check
- **GET /violations**: Get all violations
- **POST /violations**: Create a violation
- **GET /officers**: Get all officers
- **POST /officers**: Create an officer
- **GET /analytics/dashboard**: Dashboard statistics
- **POST /upload/violation**: Upload violation with image

### Database

- **Database**: MongoDB
- **Collections**: `violations`, `officers`
- **Default URL**: `mongodb://localhost:27017`
- **Database Name**: `traffic_management`
