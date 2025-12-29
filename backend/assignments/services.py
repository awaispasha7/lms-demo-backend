"""
Services for assignment grading and AI feedback
"""
import openai
from django.conf import settings
from django.utils import timezone
from .models import Submission
from decimal import Decimal


def auto_grade_submission(submission):
    """
    Auto-grade a submission by comparing answers with answer keys.
    Works with JSONB questions and answers structure.
    """
    assignment = submission.assignment
    questions = assignment.questions or []
    answers = submission.answers or []
    
    total_score = 0
    updated_answers = []
    
    # Create a map of questions by questionNumber
    questions_map = {q.get('questionNumber'): q for q in questions if isinstance(q, dict)}
    
    for answer in answers:
        question_number = answer.get('questionNumber')
        question = questions_map.get(question_number)
        
        if not question:
            # Question not found, skip
            updated_answers.append(answer)
            continue
        
        # Handle different question types
        question_type = question.get('type', 'mcq')
        is_correct = False
        score = 0
        
        if question_type == 'short_answer':
            # For short answers, we'll use AI grading (handled separately)
            # For now, mark as not graded
            updated_answers.append({
                **answer,
                'isCorrect': False,
                'score': 0,
            })
            continue
        else:
            # MCQ or True/False
            student_selected = set(answer.get('selectedOptions', []))
            correct_options = set(question.get('correctOptions', []))
            
            is_correct = student_selected == correct_options
            score = question.get('marks', 0) if is_correct else 0
        
        updated_answers.append({
            **answer,
            'isCorrect': is_correct,
            'score': score,
        })
        
        total_score += score
    
    # Update submission
    submission.answers = updated_answers
    submission.ai_score = total_score
    submission.status = 'submitted'
    submission.graded_at = timezone.now()
    submission.save()
    
    return total_score


async def grade_short_answer_async(question, student_answer):
    """
    Grade a short answer question using OpenAI.
    Returns dict with isCorrect, score, and reasoning.
    """
    if not settings.OPENAI_API_KEY:
        return {
            'isCorrect': False,
            'score': 0,
            'reasoning': 'AI grading unavailable'
        }
    
    prompt = f"""You are a teacher grading a short answer question. Your task is to evaluate the student's response and determine if it demonstrates understanding of the key concepts.

Question: {question.get('questionText', '')}
Maximum Marks: {question.get('marks', 0)}
Rubric/Key Points to Look For: {question.get('rubric', '')}
Student's Answer: {student_answer}

Evaluate the student's answer based on the rubric. The answer should demonstrate understanding of the key concepts mentioned in the rubric.

Respond in JSON format only:
{{
  "isCorrect": true or false,
  "score": number between 0 and {question.get('marks', 0)} (full marks if correct, partial marks if partially correct, 0 if incorrect),
  "reasoning": "brief explanation of why this score was given"
}}

Be fair but strict. Give full marks only if the answer demonstrates clear understanding of all key concepts. Give partial marks if some concepts are covered but not all. Give 0 if the answer is incorrect or doesn't address the question."""

    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an experienced teacher grading student responses. Be fair, consistent, and focus on whether the student demonstrates understanding of the key concepts.',
                },
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            response_format={'type': 'json_object'},
            temperature=0.3,
            max_tokens=200,
        )
        
        result = eval(response.choices[0].message.content) if isinstance(response.choices[0].message.content, str) else response.choices[0].message.content
        
        return {
            'isCorrect': result.get('isCorrect', False),
            'score': min(max(0, result.get('score', 0)), question.get('marks', 0)),
            'reasoning': result.get('reasoning', ''),
        }
    except Exception as e:
        print(f'Error grading short answer with LLM: {e}')
        return {
            'isCorrect': False,
            'score': 0,
            'reasoning': 'Error in automated grading',
        }


def generate_encouraging_feedback(question, student_selected, is_correct, student_text_answer=None):
    """
    Generate encouraging, growth-oriented feedback for a student's answer using OpenAI.
    Works with JSONB question structure.
    """
    if not settings.OPENAI_API_KEY:
        if is_correct:
            return 'Great job! You got this question correct. Keep up the excellent work!'
        else:
            return 'This question needs another look. Review the concepts and try again—you\'ve got this!'
    
    question_type = question.get('type', 'mcq')
    question_text = question.get('questionText', '')
    options = question.get('options', [])
    correct_options = question.get('correctOptions', [])
    rubric = question.get('rubric', '')
    
    # Handle short answer questions
    if question_type == 'short_answer':
        if not student_text_answer:
            return 'Please provide an answer to this question. Take your time to think through the key concepts.'
        
        prompt = f"""You are a supportive and encouraging teacher providing feedback to a student.

Question: {question_text}
Rubric/Key Points: {rubric or 'Evaluate based on understanding of the core concepts'}
Student's Answer: {student_text_answer}
Student's Score: {'Full marks' if is_correct else 'Partial or no marks'}

Provide constructive, encouraging feedback (2-3 sentences). If the answer is correct, celebrate their understanding. If incorrect or partially correct, gently guide them toward the key concepts without discouraging them. Be warm and supportive."""

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a supportive, encouraging teacher. Always use positive, growth-oriented language. Never discourage students. Focus on what they can learn and improve.',
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                max_tokens=200,
                temperature=0.7,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f'Error generating feedback for short answer: {e}')
            if is_correct:
                return 'Great job! You demonstrated good understanding of the key concepts. Keep up the excellent work!'
            else:
                return 'This question needs another look. Review the key concepts mentioned in the rubric and try to explain them in your own words. You\'ve got this!'
    
    # Handle MCQ and True/False questions
    if not options or not isinstance(options, list):
        return 'Feedback unavailable for this question type.'
    
    student_answers = [options[i] for i in student_selected if i < len(options)]
    correct_answers = [options[i] for i in correct_options if i < len(options)]
    
    if is_correct:
        prompt = f"""You are a supportive and encouraging teacher providing feedback to a student.

Question: {question_text}
Options: {', '.join(options)}
Correct Answer: {', '.join(correct_answers)}
Student's Answer: {', '.join(student_answers)}
Rubric/Context: {rubric}

The student got this question CORRECT. Provide brief, positive reinforcement (1-2 sentences). Be warm and encouraging."""

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a supportive, encouraging teacher. Always use positive, growth-oriented language. Never discourage students. Focus on what they can learn and improve.',
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                max_tokens=150,
                temperature=0.7,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f'Error generating feedback for correct answer: {e}')
            return 'Great job! You got this question correct. Keep up the excellent work!'
    else:
        # Handle incorrect answers
        prompt = f"""You are a supportive and encouraging teacher providing feedback to a student.

Question: {question_text}
Options: {', '.join(options)}
Correct Answer: {', '.join(correct_answers)}
Student's Answer: {', '.join(student_answers) if student_answers else 'No answer selected'}
Rubric/Context: {rubric or 'N/A'}

The student got this question INCORRECT. Provide encouraging, growth-oriented feedback (2-3 sentences):
- Acknowledge their effort
- Gently point out what they might have missed
- Suggest how to approach similar questions next time
- Use positive language (avoid words like "wrong", "failed", "mistake")
- Focus on learning and improvement

Example tone: "You were on the right track! Consider focusing on [specific aspect]. Next time, try [helpful tip]." """

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a supportive, encouraging teacher. Always use positive, growth-oriented language. Never discourage students. Focus on what they can learn and improve.',
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                max_tokens=200,
                temperature=0.7,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f'Error generating feedback for incorrect answer: {e}')
            return 'This question needs another look. Review the concepts and try again—you\'ve got this!'

