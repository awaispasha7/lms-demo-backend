# API Endpoints Reference

## General Endpoints

### Health Check
```
GET /api/health
```
Returns server status and timestamp.

**Response:**
```json
{
  "status": "ok",
  "message": "Server is running",
  "timestamp": "2025-01-10T12:00:00.000Z"
}
```

### Server Info
```
GET /api/info
```
Returns server statistics.

**Response:**
```json
{
  "totalAssignments": 5,
  "totalSubmissions": 12,
  "server": "LMS Demo API",
  "version": "1.0.0"
}
```

### Root
```
GET /
```
Returns API information and available endpoints.

---

## Teacher Endpoints

### Get All Assignments
```
GET /api/teacher/assignments
```
Returns all assignments with submission statistics.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Math Quiz",
    "description": "...",
    "questions": [...],
    "totalSubmissions": 5,
    "gradedCount": 3,
    "pendingCount": 2
  }
]
```

### Get Assignment by ID
```
GET /api/teacher/assignments/:id
```
Returns a specific assignment with all details (including correct answers).

### Get All Submissions
```
GET /api/teacher/submissions
```
Returns all submissions across all assignments.

### Get Submission by ID
```
GET /api/teacher/submissions/:id
```
Returns a specific submission with assignment details.

**Response:**
```json
{
  "id": 1,
  "assignmentId": 1,
  "studentName": "John Doe",
  "status": "graded",
  "aiScore": 85,
  "finalScore": 85,
  "finalGrade": "A",
  "answers": [...],
  "assignment": {...}
}
```

### Get Submissions for Assignment
```
GET /api/teacher/assignments/:id/submissions
```
Returns all submissions for a specific assignment.

### Auto-Grade Submissions
```
POST /api/teacher/assignments/:id/auto-grade
```
Auto-grades all pending submissions for an assignment.

### Generate AI Feedback
```
POST /api/teacher/submissions/:id/generate-feedback
```
Generates AI feedback for all questions in a submission.

### Finalize Grade
```
POST /api/teacher/submissions/:id/finalize
Body: { finalScore, finalGrade, teacherNotes }
```
Finalizes the grade for a submission.

### Create Assignment
```
POST /api/teacher/assignments
Body: { title, description, questions, dueDate }
```
Creates a new assignment.

---

## Student Endpoints

### Get All Assignments
```
GET /api/student/assignments
```
Returns all available assignments (without correct answers).

### Get Assignment by ID
```
GET /api/student/assignments/:id
```
Returns a specific assignment (without correct answers).

### Get All Submissions
```
GET /api/student/submissions?studentName=John
```
Returns all submissions, optionally filtered by student name.

### Get Submission by ID
```
GET /api/student/submissions/:id
```
Returns a specific submission.

### Submit Assignment
```
POST /api/student/assignments/:id/submit
Body: { studentName, answers }
```
Submits an assignment.

---

## Example Usage

### Check if server is running
```bash
curl http://localhost:5000/api/health
```

### Get all assignments (teacher)
```bash
curl http://localhost:5000/api/teacher/assignments
```

### Get assignment details
```bash
curl http://localhost:5000/api/teacher/assignments/1
```

### Get all submissions
```bash
curl http://localhost:5000/api/teacher/submissions
```

### Get student's submissions
```bash
curl http://localhost:5000/api/student/submissions?studentName=John
```

---

## Notes

- All endpoints return JSON
- Error responses include `error` field
- IDs are integers
- Dates are ISO 8601 strings
- Server uses in-memory storage (data resets on restart)

