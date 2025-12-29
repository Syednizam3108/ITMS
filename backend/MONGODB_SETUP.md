# MongoDB Setup Guide

## Option 1: Install MongoDB Locally (Recommended for Development)

### Windows:
1. Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
2. Run the installer (choose "Complete" installation)
3. Install MongoDB as a Windows Service
4. MongoDB will start automatically on `mongodb://localhost:27017`

### Verify Installation:
```bash
mongod --version
```

## Option 2: Use MongoDB Atlas (Cloud - Free Tier Available)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new cluster (M0 Free tier)
4. Create a database user
5. Get your connection string
6. Update the `.env` file with your MongoDB Atlas connection string:

```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/traffic_management?retryWrites=true&w=majority
```

## Option 3: Use MongoDB in Docker

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## Environment Variables

Create a `.env` file in the backend folder:

```
MONGODB_URL=mongodb://localhost:27017
```

## Start the Backend

Once MongoDB is running:

```bash
cd backend
uvicorn main:app --reload
```

## Default Configuration

If no `MONGODB_URL` is provided, the app defaults to:
- `mongodb://localhost:27017`
- Database name: `traffic_management`
- Collections: `violations`, `officers`
