import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || '',
});

// Initialize Supabase
const supabaseUrl = process.env.SUPABASE_URL || 'https://yntmdbalhjgmiyfauaui.supabase.co';
const supabaseKey = process.env.SUPABASE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InludG1kYmFsaGpnbWl5ZmF1YXVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzODIxNjYsImV4cCI6MjA4MDk1ODE2Nn0.xM8gJ0eiiN2hNqcVNYOfCDv3nqQGA5pwGkAmpa1-Mv0';
const supabase = createClient(supabaseUrl, supabaseKey);

console.log('✅ Supabase initialized');

// Seed sample assignments for demo
async function seedAssignments() {
  // Check if assignments already exist
  const { data: existingAssignments } = await supabase
    .from('assignments')
    .select('id')
    .limit(1);
  
  if (existingAssignments && existingAssignments.length > 0) {
    console.log('📚 Assignments already exist in database, skipping seed');
    return;
  }

  const assignmentsToSeed = [];

  // Mathematics Assignment - Calculus
  assignmentsToSeed.push({
    title: 'Calculus I - Derivatives and Applications',
    description: 'This assignment covers fundamental concepts of derivatives, including the power rule, chain rule, and applications to optimization problems.',
    questions: [
      {
        questionNumber: 1,
        questionText: 'What is the derivative of f(x) = x³ + 5x² - 3x + 7?',
        options: [
          '3x² + 10x - 3',
          'x² + 5x - 3',
          '3x² + 5x - 3',
          'x³ + 10x - 3'
        ],
        correctOptions: [0],
        rubric: 'Apply the power rule: d/dx(xⁿ) = nxⁿ⁻¹. For each term, multiply the coefficient by the exponent and reduce the exponent by 1.',
        marks: 2
      },
      {
        questionNumber: 2,
        questionText: 'If f(x) = (x² + 1)⁵, which rule should you use to find the derivative?',
        options: [
          'Power Rule',
          'Chain Rule',
          'Product Rule',
          'Quotient Rule'
        ],
        correctOptions: [1],
        rubric: 'The Chain Rule is used when you have a function inside another function. Here, (x² + 1) is inside the power function.',
        marks: 1
      },
      {
        questionNumber: 3,
        questionText: 'A rectangular box with a square base has a volume of 64 cm³. What is the minimum surface area?',
        options: [
          '64 cm²',
          '96 cm²',
          '128 cm²',
          '192 cm²'
        ],
        correctOptions: [1],
        rubric: 'Set up the optimization problem: V = x²h = 64, so h = 64/x². Surface area S = 2x² + 4xh. Substitute h and find the derivative to minimize.',
        marks: 3
      },
      {
        questionNumber: 4,
        questionText: 'What is the derivative of sin(x) with respect to x?',
        options: [
          'cos(x)',
          '-cos(x)',
          'sin(x)',
          '-sin(x)'
        ],
        correctOptions: [0],
        rubric: 'The derivative of sin(x) is cos(x). This is a fundamental trigonometric derivative that should be memorized.',
        marks: 1
      },
      {
        questionNumber: 5,
        questionText: 'If a function has a local maximum at x = a, what can you say about f\'(a)?',
        options: [
          'f\'(a) > 0',
          'f\'(a) < 0',
          'f\'(a) = 0',
          'f\'(a) is undefined'
        ],
        correctOptions: [2],
        rubric: 'At a local maximum, the derivative is zero (horizontal tangent). This is a critical point where the function changes from increasing to decreasing.',
        marks: 2
      }
    ],
    due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
  });

  // Physics Assignment - Mechanics
  assignmentsToSeed.push({
    title: 'Physics I - Newtonian Mechanics',
    description: 'This assignment covers Newton\'s laws of motion, forces, and energy conservation principles.',
    questions: [
      {
        questionNumber: 1,
        questionText: 'According to Newton\'s First Law, an object at rest will:',
        options: [
          'Accelerate if a force is applied',
          'Remain at rest unless acted upon by a net external force',
          'Move with constant velocity',
          'Always experience friction'
        ],
        correctOptions: [1],
        rubric: 'Newton\'s First Law states that an object at rest stays at rest, and an object in motion stays in motion with constant velocity, unless acted upon by a net external force.',
        marks: 2
      },
      {
        questionNumber: 2,
        questionText: 'A 10 kg block is pushed with a force of 50 N. If the coefficient of friction is 0.3, what is the acceleration? (g = 10 m/s²)',
        options: [
          '2 m/s²',
          '5 m/s²',
          '8 m/s²',
          '10 m/s²'
        ],
        correctOptions: [0],
        rubric: 'Calculate: F_net = F_applied - F_friction = 50 - (0.3 × 10 × 10) = 50 - 30 = 20 N. Then a = F_net/m = 20/10 = 2 m/s².',
        marks: 3
      },
      {
        questionNumber: 3,
        questionText: 'Which of the following is a conservative force?',
        options: [
          'Friction',
          'Air resistance',
          'Gravitational force',
          'Normal force'
        ],
        correctOptions: [2],
        rubric: 'Conservative forces are path-independent and allow for potential energy. Gravity, electric forces, and spring forces are conservative. Friction and air resistance are non-conservative.',
        marks: 2
      },
      {
        questionNumber: 4,
        questionText: 'A ball is thrown upward with initial velocity 20 m/s. What is its velocity at the maximum height?',
        options: [
          '20 m/s upward',
          '0 m/s',
          '20 m/s downward',
          '10 m/s upward'
        ],
        correctOptions: [1],
        rubric: 'At the maximum height, the vertical velocity is zero. The ball momentarily stops before falling back down due to gravity.',
        marks: 2
      },
      {
        questionNumber: 5,
        questionText: 'In a perfectly elastic collision, which quantity is conserved?',
        options: [
          'Only momentum',
          'Only kinetic energy',
          'Both momentum and kinetic energy',
          'Neither momentum nor kinetic energy'
        ],
        correctOptions: [2],
        rubric: 'In a perfectly elastic collision, both momentum and kinetic energy are conserved. This is different from inelastic collisions where only momentum is conserved.',
        marks: 2
      }
    ],
    due_date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
  });

  // Mathematics Assignment - Linear Algebra
  assignmentsToSeed.push({
    title: 'Linear Algebra - Matrix Operations',
    description: 'This assignment covers matrix multiplication, determinants, and solving systems of linear equations.',
    questions: [
      {
        questionNumber: 1,
        questionText: 'What is the determinant of a 2×2 matrix [[a, b], [c, d]]?',
        options: [
          'ad + bc',
          'ad - bc',
          'ab - cd',
          'a + d - b - c'
        ],
        correctOptions: [1],
        rubric: 'For a 2×2 matrix, the determinant is calculated as ad - bc. This is the product of the main diagonal minus the product of the off-diagonal.',
        marks: 2
      },
      {
        questionNumber: 2,
        questionText: 'For matrix multiplication A × B to be defined, what must be true?',
        options: [
          'A and B must have the same dimensions',
          'The number of columns in A must equal the number of rows in B',
          'The number of rows in A must equal the number of columns in B',
          'A and B must be square matrices'
        ],
        correctOptions: [1],
        rubric: 'Matrix multiplication requires that the number of columns in the first matrix equals the number of rows in the second matrix. The resulting matrix has dimensions (rows of A) × (columns of B).',
        marks: 2
      },
      {
        questionNumber: 3,
        questionText: 'A system of linear equations has no solution when:',
        options: [
          'The determinant is zero',
          'The system is consistent',
          'The equations are linearly dependent',
          'The system is inconsistent'
        ],
        correctOptions: [3],
        rubric: 'An inconsistent system has no solution, meaning the equations contradict each other. This can be identified when row reduction leads to a contradiction like 0 = 1.',
        marks: 2
      },
      {
        questionNumber: 4,
        questionText: 'What is the inverse of a matrix A?',
        options: [
          'A matrix B such that A + B = I',
          'A matrix B such that A × B = B × A = I',
          'A matrix B such that A - B = 0',
          'The transpose of A'
        ],
        correctOptions: [1],
        rubric: 'The inverse of matrix A, denoted A⁻¹, is the matrix such that A × A⁻¹ = A⁻¹ × A = I, where I is the identity matrix. Not all matrices have inverses.',
        marks: 2
      },
      {
        questionNumber: 5,
        questionText: 'What does it mean if the determinant of a matrix is zero?',
        options: [
          'The matrix is invertible',
          'The matrix is singular (not invertible)',
          'All entries are zero',
          'The matrix is symmetric'
        ],
        correctOptions: [1],
        rubric: 'A matrix with zero determinant is called singular and does not have an inverse. This occurs when the rows (or columns) are linearly dependent.',
        marks: 2
      }
    ],
    due_date: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
  });

  // Physics Assignment - Electromagnetism
  assignmentsToSeed.push({
    title: 'Physics II - Electric Fields and Potential',
    description: 'This assignment covers electric fields, electric potential, and Gauss\'s law applications.',
    questions: [
      {
        questionNumber: 1,
        questionText: 'What is the direction of the electric field around a positive point charge?',
        options: [
          'Radially inward',
          'Radially outward',
          'Tangential to the charge',
          'No direction (zero field)'
        ],
        correctOptions: [1],
        rubric: 'The electric field around a positive point charge points radially outward, away from the charge. For a negative charge, it points radially inward.',
        marks: 2
      },
      {
        questionNumber: 2,
        questionText: 'Two point charges of +5 μC and -3 μC are separated by 2 meters. What is the magnitude of the force between them? (k = 9 × 10⁹ N⋅m²/C²)',
        options: [
          '33.75 N',
          '67.5 N',
          '135 N',
          '270 N'
        ],
        correctOptions: [0],
        rubric: 'Use Coulomb\'s law: F = k|q₁q₂|/r² = (9×10⁹)(5×10⁻⁶)(3×10⁻⁶)/(2²) = 135×10⁻³/4 = 33.75 N. The force is attractive since charges are opposite.',
        marks: 3
      },
      {
        questionNumber: 3,
        questionText: 'Electric potential is a:',
        options: [
          'Vector quantity',
          'Scalar quantity',
          'Tensor quantity',
          'Dimensionless quantity'
        ],
        correctOptions: [1],
        rubric: 'Electric potential is a scalar quantity, meaning it has magnitude but no direction. This is different from electric field, which is a vector.',
        marks: 2
      },
      {
        questionNumber: 4,
        questionText: 'According to Gauss\'s law, the electric flux through a closed surface depends on:',
        options: [
          'The shape of the surface',
          'The size of the surface',
          'The charge enclosed by the surface',
          'The electric field outside the surface'
        ],
        correctOptions: [2],
        rubric: 'Gauss\'s law states that the electric flux through a closed surface is proportional to the charge enclosed, regardless of the surface shape or size.',
        marks: 2
      },
      {
        questionNumber: 5,
        questionText: 'What happens to the electric potential energy when two like charges are brought closer together?',
        options: [
          'It increases',
          'It decreases',
          'It remains constant',
          'It becomes zero'
        ],
        correctOptions: [0],
        rubric: 'For like charges, bringing them closer together increases the potential energy because work must be done against the repulsive force. The system stores more energy.',
        marks: 2
      }
    ],
    due_date: new Date(Date.now() + 6 * 24 * 60 * 60 * 1000).toISOString(),
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString()
  });

  // Insert all assignments into Supabase
  const { data, error } = await supabase
    .from('assignments')
    .insert(assignmentsToSeed)
    .select();

  if (error) {
    console.error('Error seeding assignments:', error);
  } else {
    console.log(`📝 Seeded ${data.length} assignments into Supabase`);
  }
}

// ============================================
// GENERAL/HEALTH CHECK ROUTES
// ============================================

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'Server is running',
    timestamp: new Date().toISOString()
  });
});

// Get server info
app.get('/api/info', async (req, res) => {
  const { count: assignmentCount } = await supabase
    .from('assignments')
    .select('*', { count: 'exact', head: true });

  const { count: submissionCount } = await supabase
    .from('submissions')
    .select('*', { count: 'exact', head: true });

  res.json({
    totalAssignments: assignmentCount || 0,
    totalSubmissions: submissionCount || 0,
    server: 'LMS Demo API',
    version: '1.0.0',
    storage: 'Supabase'
  });
});

// ============================================
// TEACHER ROUTES
// ============================================

// Get all assignments (teacher view)
app.get('/api/teacher/assignments', async (req, res) => {
  try {
    const { data: assignments, error: assignmentsError } = await supabase
      .from('assignments')
      .select('*')
      .order('created_at', { ascending: false });

    if (assignmentsError) {
      console.error('Error fetching assignments:', assignmentsError);
      return res.status(500).json({ error: assignmentsError.message });
    }

    if (!assignments || assignments.length === 0) {
      return res.json([]);
    }

    const { data: allSubmissions, error: submissionsError } = await supabase
      .from('submissions')
      .select('*');

    if (submissionsError) {
      console.error('Error fetching submissions:', submissionsError);
      // Continue with empty submissions array if error
    }

    const submissions = allSubmissions || [];

    const assignmentsWithStats = assignments.map(assignment => {
      const assignmentSubmissions = submissions.filter(s => s.assignment_id === assignment.id);
      return {
        id: assignment.id,
        title: assignment.title,
        description: assignment.description,
        questions: assignment.questions,
        dueDate: assignment.due_date,
        createdAt: assignment.created_at,
        totalSubmissions: assignmentSubmissions.length,
        gradedCount: assignmentSubmissions.filter(s => s.status === 'graded').length,
        pendingCount: assignmentSubmissions.filter(s => s.status === 'pending').length,
      };
    });

    res.json(assignmentsWithStats);
  } catch (err) {
    console.error('Unexpected error in teacher assignments:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new assignment
app.post('/api/teacher/assignments', async (req, res) => {
  const { title, description, questions, dueDate } = req.body;

  // Validate: All questions must have rubric and answer keys
  const invalidQuestions = questions.filter(
    q => !q.rubric || !q.correctOptions || q.correctOptions.length === 0
  );

  if (invalidQuestions.length > 0) {
    return res.status(400).json({
      error: 'All questions must have rubric and at least one correct answer'
    });
  }

  // Insert into Supabase
  const { data: assignment, error } = await supabase
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

  // Transform to API format
  const result = {
    id: assignment.id,
    title: assignment.title,
    description: assignment.description,
    questions: assignment.questions,
    dueDate: assignment.due_date,
    createdAt: assignment.created_at,
  };

  res.json(result);
});

// Get assignment details
app.get('/api/teacher/assignments/:id', async (req, res) => {
  const assignmentId = parseInt(req.params.id);
  
  const { data: assignment, error } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', assignmentId)
    .single();

  if (error || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }

  // Transform to API format
  const result = {
    id: assignment.id,
    title: assignment.title,
    description: assignment.description,
    questions: assignment.questions,
    dueDate: assignment.due_date,
    createdAt: assignment.created_at,
  };

  res.json(result);
});

// Get submissions for an assignment
app.get('/api/teacher/assignments/:id/submissions', async (req, res) => {
  const assignmentId = parseInt(req.params.id);
  
  const { data: submissions, error } = await supabase
    .from('submissions')
    .select('*')
    .eq('assignment_id', assignmentId)
    .order('submitted_at', { ascending: false });

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  // Transform to API format
  const result = submissions.map(s => ({
    id: s.id,
    assignmentId: s.assignment_id,
    studentName: s.student_name,
    answers: s.answers,
    status: s.status,
    submittedAt: s.submitted_at,
    aiScore: s.ai_score,
    finalScore: s.final_score,
    finalGrade: s.final_grade,
    teacherNotes: s.teacher_notes,
    gradedAt: s.graded_at,
    finalizedAt: s.finalized_at,
  }));

  res.json(result);
});

// Get all submissions (teacher view)
app.get('/api/teacher/submissions', async (req, res) => {
  const { data: submissions, error } = await supabase
    .from('submissions')
    .select('*')
    .order('submitted_at', { ascending: false });

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  // Transform to API format
  const result = submissions.map(s => ({
    id: s.id,
    assignmentId: s.assignment_id,
    studentName: s.student_name,
    answers: s.answers,
    status: s.status,
    submittedAt: s.submitted_at,
    aiScore: s.ai_score,
    finalScore: s.final_score,
    finalGrade: s.final_grade,
    teacherNotes: s.teacher_notes,
    gradedAt: s.graded_at,
    finalizedAt: s.finalized_at,
  }));

  res.json(result);
});

// Get single submission by ID (teacher view)
app.get('/api/teacher/submissions/:id', async (req, res) => {
  const submissionId = parseInt(req.params.id);
  
  const { data: submission, error: submissionError } = await supabase
    .from('submissions')
    .select('*')
    .eq('id', submissionId)
    .single();

  if (submissionError || !submission) {
    return res.status(404).json({ error: 'Submission not found' });
  }
  
  // Get assignment details
  const { data: assignment, error: assignmentError } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', submission.assignment_id)
    .single();

  // Transform to API format
  const result = {
    id: submission.id,
    assignmentId: submission.assignment_id,
    studentName: submission.student_name,
    answers: submission.answers,
    status: submission.status,
    submittedAt: submission.submitted_at,
    aiScore: submission.ai_score,
    finalScore: submission.final_score,
    finalGrade: submission.final_grade,
    teacherNotes: submission.teacher_notes,
    gradedAt: submission.graded_at,
    finalizedAt: submission.finalized_at,
    assignment: assignment ? {
      id: assignment.id,
      title: assignment.title,
      description: assignment.description,
      questions: assignment.questions,
      dueDate: assignment.due_date,
      createdAt: assignment.created_at,
    } : null
  };

  res.json(result);
});

// Auto-grade all submissions
app.post('/api/teacher/assignments/:id/auto-grade', async (req, res) => {
  const assignmentId = parseInt(req.params.id);
  
  // Get assignment
  const { data: assignment, error: assignmentError } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', assignmentId)
    .single();
  
  if (assignmentError || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }

  // Get pending submissions
  const { data: assignmentSubmissions, error: submissionsError } = await supabase
    .from('submissions')
    .select('*')
    .eq('assignment_id', assignmentId)
    .eq('status', 'pending');

  if (submissionsError) {
    return res.status(500).json({ error: submissionsError.message });
  }

  let gradedCount = 0;

  for (const submission of assignmentSubmissions) {
    // Auto-grade
    let totalScore = 0;
    const updatedAnswers = submission.answers.map(answer => {
      const question = assignment.questions.find(q => q.questionNumber === answer.questionNumber);
      if (!question) return answer;
      
      const studentSelected = new Set(answer.selectedOptions);
      const correctOptions = new Set(question.correctOptions);
      
      const isCorrect = JSON.stringify([...studentSelected].sort()) === JSON.stringify([...correctOptions].sort());
      const score = isCorrect ? question.marks : 0;
      totalScore += score;
      
      return {
        ...answer,
        isCorrect,
        score,
      };
    });

    // Update submission in Supabase
    const { error: updateError } = await supabase
      .from('submissions')
      .update({
        answers: updatedAnswers,
        ai_score: totalScore,
        status: 'submitted',
        graded_at: new Date().toISOString(),
      })
      .eq('id', submission.id);

    if (!updateError) {
      gradedCount++;
    }
  }

  res.json({ message: `Auto-graded ${gradedCount} submissions`, gradedCount });
});

// Generate AI feedback for a submission
app.post('/api/teacher/submissions/:id/generate-feedback', async (req, res) => {
  const submissionId = parseInt(req.params.id);
  
  const { data: submission, error: submissionError } = await supabase
    .from('submissions')
    .select('*')
    .eq('id', submissionId)
    .single();

  if (submissionError || !submission) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  const { data: assignment, error: assignmentError } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', submission.assignment_id)
    .single();

  if (assignmentError || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }

  if (!process.env.OPENAI_API_KEY) {
    return res.status(500).json({ error: 'OpenAI API key not configured' });
  }

  let feedbackCount = 0;
  const updatedAnswers = [...submission.answers];

  for (let i = 0; i < updatedAnswers.length; i++) {
    const answer = updatedAnswers[i];
    if (!answer.aiFeedback) {
      const question = assignment.questions.find(q => q.questionNumber === answer.questionNumber);
      
      if (question) {
        try {
          const feedback = await generateEncouragingFeedback(
            question,
            answer.selectedOptions,
            answer.isCorrect
          );
          
          updatedAnswers[i].aiFeedback = feedback;
          updatedAnswers[i].feedbackGeneratedAt = new Date().toISOString();
          feedbackCount++;
        } catch (error) {
          console.error('Error generating feedback:', error);
          updatedAnswers[i].aiFeedback = answer.isCorrect
            ? 'Great job! You got this question correct. Keep up the excellent work!'
            : 'This question needs another look. Review the concepts and try again—you\'ve got this!';
        }
      }
    }
  }

  // Update submission in Supabase
  const { error: updateError } = await supabase
    .from('submissions')
    .update({
      answers: updatedAnswers,
    })
    .eq('id', submissionId);

  if (updateError) {
    return res.status(500).json({ error: updateError.message });
  }

  res.json({ message: `Generated feedback for ${feedbackCount} questions`, feedbackCount });
});

// Finalize grade
app.post('/api/teacher/submissions/:id/finalize', async (req, res) => {
  const submissionId = parseInt(req.params.id);
  
  // Get submission
  const { data: submission, error: getError } = await supabase
    .from('submissions')
    .select('*')
    .eq('id', submissionId)
    .single();

  if (getError || !submission) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  const { finalScore, finalGrade, teacherNotes } = req.body;
  
  // Update submission
  const { data: updatedSubmission, error: updateError } = await supabase
    .from('submissions')
    .update({
      final_score: finalScore || submission.ai_score,
      final_grade: finalGrade,
      teacher_notes: teacherNotes || '',
      status: 'graded',
      finalized_at: new Date().toISOString(),
    })
    .eq('id', submissionId)
    .select()
    .single();

  if (updateError) {
    return res.status(500).json({ error: updateError.message });
  }

  // Transform to API format
  const result = {
    id: updatedSubmission.id,
    assignmentId: updatedSubmission.assignment_id,
    studentName: updatedSubmission.student_name,
    answers: updatedSubmission.answers,
    status: updatedSubmission.status,
    submittedAt: updatedSubmission.submitted_at,
    aiScore: updatedSubmission.ai_score,
    finalScore: updatedSubmission.final_score,
    finalGrade: updatedSubmission.final_grade,
    teacherNotes: updatedSubmission.teacher_notes,
    gradedAt: updatedSubmission.graded_at,
    finalizedAt: updatedSubmission.finalized_at,
  };

  res.json(result);
});

// ============================================
// STUDENT ROUTES
// ============================================

// Get available assignments
app.get('/api/student/assignments', async (req, res) => {
  try {
    const { data: assignments, error } = await supabase
      .from('assignments')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching assignments:', error);
      return res.status(500).json({ error: error.message });
    }

    if (!assignments || assignments.length === 0) {
      return res.json([]);
    }

    // Transform to API format
    const result = assignments.map(a => ({
      id: a.id,
      title: a.title,
      description: a.description,
      dueDate: a.due_date,
      createdAt: a.created_at,
    }));

    res.json(result);
  } catch (err) {
    console.error('Unexpected error in student assignments:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get assignment details
app.get('/api/student/assignments/:id', async (req, res) => {
  const assignmentId = parseInt(req.params.id);
  
  const { data: assignment, error } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', assignmentId)
    .single();

  if (error || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }
  
  // Don't send correct answers to students
  const studentView = {
    id: assignment.id,
    title: assignment.title,
    description: assignment.description,
    dueDate: assignment.due_date,
    createdAt: assignment.created_at,
    questions: assignment.questions.map(q => ({
      questionNumber: q.questionNumber,
      questionText: q.questionText,
      options: q.options,
      marks: q.marks,
    })),
  };
  
  res.json(studentView);
});

// Submit assignment
app.post('/api/student/assignments/:id/submit', async (req, res) => {
  const assignmentId = parseInt(req.params.id);
  
  // Check if assignment exists
  const { data: assignment, error: assignmentError } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', assignmentId)
    .single();
  
  if (assignmentError || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }

  const { studentName, answers } = req.body;

  // Insert submission into Supabase
  const { data: submission, error } = await supabase
    .from('submissions')
    .insert([{
      assignment_id: assignmentId,
      student_name: studentName,
      answers: answers.map(a => ({
        questionNumber: a.questionNumber,
        selectedOptions: a.selectedOptions,
      })),
      status: 'pending',
      submitted_at: new Date().toISOString(),
    }])
    .select()
    .single();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  // Transform to API format
  const result = {
    id: submission.id,
    assignmentId: submission.assignment_id,
    studentName: submission.student_name,
    answers: submission.answers,
    status: submission.status,
    submittedAt: submission.submitted_at,
    aiScore: submission.ai_score,
    finalScore: submission.final_score,
    finalGrade: submission.final_grade,
  };

  res.json(result);
});

// Get student's submission
app.get('/api/student/submissions/:id', async (req, res) => {
  const submissionId = parseInt(req.params.id);
  
  const { data: submission, error } = await supabase
    .from('submissions')
    .select('*')
    .eq('id', submissionId)
    .single();

  if (error || !submission) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  // Transform to API format
  const result = {
    id: submission.id,
    assignmentId: submission.assignment_id,
    studentName: submission.student_name,
    answers: submission.answers,
    status: submission.status,
    submittedAt: submission.submitted_at,
    aiScore: submission.ai_score,
    finalScore: submission.final_score,
    finalGrade: submission.final_grade,
  };

  res.json(result);
});

// Get all student's submissions (by student name)
app.get('/api/student/submissions', async (req, res) => {
  const { studentName } = req.query;
  
  let query = supabase
    .from('submissions')
    .select('*')
    .order('submitted_at', { ascending: false });

  if (studentName) {
    query = query.ilike('student_name', studentName);
  }

  const { data: submissions, error } = await query;

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  if (!studentName) {
    // Transform to API format
    const result = submissions.map(s => ({
      id: s.id,
      assignmentId: s.assignment_id,
      studentName: s.student_name,
      answers: s.answers,
      status: s.status,
      submittedAt: s.submitted_at,
      aiScore: s.ai_score,
      finalScore: s.final_score,
      finalGrade: s.final_grade,
    }));
    return res.json(result);
  }

  // Get assignments for student submissions
  const assignmentIds = [...new Set(submissions.map(s => s.assignment_id))];
  const { data: assignments } = await supabase
    .from('assignments')
    .select('*')
    .in('id', assignmentIds);

  const assignmentsMap = {};
  if (assignments) {
    assignments.forEach(a => {
      assignmentsMap[a.id] = a;
    });
  }

  // Transform to API format with assignment info
  const result = submissions.map(submission => {
    const assignment = assignmentsMap[submission.assignment_id];
    return {
      id: submission.id,
      assignmentId: submission.assignment_id,
      studentName: submission.student_name,
      answers: submission.answers,
      status: submission.status,
      submittedAt: submission.submitted_at,
      aiScore: submission.ai_score,
      finalScore: submission.final_score,
      finalGrade: submission.final_grade,
      assignmentTitle: assignment ? assignment.title : 'Unknown Assignment',
      assignmentDescription: assignment ? assignment.description : '',
    };
  });

  res.json(result);
});

// Get student's submission with full details (including feedback)
app.get('/api/student/submissions/:id/details', async (req, res) => {
  const submissionId = parseInt(req.params.id);
  
  const { data: submission, error: submissionError } = await supabase
    .from('submissions')
    .select('*')
    .eq('id', submissionId)
    .single();

  if (submissionError || !submission) {
    return res.status(404).json({ error: 'Submission not found' });
  }

  const { data: assignment, error: assignmentError } = await supabase
    .from('assignments')
    .select('*')
    .eq('id', submission.assignment_id)
    .single();

  if (assignmentError || !assignment) {
    return res.status(404).json({ error: 'Assignment not found' });
  }

  // Return submission with assignment details and question feedback
  const detailedSubmission = {
    id: submission.id,
    assignmentId: submission.assignment_id,
    studentName: submission.student_name,
    answers: submission.answers,
    status: submission.status,
    submittedAt: submission.submitted_at,
    aiScore: submission.ai_score,
    finalScore: submission.final_score,
    finalGrade: submission.final_grade,
    assignment: {
      id: assignment.id,
      title: assignment.title,
      description: assignment.description,
      questions: assignment.questions.map(q => ({
        questionNumber: q.questionNumber,
        questionText: q.questionText,
        options: q.options,
        marks: q.marks,
        // Include correct answer for student to see after grading
        correctOptions: q.correctOptions,
      })),
    },
  };

  res.json(detailedSubmission);
});

// ============================================
// AI FEEDBACK GENERATION
// ============================================

async function generateEncouragingFeedback(question, studentSelected, isCorrect) {
  const correctOptions = question.correctOptions;
  const studentAnswers = question.options.filter((_, idx) => studentSelected.includes(idx));
  const correctAnswers = question.options.filter((_, idx) => correctOptions.includes(idx));

  if (isCorrect) {
    const prompt = `You are a supportive and encouraging teacher providing feedback to a student.

Question: ${question.questionText}
Options: ${question.options.join(', ')}
Correct Answer: ${correctAnswers.join(', ')}
Student's Answer: ${studentAnswers.join(', ')}
Rubric/Context: ${question.rubric}

The student got this question CORRECT. Provide brief, positive reinforcement (1-2 sentences). Be warm and encouraging.`;

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        {
          role: 'system',
          content: 'You are a supportive, encouraging teacher. Always use positive, growth-oriented language. Never discourage students. Focus on what they can learn and improve.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      max_tokens: 150,
      temperature: 0.7,
    });

    return response.choices[0].message.content.trim();
  } else {
    const prompt = `You are a supportive and encouraging teacher providing feedback to a student.

Question: ${question.questionText}
Options: ${question.options.join(', ')}
Correct Answer: ${correctAnswers.join(', ')}
Student's Answer: ${studentAnswers.join(', ')}
Rubric/Context: ${question.rubric}

The student got this question INCORRECT. Provide encouraging, growth-oriented feedback (2-3 sentences):
- Acknowledge their effort
- Gently point out what they might have missed
- Suggest how to approach similar questions next time
- Use positive language (avoid words like "wrong", "failed", "mistake")
- Focus on learning and improvement

Example tone: "You were on the right track! Consider focusing on [specific aspect]. Next time, try [helpful tip]."`;

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        {
          role: 'system',
          content: 'You are a supportive, encouraging teacher. Always use positive, growth-oriented language. Never discourage students. Focus on what they can learn and improve.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      max_tokens: 150,
      temperature: 0.7,
    });

    return response.choices[0].message.content.trim();
  }
}

// ============================================
// START SERVER
// ============================================

// ============================================
// ROOT ENDPOINT
// ============================================

app.get('/', (req, res) => {
  res.json({
    message: 'LMS Demo API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      info: '/api/info',
      teacher: {
        assignments: 'GET /api/teacher/assignments',
        assignment: 'GET /api/teacher/assignments/:id',
        submissions: 'GET /api/teacher/submissions',
        submission: 'GET /api/teacher/submissions/:id',
        assignmentSubmissions: 'GET /api/teacher/assignments/:id/submissions'
      },
      student: {
        assignments: 'GET /api/student/assignments',
        assignment: 'GET /api/student/assignments/:id',
        submissions: 'GET /api/student/submissions?studentName=name',
        submission: 'GET /api/student/submissions/:id'
      }
    }
  });
});

// ============================================
// START SERVER
// ============================================

// Initialize and start server
async function startServer() {
  // NOTE: Seed function is disabled - assignments should be inserted via SQL
  // Uncomment the line below only if you want to seed on server start (not recommended for production)
  // await seedAssignments();

  app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log(`📚 Teacher API: http://localhost:${PORT}/api/teacher`);
    console.log(`👨‍🎓 Student API: http://localhost:${PORT}/api/student`);
    console.log(`❤️  Health Check: http://localhost:${PORT}/api/health`);
    console.log(`💾 Using Supabase for persistent storage`);
    console.log(`📝 Seed function disabled - use SQL to insert assignments`);
  });
}

startServer();

