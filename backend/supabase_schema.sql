-- Supabase Database Schema for LMS Demo
-- Run this in your Supabase SQL Editor

-- Create assignments table
CREATE TABLE IF NOT EXISTS assignments (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  questions JSONB NOT NULL,
  due_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create submissions table
CREATE TABLE IF NOT EXISTS submissions (
  id SERIAL PRIMARY KEY,
  assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
  student_name TEXT NOT NULL,
  answers JSONB NOT NULL,
  status TEXT DEFAULT 'pending',
  ai_score INTEGER,
  final_score INTEGER,
  final_grade TEXT,
  teacher_notes TEXT,
  submitted_at TIMESTAMP DEFAULT NOW(),
  graded_at TIMESTAMP,
  finalized_at TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_submissions_assignment_id ON submissions(assignment_id);
CREATE INDEX IF NOT EXISTS idx_submissions_student_name ON submissions(student_name);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);

-- Enable Row Level Security (RLS) - optional, can be disabled for demo
ALTER TABLE assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations (for demo purposes)
-- In production, you'd want more restrictive policies
CREATE POLICY "Allow all operations on assignments" ON assignments
  FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on submissions" ON submissions
  FOR ALL USING (true) WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at
CREATE TRIGGER update_assignments_updated_at BEFORE UPDATE ON assignments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

