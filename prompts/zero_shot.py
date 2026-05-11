# Experiment: All models × zero-shot strategy
# Orijinal CodeEnhancer system prompt'unun birebir karşılığı.


def create_prompt(task_description: str) -> str:
    """Zero-shot prompt — görev açıklaması dışında hiçbir örnek veya yönlendirme yok."""
    return (
        "Please write Python code for the following task. "
        "At the very top, add a triple-quoted docstring with these three sections, each starting on its own line:\n"
        "• **Input Prompt**: Restate the prompt clearly.\n"
        "• **Intention**: State the purpose of the code.\n"
        "• **Functionality**: Describe briefly how the code solves the task.\n\n"
        "Write only valid Python code and no extra explanations. Return the complete script only.\n\n"
        f"Prompt: {task_description}"
    )


SYSTEM_PROMPT = "You are a code generation assistant."
