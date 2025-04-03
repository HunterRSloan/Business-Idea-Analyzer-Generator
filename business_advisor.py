"""
Business Advisor module.
Provides high-level interface for business idea generation and assessment.
"""

from .business_generator import BusinessIdeaGenerator

class BusinessAdvisor:
    def __init__(self):
        self.idea_generator = BusinessIdeaGenerator()
        
    def get_business_recommendations(self, industry, target_market, investment_budget, target_roi):
        """Get complete business recommendations"""
        try:
            # Generate ideas
            ideas = self.idea_generator.generate_ideas(industry, target_market)
            if not ideas:
                return []
            
            # Analyze market
            self.idea_generator.analyze_market_trends(industry)
            
            recommendations = []
            for idea in ideas:
                feasibility = self.idea_generator.assess_feasibility(idea, investment_budget, target_roi)
                recommendations.append({
                    'idea': idea,
                    'feasibility': feasibility
                })
                
            # Sort by feasibility score
            recommendations.sort(key=lambda x: x['feasibility']['score'], reverse=True)
            
            return recommendations
        except Exception as e:
            print(f"Error getting business recommendations: {str(e)}")
            return []

    def assess_user_idea(self, idea, industry, investment_budget, target_roi):
        """Assess a user-provided business idea using the same criteria as generated ideas"""
        try:
            # Analyze market trends first
            self.idea_generator.analyze_market_trends(industry)
            
            # Assess feasibility of the user's idea
            feasibility = self.idea_generator.assess_feasibility(idea, investment_budget, target_roi)
            
            assessment = {
                'idea': idea,
                'feasibility': feasibility
            }
            
            print("\nAssessment of Your Business Idea:")
            print(f"Description: {assessment['idea']}")
            print(f"Feasibility Score: {assessment['feasibility']['score']:.2f}")
            print(f"Market Outlook: {assessment['feasibility']['market_outlook']}")
            print(f"Risk Level: {assessment['feasibility']['risk_level']}")
            print(f"Market Sentiment: {assessment['feasibility']['sentiment']}")
            
            return assessment
        except Exception as e:
            print(f"Error assessing user idea: {str(e)}")
            return None 