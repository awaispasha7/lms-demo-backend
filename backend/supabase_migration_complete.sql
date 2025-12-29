-- ============================================
-- Complete Supabase Migration Script
-- Matches Current Django Implementation
-- Run this in your Supabase SQL Editor
-- ============================================

-- ============================================
-- STEP 1: Create/Update Users Table
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITHOUT TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    phone VARCHAR(20),
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================
-- STEP 2: Create Academics Tables
-- ============================================

-- Schools
CREATE TABLE IF NOT EXISTS schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(254),
    website VARCHAR(200),
    established_year INTEGER CHECK (established_year >= 1800 AND established_year <= 2100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Academic Years
CREATE TABLE IF NOT EXISTS academic_years (
    id SERIAL PRIMARY KEY,
    school_id INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Subjects
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    school_id INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) NOT NULL,
    description TEXT,
    credit_hours NUMERIC(5, 2),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(school_id, code)
);

-- Classes
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    school_id INTEGER NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    academic_year_id INTEGER NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL,
    grade_level INTEGER NOT NULL CHECK (grade_level >= 1 AND grade_level <= 12),
    capacity INTEGER,
    class_teacher_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(school_id, code)
);

-- Student Enrollments
CREATE TABLE IF NOT EXISTS student_enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_obj_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    academic_year_id INTEGER NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    roll_number VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(student_id, class_obj_id, academic_year_id)
);

-- Teacher Subject Classes
CREATE TABLE IF NOT EXISTS teacher_subject_classes (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    class_obj_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    academic_year_id INTEGER NOT NULL REFERENCES academic_years(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(teacher_id, subject_id, class_obj_id, academic_year_id)
);

-- ============================================
-- STEP 3: Update Assignments Table
-- ============================================
-- Drop old columns if they exist
ALTER TABLE IF EXISTS assignments DROP COLUMN IF EXISTS assignment_type;
ALTER TABLE IF EXISTS assignments DROP COLUMN IF EXISTS teacher_subject_class_id;
ALTER TABLE IF EXISTS assignments DROP COLUMN IF EXISTS assigned_date;
ALTER TABLE IF EXISTS assignments DROP COLUMN IF EXISTS allow_late_submission;
ALTER TABLE IF EXISTS assignments DROP COLUMN IF EXISTS total_marks;

-- Add new columns
DO $$ 
BEGIN
    -- Add teacher FK
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'teacher_id'
    ) THEN
        ALTER TABLE assignments ADD COLUMN teacher_id INTEGER REFERENCES users(id) ON DELETE CASCADE;
    END IF;
    
    -- Add class_obj FK
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'class_obj_id'
    ) THEN
        ALTER TABLE assignments ADD COLUMN class_obj_id INTEGER REFERENCES classes(id) ON DELETE CASCADE;
    END IF;
    
    -- Add subject FK
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'subject_id'
    ) THEN
        ALTER TABLE assignments ADD COLUMN subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE;
    END IF;
    
    -- Add max_score
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'max_score'
    ) THEN
        ALTER TABLE assignments ADD COLUMN max_score NUMERIC(10, 2);
    END IF;
    
    -- Update status (don't drop, just ensure it exists)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'status'
    ) THEN
        ALTER TABLE assignments ADD COLUMN status VARCHAR(20) DEFAULT 'DRAFT';
    END IF;
    
    -- Add instructions
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'instructions'
    ) THEN
        ALTER TABLE assignments ADD COLUMN instructions TEXT;
    END IF;
    
    -- Add is_active
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'is_active'
    ) THEN
        ALTER TABLE assignments ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
    END IF;
    
    -- Ensure questions column exists as JSONB
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'assignments' AND column_name = 'questions'
    ) THEN
        ALTER TABLE assignments ADD COLUMN questions JSONB NOT NULL DEFAULT '[]'::jsonb;
    ELSE
        UPDATE assignments SET questions = '[]'::jsonb WHERE questions IS NULL;
        ALTER TABLE assignments ALTER COLUMN questions SET NOT NULL;
    END IF;
    
    -- Update column types
    ALTER TABLE assignments 
        ALTER COLUMN title TYPE VARCHAR(200),
        ALTER COLUMN description TYPE TEXT,
        ALTER COLUMN due_date TYPE TIMESTAMP WITHOUT TIME ZONE,
        ALTER COLUMN created_at SET DEFAULT NOW(),
        ALTER COLUMN updated_at SET DEFAULT NOW();
END $$;

-- ============================================
-- STEP 4: Update Submissions Table
-- ============================================
DO $$ 
BEGIN
    -- Add student FK (keep it, don't drop)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'student_id'
    ) THEN
        ALTER TABLE submissions ADD COLUMN student_id INTEGER REFERENCES users(id) ON DELETE CASCADE;
    END IF;
    
    -- student_name should be nullable (for backward compatibility)
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'student_name'
    ) THEN
        ALTER TABLE submissions ADD COLUMN student_name TEXT;
    ELSE
        ALTER TABLE submissions ALTER COLUMN student_name DROP NOT NULL;
    END IF;
    
    -- Add submission_text
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'submission_text'
    ) THEN
        ALTER TABLE submissions ADD COLUMN submission_text TEXT;
    END IF;
    
    -- Add is_active
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'is_active'
    ) THEN
        ALTER TABLE submissions ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
    END IF;
    
    -- Add created_at
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE submissions ADD COLUMN created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
    END IF;
    
    -- Add updated_at
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'updated_at'
    ) THEN
        ALTER TABLE submissions ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
    END IF;
    
    -- Ensure answers column exists as JSONB
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'submissions' AND column_name = 'answers'
    ) THEN
        ALTER TABLE submissions ADD COLUMN answers JSONB NOT NULL DEFAULT '[]'::jsonb;
    ELSE
        UPDATE submissions SET answers = '[]'::jsonb WHERE answers IS NULL;
        ALTER TABLE submissions ALTER COLUMN answers SET NOT NULL;
    END IF;
    
    -- Update status to match new choices
    ALTER TABLE submissions ALTER COLUMN status TYPE VARCHAR(20);
    
    -- submitted_at should be nullable
    ALTER TABLE submissions ALTER COLUMN submitted_at DROP NOT NULL;
    
    -- Remove old columns that don't exist in new model
    ALTER TABLE submissions DROP COLUMN IF EXISTS ai_graded_at;
    ALTER TABLE submissions DROP COLUMN IF EXISTS graded_by_id;
    ALTER TABLE submissions DROP COLUMN IF EXISTS ai_score;
    ALTER TABLE submissions DROP COLUMN IF EXISTS final_score;
    ALTER TABLE submissions DROP COLUMN IF EXISTS final_grade;
    ALTER TABLE submissions DROP COLUMN IF EXISTS teacher_notes;
    ALTER TABLE submissions DROP COLUMN IF EXISTS graded_at;
    ALTER TABLE submissions DROP COLUMN IF EXISTS finalized_at;
END $$;

-- ============================================
-- STEP 5: Create Grades Table (NEW)
-- ============================================
CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL UNIQUE REFERENCES submissions(id) ON DELETE CASCADE,
    score NUMERIC(10, 2) NOT NULL,
    max_score NUMERIC(10, 2) NOT NULL,
    feedback TEXT,
    graded_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    graded_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    ai_suggested_score NUMERIC(10, 2),
    ai_suggested_feedback TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================
-- STEP 6: Create Attendance Tables
-- ============================================

-- Attendance
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_obj_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PRESENT',
    marked_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    marked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    remarks TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(student_id, class_obj_id, date)
);

-- Attendance Reports
CREATE TABLE IF NOT EXISTS attendance_reports (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_obj_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INTEGER NOT NULL DEFAULT 0,
    present_days INTEGER NOT NULL DEFAULT 0,
    absent_days INTEGER NOT NULL DEFAULT 0,
    late_days INTEGER NOT NULL DEFAULT 0,
    excused_days INTEGER NOT NULL DEFAULT 0,
    attendance_percentage NUMERIC(5, 2) NOT NULL DEFAULT 0,
    generated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================
-- STEP 7: Create Reports Tables
-- ============================================

-- Report Templates
CREATE TABLE IF NOT EXISTS report_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    description TEXT,
    template_config JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES report_templates(id) ON DELETE SET NULL,
    report_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    generated_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    school_id INTEGER REFERENCES schools(id) ON DELETE SET NULL,
    class_obj_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    student_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    filters JSONB DEFAULT '{}'::jsonb,
    data JSONB DEFAULT '{}'::jsonb,
    generated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    file_path VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================
-- STEP 8: Create Policies Tables
-- ============================================

-- Policies
CREATE TABLE IF NOT EXISTS policies (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Policy Violations
CREATE TABLE IF NOT EXISTS policy_violations (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id) ON DELETE SET NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    policy_id INTEGER REFERENCES policies(id) ON DELETE SET NULL,
    violation_type VARCHAR(20) NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    description TEXT NOT NULL,
    reported_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reported_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    resolved BOOLEAN NOT NULL DEFAULT FALSE,
    resolution_notes TEXT,
    resolved_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP WITHOUT TIME ZONE,
    ai_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Behavior Incidents
CREATE TABLE IF NOT EXISTS behavior_incidents (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id) ON DELETE SET NULL,
    student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    incident_type VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(200),
    incident_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    reported_by_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reported_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    witnesses TEXT,
    action_taken TEXT,
    resolved BOOLEAN NOT NULL DEFAULT FALSE,
    ai_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================
-- STEP 9: Create Indexes
-- ============================================
CREATE INDEX IF NOT EXISTS idx_assignments_teacher ON assignments(teacher_id);
CREATE INDEX IF NOT EXISTS idx_assignments_class ON assignments(class_obj_id);
CREATE INDEX IF NOT EXISTS idx_assignments_subject ON assignments(subject_id);
CREATE INDEX IF NOT EXISTS idx_submissions_assignment ON submissions(assignment_id);
CREATE INDEX IF NOT EXISTS idx_submissions_student ON submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
CREATE INDEX IF NOT EXISTS idx_grades_submission ON grades(submission_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_class ON attendance(class_obj_id);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);

-- ============================================
-- STEP 10: Create Updated At Triggers
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at
DO $$ 
DECLARE
    table_name TEXT;
BEGIN
    FOR table_name IN 
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename IN (
            'users', 'schools', 'academic_years', 'subjects', 'classes',
            'student_enrollments', 'teacher_subject_classes', 'assignments',
            'submissions', 'grades', 'attendance', 'attendance_reports',
            'report_templates', 'reports', 'policies', 'policy_violations',
            'behavior_incidents'
        )
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS update_%s_updated_at ON %I', table_name, table_name);
        EXECUTE format('CREATE TRIGGER update_%s_updated_at BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()', table_name, table_name);
    END LOOP;
END $$;

-- ============================================
-- Migration Complete!
-- ============================================

