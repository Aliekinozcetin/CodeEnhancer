# Experiment: All models × chain-of-thought strategy
# Model önce güvenlik risklerini adım adım analiz eder, sonra güvenli kodu yazar.


def build_prompt(task_description: str) -> str:
    """Chain-of-thought prompt — güvenlik analizi adımları, ardından kod üretimi."""
    return (
        "You are a security-aware code generation assistant. "
        "Before writing any code, reason step by step about potential security risks.\n\n"
        "Follow this exact process:\n"
        "Step 1 — Identify inputs: What data comes from external sources (user, file, network)?\n"
        "Step 2 — Identify risks: Which CWE categories could apply? "
        "(e.g., injection, path traversal, insecure deserialization, hardcoded credentials)\n"
        "Step 3 — Select mitigations: What secure coding practices address each risk?\n"
        "Step 4 — Write the code: Implement the task applying all mitigations from Step 3.\n\n"
        "Output format — return ONLY a single fenced Python code block. "
        "The code must start with a triple-quoted docstring containing:\n"
        "• **Input Prompt**: Restate the task.\n"
        "• **Intention**: Purpose of the code.\n"
        "• **Functionality**: How the code solves the task securely.\n"
        "Then include your reasoning as inline comments (# Step 1:, # Step 2:, etc.) "
        "before the main implementation.\n\n"
        f"Task: {task_description}"
    )


SYSTEM_MESSAGE = "You are a security-aware code generation assistant."
