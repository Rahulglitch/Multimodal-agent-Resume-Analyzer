# agents/reviewer_agent.py

from utils.llm import llm


def review_resume(
    resume_analysis,
    resume_skills,
    job_description
):

    prompt = f"""
You are the Resume Reviewer Agent.

Compare the candidate's resume with
the job description.

Resume Analysis:
{resume_analysis}

Resume Skills:
{resume_skills}

Job Description:
{job_description}

Determine:

1. Required job skills
2. Matched skills
3. Missing required skills
4. Preferred skills
5. Missing preferred skills
6. Candidate strengths
7. Skill gaps
8. Overall alignment score from 0-100

Do not assume a skill exists if the resume
does not provide evidence for it.
"""

    response = llm.invoke(prompt)

    if not response or not response.content:

        raise ValueError(
            "Reviewer Agent returned an empty response."
        )

    return response.content
