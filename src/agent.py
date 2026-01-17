import os
import random

# Keyword Matching RAG Agent (Optimized for Windows Compatibility)
# This module replaces the heavy LangChain/Torch based engine to avoid DLL load errors on standard Windows environments.
# It performs direct keyword search on the local knowledge base text files.

def get_rag_docs_path():
    # Robust path finding relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path: src/../rag_docs -> root/rag_docs
    return os.path.join(base_dir, "..", "rag_docs")

def simple_retrieve(keywords):
    docs_path = get_rag_docs_path()
    results = []
    
    if not os.path.exists(docs_path):
        return ["Knowledge base directory not found locally."]

    # Iterate through all text files in the knowledge base
    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(docs_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        # Check if ANY of the keywords exist in the line (case-insensitive)
                        if any(k in line.lower() for k in keywords):
                            clean_line = line.strip()
                            # Add line if it's not empty and not a duplicate
                            if clean_line and clean_line not in results:
                                results.append(clean_line)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    # Return a random sample of tips to keep it dynamic, or all if few tips found
    sample_size = min(len(results), 5)
    if sample_size == 0:
        return []
        
    return random.sample(results, sample_size)

def generate_advice(breakdown, percentages, highest_source):
    # Mapping broader categories to specific search keywords for better results
    keyword_map = {
        "electricity": ["electricity", "energy", "power", "led", "solar", "appliance"],
        "transport": ["transport", "vehicle", "car", "fuel", "petrol", "diesel", "commute"],
        "food": ["food", "diet", "meat", "veg", "vegetarian", "eat"],
        "waste": ["waste", "plastic", "recycle", "compost", "landfill"],
        "water": ["water", "rainwater", "shower", "tap"]
    }
    
    # Get keywords for the highest emission source
    search_terms = keyword_map.get(highest_source, [highest_source])
    
    # Retrieve tips from knowledge base
    tips = simple_retrieve(search_terms)
    
    if tips:
        formatted_tips = "\n".join([f"- {tip}" for tip in tips])
    else:
        formatted_tips = "- Consider conducting a detailed energy audit for more specific insights."

    response = f"""
**Insight for {highest_source.capitalize()} ({percentages[highest_source]}% of total):**

Based on your local knowledge base:
{formatted_tips}

*(Note: Using optimized keyword search due to environment limits.)*
"""
    return response
def explain_decision(breakdown, percentages, highest_source):
    explanation = f"""
Why did the AI select {highest_source} as the main problem?

Because:
{highest_source.capitalize()} produces {breakdown[highest_source]} kg CO₂ per month,
which is {percentages[highest_source]}% of your total carbon footprint.

The AI compares all categories:
- Electricity
- Transport
- Food
- Waste
- Water

And chooses the one with the highest percentage as the priority for reduction.
"""
    return explanation

def generate_actionable_steps(breakdown, percentages, highest_source):
    # Dynamic steps based on the category
    actions = {
        "electricity": [
            "**Immediately:** Unplug devices not in use (phantom power).",
            "**This Week:** Replace incandescent bulbs with LEDs.",
            "**Long Term:** Invest in 5-star rated appliances or rooftop solar."
        ],
        "transport": [
            "**Immediately:** Check tire pressure for better mileage.",
            "**This Week:** Carpool or use public transport for one commute.",
            "**Long Term:** Switch to an Electric Vehicle (EV) or a hybrid."
        ],
        "food": [
            "**Immediately:** Incorporate one meat-free meal per day.",
            "**This Week:** Buy locally sourced vegetables to cut food miles.",
            "**Long Term:** Shift to a predominantly plant-based diet."
        ],
        "waste": [
            "**Immediately:** Start segregating dry and wet waste.",
            "**This Week:** Carry a reusable bag and water bottle everywhere.",
            "**Long Term:** Start home composting for organic waste."
        ],
        "water": [
            "**Immediately:** Turn off the tap while brushing teeth.",
            "**This Week:** Fix any leaking taps or pipes.",
            "**Long Term:** Install rainwater harvesting systems."
        ]
    }
    
    steps_list = actions.get(highest_source, ["Reduce consumption where possible."])
    formatted_steps = "\n".join([f"- {step}" for step in steps_list])
    
    return formatted_steps
