# Agentic AI Tester

A powerful, AI-driven full-stack application designed to automate the testing, debugging, and quality assurance of backend projects. By leveraging the advanced reasoning capabilities of Google's Gemini AI, this tool scans your codebase, generates comprehensive test suites, executes them, and automatically heals broken tests.


## 🚀 Features

*   **Smart Project Ingestion**: Upload your project as a ZIP file or provide a GitHub repository URL. The system automatically handles cloning, extraction, and setup.
*   **Automated Endpoint Scanning**: Intelligently scans your backend code (Python/Node.js) to detect API endpoints, methods, and structures.
*   **AI-Powered Test Generation**: Uses Gemini Pro to generate robust, production-grade `pytest` test suites tailored to your specific API endpoints.
*   **Self-Healing Tests**: When tests fail, the **Self-Healing Agent** analyzes the failure logs and automatically rewrites the test code to fix the issues.
*   **Code Diagnosis**: Provides deep insights and diagnostics for backend errors, helping you pinpoint the root cause of bugs.
*   **Interactive Dashboard**: A modern, responsive React frontend that provides real-time analytics, test history, and visual metrics (success rates, rewards).
*   **Reinforcement Learning**: Incorporates an RL Engine to optimize test generation strategies over time based on execution rewards.
*   **Session Isolation**: Securely handles multiple users with isolated sessions and automatic cleanup.

## 🛠️ Tech Stack

### Frontend
*   **Framework**: React 19 (Vite 7)
*   **Styling**: Tailwind CSS v4
*   **UI Components**: Lucide React, Framer Motion (Animations)
*   **Visualization**: Recharts (Analytics Charts)
*   **Routing**: React Router DOM
*   **HTTP Client**: Axios

### Backend
*   **Framework**: FastAPI (Python)
*   **Server**: Uvicorn
*   **AI Model**: Google Generative AI (Gemini 2.5 Pro)
*   **Testing Framework**: Pytest
*   **Utilities**: GitPython (Repo cloning), Pydantic (Validation)

### AI Agents
*   **Scanner**: Parses codebase for structure.
*   **Generator**: Creates test cases.
*   **Executor**: Runs tests and captures output.
*   **Healer**: Fixes broken tests and diagnoses code.
*   **RL Engine**: Optimizes performance.

## 📂 Project Structure

```
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── agents/           # AI Agents (Generator, Healer, etc.)
│   │   ├── main.py           # API Entry Point
│   │   └── ...
│   ├── storage/              # Session & Data Storage
│   ├── requirements.txt      # Python Dependencies
│   └── run_backend.bat       # Startup Script
├── Frontend/                 # React Frontend
│   ├── src/
│   │   ├── components/       # UI Components
│   │   ├── pages/            # App Pages (Dashboard, Upload, etc.)
│   │   └── ...
│   ├── package.json          # Node Dependencies
│   └── vite.config.js        # Vite Config
└── README.md                 # Project Documentation
```

## ⚡ Getting Started

### Prerequisites
*   **Python**: 3.9+ installed and added to PATH.
*   **Node.js**: v16+ (for Frontend).
*   **Gemini API Key**: A valid API key from Google AI Studio.

### 1. Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create a Virtual Environment (Optional but Recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment:
    Create a `.env` file in the `backend` folder and add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

5.  Run the Server:
    ```bash
    # Using the provided script
    run_backend.bat
    
    # OR manually
    uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
    ```
    The backend will start at `http://localhost:5000`.

### 2. Frontend Setup

1.  Open a new terminal and navigate to the `Frontend` directory:
    ```bash
    cd Frontend
    ```

2.  Install Dependencies:
    ```bash
    npm install
    ```

3.  Start Development Server:
    ```bash
    npm run dev
    ```
    The frontend will launch at `http://localhost:5173` (or similar).

## 📖 Usage Guide

1.  **Login**: Access the web interface. You can use a default login if not configured tightly (default: guest).
2.  **Upload Project**:
    *   Go to **Project Upload**.
    *   Upload a `.zip` file of your backend source code OR paste a **GitHub Repository URL**.
    *   Click "Clone & Scan" or "Upload".
3.  **Generate Tests**:
    *   Navigate to **Test Generator**.
    *   Review the scanned endpoints.
    *   Click **Generate Test Suite**. The AI will generate `test_<project>.py`.
4.  **Run Tests**:
    *   Go to **Test Runner**.
    *   Click **Run Tests**.
    *   View real-time logs and results (Pass/Fail).
5.  **Heal/Debug**:
    *   If tests fail, use the **Heal Test** feature to let AI fix the test file.
    *   Use **Diagnose** to analyze backend logic errors.
6.  **Analyze**: Check **Dashboard** and **Analytics** for historical data and trends.

## 🔌 API Endpoints (Backend)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/upload` | Upload a project ZIP file. |
| `POST` | `/process-github` | Clone and process a GitHub repo. |
| `POST` | `/generate-tests` | Generate a test suite using AI. |
| `POST` | `/run-tests` | Execute the generated tests. |
| `POST` | `/heal-test` | AI self-healing for failed tests. |
| `POST` | `/diagnose-code` | detailed code diagnosis for bugs. |
| `GET` | `/dashboard-stats` | Get aggregated stats for the dashboard. |
| `GET` | `/history` | Get run history for the user. |

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
