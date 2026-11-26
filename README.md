# Employee Management System (EMS)

A full-stack Employee Management System developed using **React.js, Python, FastAPI, SQLAlchemy and SQLite**. This application provides a centralized platform for managing employees, departments, attendance, leave applications and organizational reports.

## 🚀 Features

### 1. Authentication
- User registration and login.
- JWT-based authentication.
- Password hashing using bcrypt.
- Current-user profile endpoint.
- Admin, HR and Employee roles.

### 2. Employee Management
- Add new employees.
- View employee records.
- Update employee information.
- Delete employee records.
- Search and filter employees.
- Pagination.
- Department assignment.
- Employment status tracking.

### 3. Department Management
- Create and manage departments.
- View department information.
- Update department details.
- Delete departments.
- Department-wise employee organization.

### 4. Attendance Management
- Employee check-in and check-out.
- Daily attendance records.
- Personal attendance history.
- Admin and HR attendance overview.

### 5. Leave Management
- Submit leave applications.
- Select leave type and date range.
- View leave application history.
- Cancel pending applications.
- HR/Admin approval and rejection.
- Leave status tracking.

### 6. Reports and Analytics
- Employee statistics.
- Department-wise employee distribution.
- Attendance reports.
- Leave status reports.
- Date-based filtering.
- CSV report exports.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Build Tool | Vite |
| Backend | Python |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Authentication | JWT |
| Password Security | bcrypt |
| API Communication | Axios |
| Charts | Recharts |
| Icons | Lucide React |
| API Documentation | Swagger UI |
| Version Control | Git and GitHub |

## 🏗️ Application Architecture

The application follows a three-layer architecture.

```text
                 USER
                   |
                   v
          REACT.JS FRONTEND
          - Pages and Components
          - React Router
          - Axios API Client
                   |
                   v
               REST APIs
                   |
                   v
           PYTHON + FASTAPI
           - API Routes
           - Request Validation
           - Business Logic
           - Authentication
                   |
                   v
              SQLALCHEMY
                   |
                   v
               SQLITE DB
           - Users
           - Employees
           - Departments
           - Attendance
           - Leaves
```

### How the Application Works

1. Users interact with the React.js frontend.
2. Axios sends HTTP requests to the FastAPI backend.
3. FastAPI receives and validates incoming data using Pydantic schemas.
4. Backend logic processes the requested operation.
5. SQLAlchemy communicates with the SQLite database.
6. FastAPI returns a JSON response.
7. React.js updates the user interface based on the response.

## 📁 Project Structure

```text
employee-management-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── employees.py
│   │   │   ├── departments.py
│   │   │   ├── attendance.py
│   │   │   ├── leaves.py
│   │   │   └── reports.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── config1.py
│   │   │   ├── dependencies.py
│   │   │   ├── limiter.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── employee.py
│   │   │   ├── department.py
│   │   │   ├── attendance.py
│   │   │   └── leave.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── employee.py
│   │   │   ├── department.py
│   │   │   ├── attendance.py
│   │   │   └── leave.py
│   │   │
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Employees.jsx
│   │   │   ├── Departments.jsx
│   │   │   ├── Attendance.jsx
│   │   │   ├── Leave.jsx
│   │   │   └── Reports.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.12 or later
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd employee-management-system
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python3 -m venv ../.venv
```

Activate the virtual environment on Linux/macOS:

```bash
source ../.venv/bin/activate
```

On Windows:

```powershell
..\.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables according to your backend configuration.

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend URL:

http://localhost:8000

Swagger API documentation:

http://localhost:8000/docs

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Frontend URL:

http://localhost:5173

## 🔗 API Documentation

Base URL:

```text
http://localhost:8000
```

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a user |
| POST | `/api/v1/auth/login` | Authenticate a user |
| GET | `/api/v1/auth/me` | Get current user profile |

### Employee APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/employees/` | Create employee |
| GET | `/api/v1/employees/` | List employees |
| GET | `/api/v1/employees/{employee_id}` | Get employee details |
| PUT | `/api/v1/employees/{employee_id}` | Update employee |
| DELETE | `/api/v1/employees/{employee_id}` | Delete employee |

The employee listing endpoint supports search, filtering and pagination.

### Department APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/departments/` | Create department |
| GET | `/api/v1/departments/` | List departments |
| GET | `/api/v1/departments/{department_id}` | Get department |
| PUT | `/api/v1/departments/{department_id}` | Update department |
| DELETE | `/api/v1/departments/{department_id}` | Delete department |

### Attendance APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/attendance/check-in` | Employee check-in |
| POST | `/api/v1/attendance/check-out` | Employee check-out |
| GET | `/api/v1/attendance/me` | View personal attendance |
| GET | `/api/v1/attendance/` | View all attendance records |

### Leave APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/leaves/` | Apply for leave |
| GET | `/api/v1/leaves/me` | View personal leave history |
| PATCH | `/api/v1/leaves/{leave_id}/cancel` | Cancel pending leave |
| GET | `/api/v1/leaves/` | View all leave applications |
| PATCH | `/api/v1/leaves/{leave_id}/review` | Approve or reject leave |

### Reports APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/reports/overview` | Employee and department overview |
| GET | `/api/v1/reports/attendance` | Attendance report |
| GET | `/api/v1/reports/leaves` | Leave report |

For request body schemas, query parameters and response formats, refer to Swagger UI.

## 🗄️ Database

The application uses SQLite for local data storage and SQLAlchemy as the Object Relational Mapper (ORM).

The main database entities include:

- **Users:** User login information and roles.
- **Employees:** Employee personal and professional information.
- **Departments:** Department details.
- **Attendance:** Employee attendance records.
- **Leaves:** Employee leave applications and approval information.

SQLAlchemy models define the database structure, while Pydantic schemas validate API input and output.

## 🔐 Security

The application includes:

- JWT-based authentication.
- Password hashing using bcrypt.
- Role checks on selected protected API routes.
- Protected frontend routes.
- Authorization headers through Axios interceptors.
- Login rate limiting.

### Production Considerations

- Store secret keys and credentials in environment variables.
- Restrict CORS to trusted origins.
- Apply authorization checks to every sensitive endpoint.
- Avoid publishing real employee information or database files.
- Use database migrations for schema changes.
- Consider PostgreSQL for production deployment.

## 🔮 Future Enhancements

- Forgot password and email verification.
- Employee self-service portal.
- Advanced analytics dashboard.
- PDF report generation.
- Email notifications.
- Payroll management.
- Docker-based deployment.
- PostgreSQL production database.
- Automated backend and frontend testing.

## 👨‍💻 Author

**Om Ugale**

- LinkedIn: https://linkedin.com/in/om-ugale-235243267
- GitHub: Add your GitHub profile URL

## 📄 License

This project is developed for educational and portfolio purposes. An appropriate open-source license can be added before distributing the project publicly.