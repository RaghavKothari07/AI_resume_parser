from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CandidateProfile, JobPosting
from .services import parse_resume, parse_job_posting, match_candidate_to_job, generate_cover_letter

@api_view(['POST'])
def upload_resume(request):
    text = request.data.get("resume_text", "")
    parsed_data = parse_resume(text)
    return Response(parsed_data)

@api_view(['POST'])
def upload_job_posting(request):
    text = request.data.get("job_text", "")
    parsed_data = parse_job_posting(text)
    return Response(parsed_data)

@api_view(['POST'])
def match_candidate(request):
    candidate_id = request.data.get("candidate_id")
    job_id = request.data.get("job_id")
    match_data = match_candidate_to_job(candidate_id, job_id)
    return Response(match_data)

@api_view(['POST'])
def cover_letter(request):
    candidate_id = request.data.get("candidate_id")
    job_id = request.data.get("job_id")
    cover_letter_text = generate_cover_letter(candidate_id, job_id)
    return Response({"cover_letter": cover_letter_text})
