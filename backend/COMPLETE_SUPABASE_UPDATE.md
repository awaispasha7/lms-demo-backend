# Complete Supabase Integration

## ✅ What's Done

1. ✅ SQL schema created (`supabase_schema.sql`)
2. ✅ Supabase client initialized in server.js
3. ✅ Seed function updated to insert into Supabase
4. ✅ Package.json updated with @supabase/supabase-js

## 🔄 What Needs to Be Updated

All endpoints need to be converted from in-memory to Supabase. Here are the patterns:

### GET Endpoints - Convert to Supabase

**Example: Get all assignments**
```javascript
// OLD:
app.get('/api/teacher/assignments', (req, res) => {
  res.json(assignments);
});

// NEW:
app.get('/api/teacher/assignments', async (req, res) => {
  const { data: assignments, error } = await supabase
    .from('assignments')
    .select('*')
    .order('created_at', { ascending: false });
  
  if (error) {
    return res.status(500).json({ error: error.message });
  }
  
  // Get submissions for stats
  const { data: allSubmissions } = await supabase
    .from('submissions')
    .select('*');
  
  const assignmentsWithStats = assignments.map(assignment => {
    const assignmentSubmissions = allSubmissions.filter(s => s.assignment_id === assignment.id);
    return {
      ...assignment,
      dueDate: assignment.due_date,
      createdAt: assignment.created_at,
      totalSubmissions: assignmentSubmissions.length,
      gradedCount: assignmentSubmissions.filter(s => s.status === 'graded').length,
      pendingCount: assignmentSubmissions.filter(s => s.status === 'pending').length,
    };
  });
  
  res.json(assignmentsWithStats);
});
```

### POST Endpoints - Convert to Supabase

**Example: Create assignment**
```javascript
// OLD:
assignments.push(assignment);
res.json(assignment);

// NEW:
const { data, error } = await supabase
  .from('assignments')
  .insert([{
    title,
    description,
    questions: questions.map((q, idx) => ({
      ...q,
      questionNumber: idx + 1,
    })),
    due_date: dueDate,
    created_at: new Date().toISOString(),
  }])
  .select()
  .single();

if (error) {
  return res.status(500).json({ error: error.message });
}

// Transform back to API format
const result = {
  ...data,
  dueDate: data.due_date,
  createdAt: data.created_at,
};
res.json(result);
```

### Field Name Conversions

When reading from DB → API:
- `due_date` → `dueDate`
- `created_at` → `createdAt`
- `assignment_id` → `assignmentId`
- `student_name` → `studentName`
- `ai_score` → `aiScore`
- `final_score` → `finalScore`
- `final_grade` → `finalGrade`
- `teacher_notes` → `teacherNotes`
- `submitted_at` → `submittedAt`
- `graded_at` → `gradedAt`
- `finalized_at` → `finalizedAt`

When writing to DB from API:
- Reverse the above conversions

## Next Steps

1. Run the SQL schema in Supabase
2. Update all GET endpoints to fetch from Supabase
3. Update all POST/PUT endpoints to insert/update in Supabase
4. Test each endpoint
5. Deploy

The seed function is already done - it will populate your database on first run!

