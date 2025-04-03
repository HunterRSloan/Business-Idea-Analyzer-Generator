# Business Idea Analyzer & Generator

An AI-powered tool that helps entrepreneurs evaluate and generate business ideas using market analysis, sentiment analysis, and feasibility assessment.

## Features

- **Business Idea Generation**: Generate innovative business ideas based on industry and target market
- **Feasibility Assessment**: Evaluate business ideas using multiple criteria:
  - Market trends and outlook
  - Risk level analysis
  - Market sentiment
  - Ethical impact assessment
  - Complexity evaluation
  - Competition analysis
  - Scalability potential
- **Comprehensive Scoring**: Get detailed scores and insights for each business idea
- **Market Analysis**: Real-time market data and sentiment analysis using financial APIs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/business-idea-analyzer.git
cd business-idea-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     NEWS_API_KEY=your_news_api_key_here
     ```

## Usage

### Basic Usage

```python
from business_idea_analyzer import BusinessIdeaGenerator

# Initialize the generator
generator = BusinessIdeaGenerator()

# Generate business ideas
ideas = generator.generate_ideas(
    industry="technology",
    target_market="small businesses"
)

# Assess a specific idea
assessment = generator.assess_feasibility(
    idea="A sustainable mobile app for managing finances",
    initial_investment=50000,
    target_roi=200
)

# Print results
print(f"Feasibility Score: {assessment['score']:.2f}")
print(f"Market Outlook: {assessment['market_outlook']}")
print(f"Risk Level: {assessment['risk_level']}")
print(f"Market Sentiment: {assessment['sentiment']}")
```

### Running the Demo

```bash
python src/main.py
```

This will run the demo script that:
1. Tests assessment of a bad idea
2. Tests assessment of a good idea
3. Generates and assesses new business ideas

## Project Structure

```
business-idea-analyzer/
├── src/
│   ├── __init__.py
│   ├── business_generator.py
│   ├── business_advisor.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT-3.5 API
- Yahoo Finance for market data
- News API for sentiment analysis
- TextBlob for natural language processing 