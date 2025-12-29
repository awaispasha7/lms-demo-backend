from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
import json
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from .services import auto_grade_submission, generate_encouraging_feedback


# ============================================
# API VIEWS (for compatibility with Express.js API)
# ============================================

@api_view(['GET'])
def api_health(request):
    """Health check endpoint"""
    return Response({
        'status': 'ok',
        'message': 'Server is running',
        'timestamp': timezone.now().isoformat()
    })


@api_view(['GET'])
def api_info(request):
    """Server info endpoint"""
    assignment_count = Assignment.objects.count()
    submission_count = Submission.objects.count()
    
    return Response({
        'totalAssignments': assignment_count,
        'totalSubmissions': submission_count,
        'server': 'LMS Demo API',
        'version': '1.0.0',
        'storage': 'Supabase'
    })


@api_view(['GET', 'POST'])
def api_teacher_assignments(request):
    """Teacher assignments endpoint"""
    if request.method == 'GET':
        assignments = Assignment.objects.all().order_by('-created_at')
        
        # Get submission stats
        result = []
        for assignment in assignments:
            submissions = Submission.objects.filter(assignment=assignment)
            result.append({
                'id': assignment.id,
                'title': assignment.title,
                'description': assignment.description,
                'questions': assignment.questions,
                'dueDate': assignment.due_date.isoformat() if assignment.due_date else None,
                'createdAt': assignment.created_at.isoformat(),
                'totalSubmissions': submissions.count(),
                'gradedCount': submissions.filter(status='graded').count(),
                'pendingCount': submissions.filter(status='pending').count(),
            })
        
        return Response(result)
    
    elif request.method == 'POST':
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            assignment = serializer.save()
            return Response(AssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_teacher_assignment_detail(request, assignment_id):
    """Get assignment detail"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    serializer = AssignmentSerializer(assignment)
    return Response(serializer.data)


@api_view(['GET'])
def api_teacher_submissions(request, assignment_id):
    """Get submissions for an assignment"""
    submissions = Submission.objects.filter(assignment_id=assignment_id).order_by('-submitted_at')
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_teacher_auto_grade(request, assignment_id):
    """Auto-grade all submissions for an assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment, status='pending')
    
    graded_count = 0
    for submission in submissions:
        auto_grade_submission(submission)
        graded_count += 1
    
    return Response({
        'message': f'Auto-graded {graded_count} submissions',
        'gradedCount': graded_count
    })


@api_view(['GET', 'POST'])
def api_student_assignments(request):
    """Student assignments endpoint"""
    if request.method == 'GET':
        assignments = Assignment.objects.all().order_by('-created_at')
        result = []
        for assignment in assignments:
            result.append({
                'id': assignment.id,
                'title': assignment.title,
                'description': assignment.description,
                'dueDate': assignment.due_date.isoformat() if assignment.due_date else None,
                'createdAt': assignment.created_at.isoformat(),
            })
        return Response(result)


@api_view(['GET'])
def api_student_assignment_detail(request, assignment_id):
    """Get assignment detail for student (without correct answers)"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Remove correct answers from questions
    student_questions = []
    for q in assignment.questions:
        student_q = {k: v for k, v in q.items() if k != 'correctOptions'}
        student_q['questionNumber'] = q.get('questionNumber')
        student_questions.append(student_q)
    
    return Response({
        'id': assignment.id,
        'title': assignment.title,
        'description': assignment.description,
        'dueDate': assignment.due_date.isoformat() if assignment.due_date else None,
        'createdAt': assignment.created_at.isoformat(),
        'questions': student_questions,
    })


@api_view(['POST'])
def api_student_submit(request, assignment_id):
    """Submit assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    student_name = request.data.get('studentName')
    answers = request.data.get('answers', [])
    
    submission = Submission.objects.create(
        assignment=assignment,
        student_name=student_name,
        answers=answers,
        status='pending'
    )
    
    serializer = SubmissionSerializer(submission)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def api_teacher_all_submissions(request):
    """Get all submissions (teacher view)"""
    submissions = Submission.objects.all().order_by('-submitted_at')
    serializer = SubmissionSerializer(submissions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_teacher_submission_detail(request, submission_id):
    """Get single submission by ID (teacher view)"""
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    
    result = SubmissionSerializer(submission).data
    result['assignment'] = AssignmentSerializer(assignment).data
    
    return Response(result)


@api_view(['POST'])
def api_teacher_generate_feedback(request, submission_id):
    """Generate AI feedback for a submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    
    questions = assignment.questions or []
    answers = submission.answers or []
    
    # Create questions map
    questions_map = {q.get('questionNumber'): q for q in questions if isinstance(q, dict)}
    
    feedback_count = 0
    updated_answers = []
    
    for answer in answers:
        question_number = answer.get('questionNumber')
        question = questions_map.get(question_number)
        
        if not question:
            updated_answers.append(answer)
            continue
        
        # Generate feedback if not already present
        if not answer.get('aiFeedback'):
            is_correct = answer.get('isCorrect', False)
            selected_options = answer.get('selectedOptions', [])
            text_answer = answer.get('textAnswer')
            
            feedback = generate_encouraging_feedback(
                question,
                selected_options,
                is_correct,
                text_answer
            )
            
            answer['aiFeedback'] = feedback
            answer['feedbackGeneratedAt'] = timezone.now().isoformat()
            feedback_count += 1
        
        updated_answers.append(answer)
    
    submission.answers = updated_answers
    submission.save()
    
    return Response({
        'message': f'Generated feedback for {feedback_count} questions',
        'feedbackCount': feedback_count
    })


@api_view(['POST'])
def api_teacher_finalize_grade(request, submission_id):
    """Finalize grade for a submission"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    final_score = request.data.get('finalScore', submission.ai_score)
    final_grade = request.data.get('finalGrade')
    teacher_notes = request.data.get('teacherNotes', '')
    
    submission.final_score = final_score
    submission.final_grade = final_grade
    submission.teacher_notes = teacher_notes
    submission.status = 'graded'
    submission.finalized_at = timezone.now()
    submission.save()
    
    serializer = SubmissionSerializer(submission)
    return Response(serializer.data)


@api_view(['GET'])
def api_student_submissions(request):
    """Get all student submissions (optionally filtered by studentName)"""
    student_name = request.query_params.get('studentName')
    
    if student_name:
        submissions = Submission.objects.filter(student_name__icontains=student_name).order_by('-submitted_at')
    else:
        submissions = Submission.objects.all().order_by('-submitted_at')
    
    # Get assignments for submissions
    assignment_ids = submissions.values_list('assignment_id', flat=True).distinct()
    assignments = {a.id: a for a in Assignment.objects.filter(id__in=assignment_ids)}
    
    result = []
    for submission in submissions:
        sub_data = SubmissionSerializer(submission).data
        assignment = assignments.get(submission.assignment_id)
        if assignment:
            sub_data['assignmentTitle'] = assignment.title
            sub_data['assignmentDescription'] = assignment.description
        result.append(sub_data)
    
    return Response(result)


@api_view(['GET'])
def api_student_submission_detail(request, submission_id):
    """Get student submission detail"""
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    
    result = SubmissionSerializer(submission).data
    
    # Include assignment with questions (but hide correct answers if not graded)
    assignment_data = {
        'id': assignment.id,
        'title': assignment.title,
        'description': assignment.description,
        'questions': []
    }
    
    for q in assignment.questions:
        question_data = {
            'questionNumber': q.get('questionNumber'),
            'questionText': q.get('questionText'),
            'options': q.get('options'),
            'marks': q.get('marks'),
            'type': q.get('type'),
            'rubric': q.get('rubric'),
        }
        
        # Only show correct answers if submission is graded
        if submission.status != 'pending' and submission.ai_score is not None:
            question_data['correctOptions'] = q.get('correctOptions')
        
        assignment_data['questions'].append(question_data)
    
    result['assignment'] = assignment_data
    
    return Response(result)


# ============================================
# TEMPLATE VIEWS (Django + HTMX)
# ============================================

def index(request):
    """Home page"""
    return render(request, 'assignments/index.html')


def teacher_dashboard(request):
    """Teacher dashboard"""
    assignments = Assignment.objects.annotate(
        total_submissions=Count('submissions'),
        graded_count=Count('submissions', filter=Q(submissions__status='GRADED')),
        pending_count=Count('submissions', filter=Q(submissions__status='SUBMITTED') | Q(submissions__status='DRAFT'))
    ).order_by('-created_at')
    
    context = {
        'assignments': assignments
    }
    return render(request, 'assignments/teacher/dashboard.html', context)


def teacher_assignment_list(request):
    """Teacher assignment list (HTMX partial)"""
    assignments = Assignment.objects.annotate(
        total_submissions=Count('submissions'),
        graded_count=Count('submissions', filter=Q(submissions__status='GRADED')),
        pending_count=Count('submissions', filter=Q(submissions__status='SUBMITTED') | Q(submissions__status='DRAFT'))
    ).order_by('-created_at')
    
    return render(request, 'assignments/teacher/assignment_list.html', {'assignments': assignments})


def teacher_assignment_create(request):
    """Create new assignment"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Validate and create assignment
        questions = data.get('questions', [])
        for idx, q in enumerate(questions):
            q['questionNumber'] = idx + 1
        
        assignment = Assignment.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            questions=questions,
            due_date=data.get('dueDate')
        )
        
        if request.headers.get('HX-Request'):
            return HttpResponse(f'<div hx-get="/teacher/assignments" hx-trigger="load" hx-swap="outerHTML">Assignment created!</div>')
        return redirect('teacher_dashboard')
    
    return render(request, 'assignments/teacher/create.html')


def teacher_assignment_detail(request, assignment_id):
    """Assignment detail with submissions"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment).order_by('-submitted_at')
    
    context = {
        'assignment': assignment,
        'submissions': submissions
    }
    return render(request, 'assignments/teacher/assignment_detail.html', context)


def teacher_submission_detail(request, submission_id):
    """Submission detail for grading"""
    submission = get_object_or_404(Submission, id=submission_id)
    assignment = submission.assignment
    
    context = {
        'submission': submission,
        'assignment': assignment
    }
    return render(request, 'assignments/teacher/submission_detail.html', context)


def student_dashboard(request):
    """Student dashboard"""
    assignments = Assignment.objects.all().order_by('-created_at')
    context = {'assignments': assignments}
    return render(request, 'assignments/student/dashboard.html', context)


def student_assignment_detail(request, assignment_id):
    """Student assignment detail"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    context = {'assignment': assignment}
    return render(request, 'assignments/student/assignment_detail.html', context)


def test_backend_url(request):
    """Test page to verify backend API URL configuration"""
    from django.conf import settings
    context = {
        'BACKEND_API_URL': getattr(settings, 'BACKEND_API_URL', '')
    }
    return render(request, 'assignments/test_backend_url.html', context)

