# 🎮 Interactive Story Generator

**Interactive Story Generator** is a full-stack application that **generates and suggests story paths in real time** using **OpenAI and LangChain**.  
It allows users to play a *choose-your-own-adventure* style game where the story dynamically evolves based on their choices.

---

## ✨ Overview

Users begin by selecting a story theme. The backend dynamically generates story nodes along with **intelligent next-step suggestions**, enabling real-time branching narratives.

The system supports:
- **AI-powered story generation** using OpenAI + LangChain
- **Mock fallback mode** for reliability and cost control when AI is disabled

---

## 🧠 Key Features

- 🔮 Real-time story path suggestions
- 🧠 AI-driven narrative generation (feature-flag controlled)
- ⚡ Background task processing for story generation
- 🗃️ Database-backed story persistence
- 🌐 Clean REST API design
- 🎨 Smooth, interactive React frontend
- ☁️ Free production deployment

---

## 🏗️ Tech Stack

### Backend
- **FastAPI**
- **LangChain**
- **OpenAI API**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**
- **BackgroundTasks**

### Frontend
- **React**
- **JavaScript**
- **Vite**
- **Axios**
- **React Router**

### Database
- **SQLite** (development / mock mode)
- **PostgreSQL-ready** (production)

---

## 🔄 Architecture Highlights

- **Feature-flagged AI integration** (`USE_OPENAI`)
- **Clean separation of concerns**
- **Asynchronous job handling**
- **Scalable API structure**
- **Environment-based configuration**

---

## 🌐 Live Deployment

### 🚀 Frontend  
🔗 https://fastapi-pro-rq1d.onrender.com/

### 🔧 Backend (API & Swagger Docs)  
🔗 https://fastapi-story-backend.onrender.com/docs 


<img width="609" height="386" alt="image" src="https://github.com/user-attachments/assets/8e24c87f-cd70-4320-9ee5-854d2ec2191b" />
<img width="602" height="438" alt="image" src="https://github.com/user-attachments/assets/9af79ec0-2c5e-4d9b-811e-a026715b4406" />
<img width="574" height="423" alt="image" src="https://github.com/user-attachments/assets/a079414c-479d-49df-b2b6-5d2b969b8b41" />
<img width="536" height="405" alt="image" src="https://github.com/user-attachments/assets/a4c21049-46c6-4f66-9490-72d90609193b" />


