from llama_cpp import Llama
import os
import fitz  # PyMuPDF for PDF parsing

# Load Llama Model
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
llm = Llama(model_path="path/to/llama-3-model.gguf")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    return text

def parse_resume(pdf_path):
    """Extract structured resume data from a PDF using Llama function calling."""
    text = extract_text_from_pdf(pdf_path)

    # Define function schema
    functions = [
        {
            "name": "parse_resume",
            "description": "Extract structured resume data from plain text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "skills": {"type": "array", "items": {"type": "string"}},
                    "education": {"type": "array", "items": {"type": "string"}},
                    "work_experience": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["name", "skills", "education", "work_experience"]
            }
        }
    ]

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": text}],
        functions=functions,
        function_call="parse_resume"
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]

def parse_job_posting(text):
    """Extract structured job posting data from plain text."""
    functions = [
        {
            "name": "parse_job_posting",
            "description": "Extract job posting details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "required_skills": {"type": "array", "items": {"type": "string"}},
                    "description": {"type": "string"}
                },
                "required": ["title", "company", "required_skills", "description"]
            }
        }
    ]

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": text}],
        functions=functions,
        function_call="parse_job_posting"
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]

def match_candidate_to_job(candidate, job):
    """Match a candidate to a job posting and return a match score."""
    functions = [
        {
            "name": "match_candidate_to_job",
            "description": "Compute a match score between a candidate and a job.",
            "parameters": {
                "type": "object",
                "properties": {
                    "match_score": {"type": "integer"},
                    "missing_skills": {"type": "array", "items": {"type": "string"}},
                    "summary": {"type": "string"}
                },
                "required": ["match_score", "missing_skills", "summary"]
            }
        }
    ]

    prompt = f"Candidate Profile: {candidate}\nJob Posting: {job}"

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        functions=functions,
        function_call="match_candidate_to_job"
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]

def generate_cover_letter(candidate, job):
    """Generate a cover letter using structured function calling."""
    functions = [
        {
            "name": "generate_cover_letter",
            "description": "Generate a tailored cover letter for a candidate applying to a job.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cover_letter": {"type": "string"}
                },
                "required": ["cover_letter"]
            }
        }
    ]

    prompt = f"Generate a cover letter for {candidate['name']} applying for {job['title']} at {job['company']}."

    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        functions=functions,
        function_call="generate_cover_letter"
    )

    return response["choices"][0]["message"]["function_call"]["arguments"]["cover_letter"]
