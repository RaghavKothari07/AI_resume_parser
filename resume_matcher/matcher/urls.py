from django.urls import path
from .views import upload_resume, upload_job_posting, match_candidate, cover_letter

urlpatterns = [
    path('upload-resume/', upload_resume),
    path('upload-job/', upload_job_posting),
    path('match-candidate/', match_candidate),
    path('generate-cover-letter/', cover_letter),
]