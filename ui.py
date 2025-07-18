import streamlit as st
from main import analyze_business_data
from agents import Agent, Runner, OpenAIChatCompletionsModel
from main import analyze_business_data, generate_proposal_from_knowledge, return_final_output
from openai import AsyncOpenAI
import os
import asyncio
import json
import pandas as pd
import os
# Page Configuration
st.set_page_config(
    page_title="ZApps Consulting | Client Business Discovery Form",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .logo-section {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
    }
    
    .company-logo {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .section-header {
        background: linear-gradient(90deg, #f7c9f3 0%, #f78f9d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .submit-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .result-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stTextInput > div > div {
        border-radius: 10px;
    }
    
    .stTextArea > div > div {
        border-radius: 10px;
    }
    
    .intro-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Logo Section
st.markdown("""
<div class="logo-section">
    <div class="company-logo">ZApps Consulting</div>
</div>
""", unsafe_allow_html=True)

# Introduction Text
st.markdown("""
<div class="intro-text">
    <strong>Hey there,</strong><br><br>
    We're excited to learn about your brand. This form helps us tailor our strategy exactly to your business, whether you're launching, growing, or scaling.<br><br>
    It's quick, and every answer helps us give you better results.<br><br>
    <strong>Thank you.</strong>
</div>
""", unsafe_allow_html=True)

# Initialize session state for form data
if 'client_data' not in st.session_state:
    st.session_state.client_data = {}

# Create form

with st.form("client_discovery_form"):
    st.subheader("All About You")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("• Your First Name *")
    with col2:
        last_name = st.text_input("• Your Last Name *")

    col3, col4 = st.columns(2)
    with col3:
        reference = st.text_input("• Reference (How did you hear about us?)")
    with col4:
        phone_number = st.text_input("• Phone Number *", placeholder="+1 (555) 123-4567")

    st.markdown("---")
    st.subheader(" Your Product and Service")
    business_description = st.text_area("• What does your business do? *")
    problem_solved = st.text_area("• What problem does your product/service solve? *")
    unique_selling_point = st.text_area("• What makes your offering unique? *")
    customer_results = st.text_area("• Typical results your customers get?")
    main_competitors = st.text_area("• Who are your main competitors?")

    st.markdown("---")
    st.subheader(" Your Business Model")

    st.markdown("• How are you currently selling your product/service?")
    sales_channels = st.multiselect(
        "Select sales channels",
        ["Physical Store", "Shopify", "Amazon", "Instagram Shop", "Other"]
    )

    monthly_revenue = st.number_input("• What is your current monthly revenue (approx.)?", min_value=0, step=500)
    profit_margin = st.number_input("• Expected annual profit margin (%)", min_value=0.0, step=0.5)

    col1, col2 = st.columns(2)
    with col1:
        customer_lifetime_value = st.text_input("•Where are You Located")
    with col2:
        business_location = st.text_input("• Where is your business mostly active? *")

    marketing_platforms = st.multiselect(
        "• Which platforms do you use for marketing?",
        ["Facebook", "Instagram", "TikTok", "LinkedIn", "YouTube", "WhatsApp", "Other"]
    )

    smart_goals = st.text_area("• Business goals for this year (SMART) (OPTIONAL)")

    st.markdown("---")
    st.subheader("Online Marketing")

    col1, col2 = st.columns(2)
    with col1:
        facebook_page = st.text_input("Facebook Page URL")
        instagram = st.text_input("Instagram Account")
    with col2:
        website = st.text_input("Website")

    monthly_visitors = st.selectbox("• Monthly website visitors (optional)", 
                                    ["Select", "Under 1k", "1k-5k", "5k-20k", "20k+", "Not Sure"])

    col3, col4 = st.columns(2)
    with col3:
        traffic_source = st.text_area("• Website traffic sources?")
    with col4:
        running_ads = st.selectbox("• Are you running any marketing campaigns or ads?", ["Select", "Yes", "No"])

    col5, col6 = st.columns(2)
    with col5:
        ad_budget = st.selectbox("• Current budget for marketing/ads", ["Select", "Low", "Normal", "High"])
    with col6:
        other_campaigns = st.text_area("• Other ongoing marketing campaigns (optional)")

    col7, col8 = st.columns(2)
    with col7:
        marketing_software = st.text_area("• Marketing software in use (optional)")
    with col8:
        using_software = st.selectbox("• Are you using any marketing software?", ["Select", "Yes", "No"])

    pricing_expectation = st.text_area("• What's your budget for marketing services?")

    submitted = st.form_submit_button(": Submit :")

    if submitted:
        client_data = {
            "First Name": full_name,
            "Last Name": last_name,
            "Reference": reference,
            "Phone Number": phone_number,
            "Business Description": business_description,
            "Problem Solved": problem_solved,
            "Unique Selling Point": unique_selling_point,
            "Customer Results": customer_results,
            "Competitors": main_competitors,
            "Sales Channels": ", ".join(sales_channels),
            "Monthly Revenue": monthly_revenue,
            "Profit Margin (%)": profit_margin,
            "CLV": customer_lifetime_value,
            "Business Location": business_location,
            "Marketing Platforms": ", ".join(marketing_platforms),
            "SMART Goals": smart_goals,
            "Facebook Page": facebook_page,
            "Instagram": instagram,
            "Website": website,
            "Monthly Visitors": monthly_visitors,
            "Traffic Sources": traffic_source,
            "Running Ads": running_ads,
            "Ad Budget": ad_budget,
            "Other Campaigns": other_campaigns,
            "Marketing Software": marketing_software,
            "Using Software": using_software,
            "Marketing Budget Expectation": pricing_expectation,
        }

        df = pd.DataFrame([client_data])

        # Save to CSV (append if exists)
        if os.path.exists("replies.csv"):
            df.to_csv("replies.csv", mode="a", header=False, index=False)
        else:
            df.to_csv("replies.csv", index=False)

        st.success("✅ Your responses have been saved to **replies.csv** successfully!")

        # Define the agent here (if not already global)
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

        client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        agent = Agent(
            name="ProposalAgent",
            instructions="""**Role:** Senior Business marketing Strategist at ZApps Consulting

**Core Objective:** Generate premium client proposals using ZAPPS_KNOWLEDGE_BASE with strategic visual enhancement

**Execution Protocol:**
1. **Data Analysis Phase:**
   - Categorize business by revenue tier using client's monthly_revenue
   - Identify 2 primary strengths and 2 critical improvement areas
   - Cross-reference all recommendations with ZAPPS_KNOWLEDGE_BASE

2. **Proposal Structure:**
   1. Executive Summary (1 paragraph)
   2. Business Health Assessment (SWOT format)
   3. Customized Solutions (Bulleted action items)
   4. Investment Analysis (Pricing table comparison)
   5. Implementation Roadmap (Phased timeline)
   6. Next Steps (Clear CTA)

3. **Visual Enhancement Rules:**
   - Use maximum 3 emojis total in entire proposal
   - doen;t use emoji
   - Apply **bold** for key metrics and pricing figures
   - Use --- for section dividers
   - Format tables with aligned columns
   - Use bullet points for features/benefits

4. **ZAPPS_KNOWLEDGE_BASE Integration:**
   - Select pricing plan based strictly on monthly_revenue:
        < 50K PKR → Starter
        50K-200K PKR → Growth
        > 200K PKR → Pro
   - Include ALL plan features from knowledge base
   - Add ROI projections based on revenue tier

5. **Tone & Content Requirements:**
   - Ultra-professional business language
   - Data-driven recommendations only
   - Quantify all projections (%, PKR, timelines)
   - Match solutions to client's smart_goals
   - Highlight competitive advantages 
   
   
   """,
            tools=[analyze_business_data, generate_proposal_from_knowledge, return_final_output],
            model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
        )

        result = asyncio.run(Runner.run(
            agent, 
            f"Please analyze this business and generate a full profesonal proposal : {json.dumps(client_data)}"
        ))

        strategy_result = result.final_output
        st.markdown(f"""
        <div style="background-color: #f9f9fb; padding: 2rem; border-radius: 16px; box-shadow: 0 0 8px rgba(0,0,0,0.05); font-family: 'Segoe UI', sans-serif;">
            <h2 style="color: #222831;">Final Strategy & Proposal</h2>
            <hr style="border: none; height: 1px; background-color: #ddd;" />
            <div style="font-size: 1rem; color: #393e46; line-height: 1.8;">
                {strategy_result.replace('\n', '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>ZApps Consulting</strong> - Transforming Businesses Through Strategic Innovation</p>
    <p><em>Thank you for trusting us with your business information. We're excited to help you grow!</em></p>
</div>
""", unsafe_allow_html=True)