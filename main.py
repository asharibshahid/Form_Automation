import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled , function_tool
import os
import dotenv

import json
import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

dotenv.load_dotenv()

class FullClientData(BaseModel):
    full_name: str
    last_name: str
    reference: str
    phone_number: str
    business_description: str
    best_selling_products: str
    problem_solved: str
    unique_selling_point: str
    main_competitors: str
    customer_results: str
    selling_method: str
    revenue_year1: int
    revenue_year2: int
    revenue_year3: int
    monthly_revenue: int
    profit_margin: str
    customer_lifetime_value: int
    business_location: str
    number_of_offers: int
    best_selling_offers: str
    smart_goals: str
    facebook_page: str
    facebook_group: str
    instagram: str
    website: str
    blog: str
    sales_pages: str
    monthly_visitors: str
    most_visited_pages: str
    traffic_source: str
    running_fb_ads: str
    fb_ads_budget: str
    other_campaigns: str
    marketing_software: str
    using_marketing_software: str
    pricing_expectation: str




gemini_api_key ="AIzaSyDFOyYXqDtxb9218m7o2OKJQC--jtFEFdk"

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)
from openai import OpenAI

from pydantic import BaseModel
from typing import List

# Step 1: Input schema using Pydantic
class ClientData(BaseModel):
    name: str
    email: str
    business_name: str
    industry: str
    monthly_revenue: int
    goals: str
    website: str
    pain_points: str

# Step 2: First Tool - Analyze Business Data
@function_tool
def analyze_business_data(client_data: ClientData) -> str:
    """
    Analyze the client input data and generate summary/insight.
    """
     
    return (
        f"Client {client_data.full_name} ({client_data.phone_number}) runs a business focused on {client_data.business_description}. "
        f"Their top products are: {client_data.best_selling_products}. They face challenges like: {client_data.problem_solved}. "
        f"Monthly revenue is {client_data.monthly_revenue} PKR. Goals: {client_data.smart_goals}. "
        f"We’ll use this data to craft the perfect solution."
    )
# Sample knowledge base (could be replaced by vector search or file loader)
ZAPPS_KNOWLEDGE_BASE = {
    "highlights": [
        "We provide automation solutions for e-commerce, including cart recovery, order processing, and CRM integration.",
        "Our pricing starts at 20,000 PKR/month, and includes AI-based support agents, marketing automation, and analytics.",
        "For low-revenue clients (<100k PKR), we offer lean automation models to maximize ROI without large investment."
    ],
    "pricing_plans": {
        "starter": {
            "name": "Crystal Clear Starter Plan",
            "description": "Unlocking Value for Your Healthy Food Brand",
            "features": [
                "8 Designed Posts (static/image)",
                "2 Instagram Reels (basic video editing)",
                "Captions + Hashtag Research",
                "Profile Bio Optimization",
                "Monthly Report (reach & engagement)"
            ],
            "price_pkr": "PKR 16,000 – 37,990",
            "price_usd": "$80",
            "price_sar": "SAR 500"
        },
        "growth": {
            "name": "Growth Plan",
            "description": "Ideal for businesses looking to grow audience & engagement",
            "features": [
                "8 TikTok Videos per Month",
                "Trendy Editing, Filters, Voiceover/Text",
                "Product Showcase with brand voice",
                "Custom Strategy + Bi-Weekly Report",
                "Audience Targeting & Growth Tips"
            ],
            "price_pkr": "PKR 25,000 – 75,980",
            "price_usd": "$150",
            "price_sar": "SAR 1,000"
        },
        "pro": {
            "name": "Pro Brand Plan",
            "description": "Strong online presence, high-level engagement",
            "features": [
                "12–16 Viral TikTok Videos",
                "Full Scripting + Trend Research",
                "Premium Editing with Voiceovers + Effects",
                "Brand Challenges, Skits, Influencer Collabs",
                "Hashtag Campaigns + Weekly Reports",
                "24/7 Community Management & Support"
            ],
            "price_pkr": "PKR 35,000 – 113,970",
            "price_usd": "$200",
            "price_sar": "SAR 1,500"
        }
    }
}


# Step 3: Second Tool - Generate Proposal Based on Knowledge Base
@function_tool
def generate_proposal_from_knowledge(client_data: FullClientData) -> str:
    monthly_revenue = client_data.monthly_revenue

    # Select best pricing plan based on monthly revenue
    if monthly_revenue <= 20000:
        selected_plan = "starter"
    elif monthly_revenue <= 60000:
        selected_plan = "growth"
    else:
        selected_plan = "pro"

    plan = ZAPPS_KNOWLEDGE_BASE["pricing_plans"][selected_plan]

    proposal_text = (
        f"📄 **Proposal for {client_data.full_name}**\n\n"
        f"Based on your input, we recommend:\n"
        f"Targeting your unique value: {client_data.unique_selling_point}\n"
        f" Tackling pain points: {client_data.problem_solved}\n"
        f" Monthly Revenue: {monthly_revenue:,} PKR — "
        f"our automation model is affordable for this range.\n"
        f" Business Goals: {client_data.smart_goals}\n\n"
        f"We suggest starting with:\n"
        f"- AI automation setup\n"
        f"- CRM integration\n"
        f"- Ad optimization based on your campaign info\n\n"
        f" **Estimated Cost**: PKR 20,000/month — scalable as you grow.\n"
        f"\n---\n\n"
        f"##  **Recommended Pricing Plan: {plan['name']}**\n\n"
        f"**{plan['description']}**\n\n"
        f"### 🔹 What's Included:\n"
    )

    for feat in plan["features"]:
        proposal_text += f"- {feat}\n"

    proposal_text += (
        f"\n### :Pricing:\n"
        f"- **PKR**: {plan['price_pkr']}\n"
        f"- **USD**: {plan['price_usd']}\n"
        f"- **SAR**: {plan['price_sar']}\n"
    )

    return proposal_text


@function_tool
def return_final_output(proposal: str) -> str:
    return f": Final Proposal Ready:\n\n{proposal}"












async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="ZApps Strategy Consultant",
        instructions="""
You are ZApps Consulting's premium AI Business Strategist. Generate client proposals with these guidelines:

1. **STRUCTURE:**
   - Personalized Introduction (Client name + business)
   - Business Assessment (Strengths/weaknesses based on data)
   - Revenue Analysis (Detailed breakdown with visual indicators)
   - Customized Solutions (3-5 specific strategies)
   - Pricing Plan Showcase (Visual comparison table)
   - Implementation Timeline (Phased approach)
   - Call-to-Action (Clear next steps)

2. **VISUAL FORMATTING:**
   - Use ONLY Streamlit-compatible markdown
   - Section headers: `###` level with strategic emojis (max 3 per section)
   - Pricing tables with colored headers (🔷 **Starter** 🔷)
   - Progress bars for metrics: `[█████▁▁▁▁] 60%`
   - Key metrics in **bold** with arrows ➔ 
   - Feature lists with checkmarks ✓

3. **CONTENT PRINCIPLES:**
   - Professional yet approachable tone
   - Data-driven recommendations
   - Concrete metrics and timelines
   - Competitive differentiation highlights

4. **PRICING PRESENTATION:**
ZAPPS_KNOWLEDGE_BASE = {
   - all plans are stored in  in this pleas e use it to generate the pricing plan
and all kind of pricing plans are stored in the ZAPPS_KNOWLEDGE_BASE variable
5. **BUSINESS ANALYSIS:**
   - Categorize by revenue: Startup (<50k), Growth (50-200k), Enterprise (200k+)
   - Identify 2 core strengths + 2 improvement areas
   - Map all recommendations to client's SMART goals

5. **DATA UTILIZATION:**
    - Use all provided client data fields
    - Analyze business health, market position, and competitive landscape
    - Generate insights from client inputs and ZAPPS_KNOWLEDGE_BASE
6. **OUTPUT FORMAT:**
    - Return a single string with the complete proposal
    - Use Streamlit markdown formatting for rendering
    - No emojis in the final output, only in section headers
    must be in 50 lines or more
Use all tools to analyze data and generate proposal components before final assembly.
""",
        tools=[
            analyze_business_data,
            generate_proposal_from_knowledge,
            return_final_output
        ],
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Generate EXTREME premium proposal using ALL client data. Include: "
        "1. Business health dashboard 2. Competitor gap analysis "
        "3. Customized solution matrix 4. Luxury pricing presentation "
        "5. Implementation roadmap. Format for Streamlit rendering with visual hierarchy. But withouot an single emoji ",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
