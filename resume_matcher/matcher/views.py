from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CandidateProfile, JobPosting, MatchResult
from .serializers import CandidateProfileSerializer, JobPostingSerializer, MatchResultSerializer
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
    candidate = request.data.get("candidate")
    job = request.data.get("job")
    match_data = match_candidate_to_job(candidate, job)
    return Response(match_data)

@api_view(['POST'])
def cover_letter(request):
    candidate = request.data.get("candidate")
    job = request.data.get("job")
    cover_letter_text = generate_cover_letter(candidate, job)
    return Response({"cover_letter": cover_letter_text})