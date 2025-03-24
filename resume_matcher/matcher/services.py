from llama_cpp import Llama
import os

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

# Load Llama Model
llm = Llama(model_path="path/to/llama-3-model.gguf")

def parse_resume(text):
    prompt = f"Extract structured resume data from this text:\n\n{text}"
    response = llm(prompt)
    return response['choices'][0]['text']

def parse_job_posting(text):
    prompt = f"Extract structured job posting data from this text:\n\n{text}"
    response = llm(prompt)
    return response['choices'][0]['text']

def match_candidate_to_job(candidate, job):
    prompt = f"Match the following candidate profile to this job and provide match score, missing skills, and summary:\n\nCandidate: {candidate}\n\nJob: {job}"
    response = llm(prompt)
    return response['choices'][0]['text']

def generate_cover_letter(candidate, job):
    prompt = f"Generate a personalized cover letter for {candidate['name']} applying to {job['title']} at {job['company']}.\n\nCandidate Profile: {candidate}\n\nJob Description: {job}"
    response = llm(prompt)
    return response['choices'][0]['text']