from setuptools import setup, find_packages

setup(
    name="pitch_evolve",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "openai>=1.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.1.0",
        "tiktoken>=0.5.0",
        "tenacity>=8.2.0",
        "tqdm>=4.66.0",
        "scikit-learn>=1.3.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.9",
    author="Daniel Compton",
    description="A prompt-evolving pydantic-AI agent for generating go community pitches",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
