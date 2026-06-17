def explanation_prompt(topic, level):
    return f"""
    Explain the topic '{topic}' in a {level} level.
    Use simple language, examples, and bullet points.
    """

def summary_prompt(topic):
    return f"Summarize the topic '{topic}' in 5 bullet points."

def quiz_prompt(topic):
    return f"""
    Create 5 multiple-choice questions on '{topic}'.
    Provide answers at the end.
    """

def pdf_explanation_prompt(text, mode):
    return f"""
    You are an AI study assistant.

    Based on the following study material:
    -------------------
    {text[:12000]}
    -------------------

    Task: {mode}
    Use clear explanations and bullet points.
    """
