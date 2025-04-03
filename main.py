"""
Main script for the Business Idea Analyzer & Generator.
Demonstrates the usage of the BusinessIdeaGenerator class.
"""

from business_idea_analyzer import BusinessAdvisor

def main():
    # Initialize the advisor
    advisor = BusinessAdvisor()
    
    # Test case 1: Bad idea
    print("\n=== Testing Bad Idea Assessment ===")
    bad_idea = "A mobile app that helps small businesses go bankrupt by providing misleading financial advice"
    print(f"\nBad Idea: {bad_idea}")
    
    # Assess the bad idea
    bad_assessment = advisor.assess_user_idea(
        idea=bad_idea,
        industry="technology",
        investment_budget=50000,
        target_roi=0.25
    )
    
    # Test case 2: Good idea
    print("\n=== Testing Good Idea Assessment ===")
    good_idea = "A sustainable mobile app that helps small businesses manage their finances efficiently"
    print(f"\nGood Idea: {good_idea}")
    
    # Assess the good idea
    good_assessment = advisor.assess_user_idea(
        idea=good_idea,
        industry="technology",
        investment_budget=50000,
        target_roi=0.25
    )
    
    # Generate business recommendations
    print("\n=== Generating Business Recommendations ===")
    recommendations = advisor.get_business_recommendations(
        industry="technology",
        target_market="small businesses",
        investment_budget=50000,
        target_roi=0.25
    )
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            print(f"\nIdea {idx}:")
            print(f"Description: {rec['idea']}")
            print(f"Feasibility Score: {rec['feasibility']['score']:.2f}")
            print(f"Market Outlook: {rec['feasibility']['market_outlook']}")
            print(f"Risk Level: {rec['feasibility']['risk_level']}")
            print(f"Market Sentiment: {rec['feasibility']['sentiment']}")
    else:
        print("No recommendations were generated. Please check your API keys and try again.")

if __name__ == "__main__":
    main() 