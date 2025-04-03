from setuptools import setup, find_packages

setup(
    name="business-idea-analyzer",
    version="1.0.0",
    description="AI-powered tool for generating and analyzing business ideas",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=1.0.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "textblob>=0.17.1",
        "yfinance>=0.2.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business/Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business",
    ],
) 