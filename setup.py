from setuptools import setup, find_packages

setup(
    name="file-analyzer-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "langchain",
        "faiss-cpu",
        "ollama",
        "python-dotenv",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "file-analyzer=file_analyzer.cli:app",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Um agente CLI para análise de arquivos usando modelos locais",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/file-analyzer-agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 