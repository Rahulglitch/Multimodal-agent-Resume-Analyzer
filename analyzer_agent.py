# agents/analyzer_agent.py

from utils.llm import llm


def analyzer_resume(
    resume_text,
    resume_skills
):

    prompt = f"""
You are a Resume Analysis Agent.

Analyze the candidate's resume carefully.

Resume Text:
{resume_text}

Detected Resume Skills:
{resume_skills}

Provide a detailed analysis containing:

1. Candidate profile summary
2. Technical skills
3. Soft skills
4. Work experience
5. Education
6. Projects
7. Certifications
8. Key strengths
9. Potential weaknesses
10. Overall resume quality

Only use information that is actually present
in the resume.

Do not invent qualifications, experience,
skills, projects, or certifications.
"""

    response = llm.invoke(prompt)

    if not response or not response.content:

        raise ValueError(
            "Analyzer Agent returned an empty response."
        )

    return response.content
