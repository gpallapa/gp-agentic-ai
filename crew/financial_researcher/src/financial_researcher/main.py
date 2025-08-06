#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from financial_researcher.crew import FinancialResearcher

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the research crew.
    """
    inputs = {
        'company': 'Scotiabank'
    }

    # Create and run the crew
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print(f"\n\nReport has been saved to output/{inputs['company']}_report.md")

if __name__ == "__main__":
    run()