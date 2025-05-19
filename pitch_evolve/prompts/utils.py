import os

def load(prompt_path: str) -> str:
    """
    Load a prompt from a file.
    
    Args:
        prompt_path: Relative path to the prompt file
    
    Returns:
        The prompt content as a string
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    prompt_full_path = os.path.join(base_dir, prompt_path)
    
    with open(prompt_full_path, 'r') as f:
        return f.read()
