from llama_cpp import Llama
import json
import os
from .models import CandidateProfile, JobPosting, MatchResult

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
llm = Llama(model_path="path/to/llama-3-model.gguf")

def parse_resume(text):
    """Extract structured resume data and store in DB."""
    prompt = f"Extract structured resume data in JSON format:\n\n{text}"
    response = llm(prompt)

    try:
        structured_data = json.loads(response['choices'][0]['text'].strip())
        candidate = CandidateProfile.objects.create(
            name=structured_data['name'],
            skills=structured_data['skills'],
            education=structured_data['education'],
            work_experience=structured_data['work_experience']
        )
        return structured_data
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse response: {str(e)}"}

def parse_job_posting(text):
    """Extract structured job posting data and store in DB."""
    prompt = f"Extract structured job posting data in JSON format:\n\n{text}"
    response = llm(prompt)

    try:
        structured_data = json.loads(response['choices'][0]['text'].strip())
        job = JobPosting.objects.create(
            title=structured_data['title'],
            company=structured_data['company'],
            required_skills=structured_data['required_skills'],
            description=structured_data['description']
        )
        return structured_data
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse response: {str(e)}"}

def match_candidate_to_job(candidate_id, job_id):
    """Match a candidate to a job and store results in DB."""
    candidate = CandidateProfile.objects.get(id=candidate_id)
    job = JobPosting.objects.get(id=job_id)

    prompt = f"Match the candidate with the job and return JSON with match_score, missing_skills, and summary:\n\nCandidate: {candidate}\n\nJob: {job}"
    response = llm(prompt)

    try:
        match_data = json.loads(response['choices'][0]['text'].strip())
        match = MatchResult.objects.create(
            candidate=candidate,
            job=job,
            match_score=match_data["match_score"],
            missing_skills=match_data["missing_skills"],
            summary=match_data["summary"]
        )
        return match_data
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse response: {str(e)}"}

def generate_cover_letter(candidate_id, job_id):
    """Generate a cover letter for a given candidate and job."""
    candidate = CandidateProfile.objects.get(id=candidate_id)
    job = JobPosting.objects.get(id=job_id)

    prompt = f"Generate a JSON response with a 'cover_letter' field for {candidate.name} applying to {job.title} at {job.company}."
    response = llm(prompt)

    try:
        return json.loads(response['choices'][0]['text'].strip()).get("cover_letter", "Error generating cover letter.")
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse response: {str(e)}"}
