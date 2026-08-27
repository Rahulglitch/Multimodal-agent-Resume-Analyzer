# utils/skill_extractor.py

KNOWN_SKILLS = [

    "Python",
    "Java",
    "JavaScript",
    "React",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",

    "PostgreSQL",
    "MySQL",
    "MongoDB",

    "Docker",
    "Kubernetes",

    "AWS",
    "Azure",

    "Git",
    "GitHub",
    "CI/CD",

    "Machine Learning",
    "Deep Learning",

    "TensorFlow",
    "PyTorch",
]


def extract_skills(text):

    if not text:

        return []

    text_lower = text.lower()

    found_skills = []

    for skill in KNOWN_SKILLS:

        if skill.lower() in text_lower:

            found_skills.append(skill)

    return found_skills
