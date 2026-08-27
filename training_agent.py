# agents/training_agent.py

from utils.llm import llm


def create_training_plan(
    review_result
):

    prompt = f"""
You are a Career Training Agent.

Based on the review below, create a
learning roadmap.

Review:

{review_result}

For each missing skill provide:

- Skill
- Priority
- Why it is important
- Topics to learn
- Practical project idea
- Estimated learning duration

Prioritize skills explicitly required
by the job description.

Do not invent missing skills that are
not supported by the review.
"""

    response = llm.invoke(prompt)

    if not response or not response.content:

        raise ValueError(
            "Training Agent returned an empty response."
        )

    return response.content
