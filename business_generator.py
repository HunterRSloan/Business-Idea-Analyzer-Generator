"""
Business Idea Generator module.
Handles the generation and analysis of business ideas using AI and market data.
"""

import openai
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from textblob import TextBlob
import yfinance as yf
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BusinessIdeaGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = self.api_key
        self.market_data = {}
        self.scaler = MinMaxScaler()
        
    def generate_ideas(self, industry, target_market):
        """Generate business ideas based on market trends and customer demand"""
        try:
            prompt = f"Generate 5 innovative business ideas in the {industry} industry targeting {target_market}. Format each idea as a numbered list item starting with the number followed by a period."
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Split the response and clean up each idea
            ideas = response.choices[0].message.content.split("\n")
            cleaned_ideas = []
            for idea in ideas:
                # Remove numbering and clean up the idea
                cleaned = idea.strip()
                if cleaned and not cleaned.isspace():
                    # Remove the number and period if present
                    if cleaned[0].isdigit() and '. ' in cleaned:
                        cleaned = cleaned.split('. ', 1)[1]
                    cleaned_ideas.append(cleaned)
            
            return cleaned_ideas[:5]  # Ensure we only return 5 ideas
        except openai.RateLimitError:
            print("Error: You've exceeded your OpenAI API quota. Please check your billing details.")
            return []
        except Exception as e:
            print(f"Error generating ideas: {str(e)}")
            return []
    
    def analyze_market_trends(self, industry):
        """Analyze market trends using financial and news data"""
        try:
            # Use a more reliable ETF for technology sector
            etf_symbols = {
                "technology": "XLK",  # Technology Select Sector SPDR Fund
                "healthcare": "XLV",
                "finance": "XLF",
                "consumer": "XLP",
                "default": "SPY"  # S&P 500 ETF as fallback
            }
            
            etf_symbol = etf_symbols.get(industry.lower(), etf_symbols["default"])
            etf = yf.Ticker(etf_symbol)
            hist = etf.history(period="1y")
            
            if hist.empty:
                raise ValueError(f"No data found for ETF {etf_symbol}")
            
            # Calculate trend indicators
            self.market_data['price_trend'] = hist['Close'].pct_change().mean()
            self.market_data['volatility'] = hist['Close'].std()
            
            # Get news sentiment
            news_api_key = os.getenv('NEWS_API_KEY')
            if not news_api_key:
                raise ValueError("NEWS_API_KEY environment variable is not set")
                
            url = f"https://newsapi.org/v2/everything?q={industry}&apiKey={news_api_key}"
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json()['articles']
            
            sentiment_scores = []
            for article in articles:
                 text = f"{article.get('title', '')} {article.get('description', '')}"
                 blob = TextBlob(text)
                 sentiment_scores.append(blob.sentiment.polarity)
                
            self.market_data['news_sentiment'] = np.mean(sentiment_scores) if sentiment_scores else 0
        except Exception as e:
            print(f"Error analyzing market trends: {str(e)}")
            # Set more realistic default values based on industry
            self.market_data['price_trend'] = 0.15 if industry.lower() == "technology" else 0.05
            self.market_data['volatility'] = 0.25 if industry.lower() == "technology" else 0.15
            self.market_data['news_sentiment'] = 0.2 if industry.lower() == "technology" else 0.1
        
    def assess_feasibility(self, idea, initial_investment, target_roi):
        """Assess the feasibility of a business idea"""
        try:
            # Get ethical impact first
            ethical_impact = self._assess_ethical_impact(idea)
            
            # If ethical impact is very low (harmful idea), return very low scores
            if ethical_impact < 0.3:
                return {
                    'score': 20.0,  # Very low score for harmful ideas
                    'market_outlook': 'Very Negative',
                    'risk_level': 'Very High',
                    'sentiment': 'Very Negative'
                }
            
            # Analyze idea characteristics
            idea_characteristics = {
                'idea': idea,
                'market_trend': float(self.market_data['price_trend']),
                'market_volatility': float(self.market_data['volatility']),
                'sentiment': float(self.market_data['news_sentiment']),
                'investment_required': float(initial_investment),
                'target_roi': float(target_roi),
                'complexity': float(self._assess_complexity(idea)),
                'market_competition': float(self._assess_competition(idea)),
                'scalability': float(self._assess_scalability(idea)),
                'ethical_impact': ethical_impact
            }
            
            # Create a DataFrame with multiple rows for proper normalization
            df = pd.DataFrame([idea_characteristics])
            
            # Normalize each column separately
            for column in df.columns:
                if column == 'idea':
                    continue
                if column in ['market_trend', 'sentiment']:
                    # These should be normalized to [-1, 1] range
                    df[column] = df[column].clip(-1, 1)
                elif column in ['investment_required', 'target_roi']:
                    # These should be normalized to [0, 1] range
                    df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min() + 1e-10)
                else:
                    # All other factors are already in [0, 1] range
                    df[column] = df[column].clip(0, 1)
            
            # Calculate weighted feasibility score (0-100)
            weights = {
                'market_trend': 0.15,
                'market_volatility': 0.1,
                'sentiment': 0.1,
                'investment_required': 0.1,
                'target_roi': 0.1,
                'complexity': 0.1,
                'market_competition': 0.1,
                'scalability': 0.1,
                'ethical_impact': 0.15
            }
            
            # Calculate weighted score
            weighted_score = sum(df[col].iloc[0] * weights[col] for col in weights)
            feasibility_score = (weighted_score + 1) * 50  # Convert to 0-100 range
            
            # Get characteristics as float values for determination methods
            characteristics = {
                'market_trend': float(df['market_trend'].iloc[0]),
                'sentiment': float(df['sentiment'].iloc[0]),
                'market_competition': float(df['market_competition'].iloc[0]),
                'ethical_impact': float(df['ethical_impact'].iloc[0]),
                'market_volatility': float(df['market_volatility'].iloc[0]),
                'complexity': float(df['complexity'].iloc[0])
            }
            
            # Determine market outlook based on multiple factors
            market_outlook = self._determine_market_outlook(characteristics)
            
            # Determine risk level based on multiple factors
            risk_level = self._determine_risk_level(characteristics)
            
            # Determine sentiment based on multiple factors
            sentiment = self._determine_sentiment(characteristics)
            
            return {
                'score': max(0, min(100, feasibility_score)),
                'market_outlook': market_outlook,
                'risk_level': risk_level,
                'sentiment': sentiment
            }
        except Exception as e:
            print(f"Error assessing feasibility: {str(e)}")
            return {
                'score': 0,
                'market_outlook': 'Unknown',
                'risk_level': 'Unknown',
                'sentiment': 'Unknown'
            }
    
    def _assess_complexity(self, idea):
        """Assess the complexity of implementing the idea"""
        complexity_keywords = {
            'high': ['AI', 'machine learning', 'artificial intelligence', 'cybersecurity', 'blockchain'],
            'medium': ['platform', 'software', 'system', 'cloud', 'digital'],
            'low': ['consulting', 'service', 'training', 'education']
        }
        
        idea_lower = idea.lower()
        for level, keywords in complexity_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                return {'high': 0.3, 'medium': 0.6, 'low': 0.9}[level]
        return 0.6  # Default to medium complexity
    
    def _assess_competition(self, idea):
        """Assess the level of market competition"""
        competition_keywords = {
            'high': ['software', 'platform', 'system', 'CRM', 'management'],
            'medium': ['consulting', 'service', 'training', 'education'],
            'low': ['specialized', 'niche', 'unique', 'innovative']
        }
        
        idea_lower = idea.lower()
        for level, keywords in competition_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                return {'high': 0.3, 'medium': 0.6, 'low': 0.9}[level]
        return 0.6  # Default to medium competition
    
    def _assess_ethical_impact(self, idea):
        """Assess the ethical impact and potential negative consequences of the idea"""
        negative_keywords = {
            'high_risk': ['bankrupt', 'scam', 'fraud', 'deceptive', 'harmful', 'dangerous', 'illegal', 'bad way'],
            'medium_risk': ['controversial', 'unethical', 'exploitative', 'manipulative', 'risky'],
            'low_risk': ['questionable', 'borderline', 'uncertain']
        }
        
        positive_keywords = {
            'high_benefit': ['sustainable', 'ethical', 'helpful', 'beneficial', 'improve', 'support', 'efficiently'],
            'medium_benefit': ['efficient', 'convenient', 'innovative', 'modern', 'manage'],
            'low_benefit': ['basic', 'standard', 'traditional']
        }
        
        idea_lower = idea.lower()
        
        # Check for negative impact first
        for level, keywords in negative_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                if level == 'high_risk':
                    return 0.0  # Extremely negative impact
                elif level == 'medium_risk':
                    return 0.2  # Very negative impact
                else:
                    return 0.3  # Negative impact
        
        # Check for positive impact
        for level, keywords in positive_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                if level == 'high_benefit':
                    return 0.9  # Very positive impact
                elif level == 'medium_benefit':
                    return 0.7  # Positive impact
                else:
                    return 0.5  # Slightly positive impact
        
        return 0.5  # Neutral default
    
    def _assess_scalability(self, idea):
        """Assess the scalability potential of the idea"""
        scalability_keywords = {
            'high': ['software', 'platform', 'system', 'cloud', 'digital'],
            'medium': ['consulting', 'service', 'training'],
            'low': ['local', 'physical', 'brick-and-mortar']
        }
        
        idea_lower = idea.lower()
        for level, keywords in scalability_keywords.items():
            if any(keyword in idea_lower for keyword in keywords):
                return {'high': 0.9, 'medium': 0.6, 'low': 0.3}[level]
        return 0.6  # Default to medium scalability
    
    def _determine_market_outlook(self, characteristics):
        """Determine market outlook based on multiple factors"""
        trend = characteristics['market_trend']
        sentiment = characteristics['sentiment']
        competition = characteristics['market_competition']
        ethical_impact = characteristics['ethical_impact']
        
        # Calculate weighted outlook score with ethical impact
        outlook_score = (trend * 0.3 + sentiment * 0.3 + competition * 0.2 + ethical_impact * 0.2)
        
        if outlook_score > 0.6:
            return 'Very Positive'
        elif outlook_score > 0.2:
            return 'Positive'
        elif outlook_score > -0.2:
            return 'Neutral'
        elif outlook_score > -0.6:
            return 'Negative'
        else:
            return 'Very Negative'
    
    def _determine_risk_level(self, characteristics):
        """Determine risk level based on multiple factors"""
        volatility = characteristics['market_volatility']
        complexity = characteristics['complexity']
        competition = characteristics['market_competition']
        ethical_impact = characteristics['ethical_impact']
        
        # Calculate weighted risk score with ethical impact
        risk_score = (volatility * 0.3 + complexity * 0.2 + competition * 0.2 + (1 - ethical_impact) * 0.3)
        
        if risk_score > 0.7:
            return 'Very High'
        elif risk_score > 0.4:
            return 'High'
        elif risk_score > 0.2:
            return 'Moderate'
        elif risk_score > 0.1:
            return 'Low'
        else:
            return 'Very Low'
    
    def _determine_sentiment(self, characteristics):
        """Determine sentiment based on multiple factors"""
        news_sentiment = characteristics['sentiment']
        market_trend = characteristics['market_trend']
        competition = characteristics['market_competition']
        ethical_impact = characteristics['ethical_impact']
        
        # Calculate weighted sentiment score with ethical impact
        sentiment_score = (news_sentiment * 0.3 + market_trend * 0.2 + competition * 0.2 + ethical_impact * 0.3)
        
        if sentiment_score > 0.6:
            return 'Very Positive'
        elif sentiment_score > 0.2:
            return 'Positive'
        elif sentiment_score > -0.2:
            return 'Neutral'
        elif sentiment_score > -0.6:
            return 'Negative'
        else:
            return 'Very Negative' 