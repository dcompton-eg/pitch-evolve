import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    model_name: str = Field(default="gpt-4", description="The LLM model to use for the agent")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    prompt_template_path: Optional[str] = Field(default=None, description="Path to prompt template file")
    evolution_strategy: str = Field(default="tournament", description="Strategy for evolving prompts")
    
class EvalConfig(BaseModel):
    metrics: List[str] = Field(default=["relevance", "persuasiveness", "clarity"], 
                              description="Metrics to evaluate on")
    test_size: float = Field(default=0.2, description="Portion of data to use for testing")
    num_seeds: int = Field(default=5, description="Number of random seeds for experiments")
    
class AppConfig(BaseModel):
    agent: AgentConfig = Field(default_factory=AgentConfig)
    eval: EvalConfig = Field(default_factory=EvalConfig)
    data_dir: str = Field(default="data", description="Directory for data storage")
    output_dir: str = Field(default="output", description="Directory for output storage")
    log_level: str = Field(default="INFO", description="Logging level")
    random_seed: int = Field(default=42, description="Random seed for reproducibility")

def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from a file or use defaults
    """
    if config_path and os.path.exists(config_path):
        # Load from file logic here
        # For now, return default config
        pass
    
    return AppConfig()

# Default configuration
DEFAULT_CONFIG = load_config()