import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.calculations import (
    calculate_mortgage_payment, 
    calculate_affordability,
    get_affordability_status,
    calculate_total_buying_cost,
    calculate_total_renting_cost
)
from utils.data_handler import get_average_rent, get_available_cities

# Page configuration
st.set_page_config(
    page_title="HomeDecide - Rent vs. Buy Comparator",
    page_icon="🏠",
    layout="wide"
)

# Title and description
st.title("🏠 HomeDecide - Rent vs. Buy Comparator")
st.markdown("""
Compare the long-term costs of renting versus buying a home with data-driven insights.
This tool helps you make an informed decision based on your financial situation.
""")

st.markdown("---")

# Disclaimer
with st.expander("⚠️ Disclaimer"):
    st.markdown("""
    **Not Financial Advice**: The information provided by this tool is for educational purposes only. 
    It's not intended to be financial advice. Please consult with a qualified financial advisor 
    before making any important financial decisions.
    """)

# Main inputs
st.header("📝 Your Information")

# User information
col1, col2 = st.columns(2)

with col1:
    monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)

with col2:
    city = st.selectbox("City", options=get_available_cities())

# Main layout - Two columns for Buy vs Rent
buy_col, rent_col = st.columns(2)

# Buy inputs
with buy_col:
    st.subheader("🛒 Buying a Home")
    
    home_price = st.number_input("Home Price ($)", 
                            min_value=50000, 
                            max_value=5000000,  # Increased max for Canadian market
                            value=750000,  # More realistic starting value for Vancouver/Toronto
                            step=25000,
                            format="%d")
    st.caption(f"${home_price:,}")  # Show formatted value for clarity
    
    down_payment_percent = st.slider("Down Payment (%)", min_value=5, max_value=50, value=20, step=1)
    down_payment = home_price * down_payment_percent / 100
    st.write(f"Down Payment Amount: ${down_payment:,.2f}")
    
    interest_rate = st.slider("Interest Rate (%)", min_value=1.0, max_value=10.0, value=5.5, step=0.1)
    loan_term_years = st.slider("Loan Term (Years)", min_value=10, max_value=30, value=25, step=5)
    
    # Advanced buying inputs
    with st.expander("Advanced Options"):
        property_tax_rate = st.slider("Property Tax Rate (%/year)", min_value=0.0, max_value=5.0, value=0.7, step=0.1)
        st.caption("Canadian property tax rates typically range from 0.5% to 1.5%")
        
        maintenance_cost = st.slider("Annual Maintenance Cost ($)", min_value=0, max_value=15000, value=5000, step=250)
        st.caption("Typically 1-3% of home value annually")
        
        appreciation_rate = st.slider("Expected Home Appreciation (%/year)", min_value=0.0, max_value=8.0, value=3.0, step=0.1)
        st.caption("Historical average in Canada is around 3-4%")
        
        include_selling_costs = st.checkbox("Include selling costs", value=True)
        if include_selling_costs:
            selling_cost_percent = st.slider("Selling Costs (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
            st.caption("Includes realtor fees, legal fees, and other closing costs")
        else:
            selling_cost_percent = 0.0

# Rent inputs
with rent_col:
    st.subheader("🏢 Renting a Home")
    
    bedrooms = st.slider("Number of Bedrooms", min_value=1, max_value=4, value=2, step=1)
    
    # Get average rent for the selected city and bedrooms
    avg_rent = get_average_rent(city, bedrooms)
    
    if avg_rent is not None:
        st.write(f"Average Rent in {city} for {bedrooms} bedroom(s): ${avg_rent:,.2f}")
        monthly_rent = st.number_input("Monthly Rent ($)", min_value=0, max_value=10000, value=avg_rent, step=100)
        st.caption(f"${monthly_rent:,}")
    else:
        st.warning(f"No rent data available for {city} with {bedrooms} bedroom(s).")
        monthly_rent = st.number_input("Monthly Rent ($)", min_value=0, max_value=10000, value=1800, step=100)
        st.caption(f"${monthly_rent:,}")
    
    # Advanced renting inputs
    with st.expander("Advanced Options"):
        rent_increase_rate = st.slider("Expected Annual Rent Increase (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
        st.caption("Historical average in Canada is around 2-5%")
        
        investment_return_rate = st.slider("Expected Investment Return Rate (%)", min_value=0.0, max_value=12.0, value=5.0, step=0.1)
        st.caption("This represents the opportunity cost of using money for a down payment")

# Calculate button
if st.button("📊 Calculate Comparison", type="primary"):
    # Calculate mortgage payment
    loan_amount = home_price - down_payment
    monthly_mortgage = calculate_mortgage_payment(loan_amount, interest_rate, loan_term_years)
    
    # Calculate affordability
    mortgage_affordability = calculate_affordability(monthly_mortgage, monthly_income)
    rent_affordability = calculate_affordability(monthly_rent, monthly_income)
    
    # Get affordability status
    mortgage_status, mortgage_color = get_affordability_status(mortgage_affordability)
    rent_status, rent_color = get_affordability_status(rent_affordability)
    
    # Calculate total costs with more realistic models
    # Monthly property tax and maintenance
    monthly_property_tax = home_price * property_tax_rate / 100 / 12
    monthly_maintenance = maintenance_cost / 12
    total_monthly_buying = monthly_mortgage + monthly_property_tax + monthly_maintenance
    
    # BUYING COST CALCULATION - IMPROVED
    
    # Cap appreciation rate for realism
    capped_appreciation_rate = min(appreciation_rate, 4.0)
    
    # Initial costs
    total_buying_cost = down_payment
    
    # Calculate cumulative buying costs with increasing property tax and maintenance
    cumulative_buying_cost = 0
    current_home_value = home_price
    current_property_tax = monthly_property_tax * 12
    current_maintenance = maintenance_cost
    
    for year in range(loan_term_years):
        # Add mortgage payments for the year
        cumulative_buying_cost += monthly_mortgage * 12
        
        # Add property tax for the year (increases with property value)
        current_property_tax = current_home_value * property_tax_rate / 100
        cumulative_buying_cost += current_property_tax
        
        # Add maintenance costs (increases with inflation/property value)
        current_maintenance = maintenance_cost * (1 + min(capped_appreciation_rate, 2.0) / 100) ** year
        cumulative_buying_cost += current_maintenance
        
        # Update home value for next year
        current_home_value *= (1 + capped_appreciation_rate / 100)
    
    # Total buying cost includes initial down payment
    total_buying_cost = down_payment + cumulative_buying_cost
    
    # Calculate final home value with more realistic model
    final_home_value = home_price
    for year in range(loan_term_years):
        final_home_value *= (1 + capped_appreciation_rate / 100)
    
    # Apply a modest discount factor for long-term projections
    if loan_term_years > 20:
        discount_factor = 0.95  # 5% discount for long-term projections
        final_home_value *= discount_factor
    
    # Include selling costs if selected
    selling_costs = 0
    if include_selling_costs:
        selling_costs = final_home_value * selling_cost_percent / 100
    
    # Net proceeds from home sale
    net_home_sale_proceeds = final_home_value - selling_costs
    
    # RENTING COST CALCULATION - IMPROVED
    
    # Calculate renting costs with compounding rent increases
    total_renting_cost = 0
    current_rent = monthly_rent
    
    for year in range(loan_term_years):
        annual_rent = current_rent * 12
        total_renting_cost += annual_rent
        current_rent *= (1 + rent_increase_rate / 100)
    
    # Calculate opportunity cost/benefit of down payment investment
    investment_value = down_payment
    for year in range(loan_term_years):
        investment_value *= (1 + investment_return_rate / 100)
    
    # Investment gain (how much extra money the renter has from investing)
    investment_gain = investment_value - down_payment
    
    # Adjusted renting cost (total rent paid minus investment gains)
    adjusted_renting_cost = total_renting_cost - investment_gain
    
    # Net buying cost (all costs minus what you get from selling the home)
    net_buying_cost = total_buying_cost - net_home_sale_proceeds
    
    # Display results
    st.header("🔍 Results")
    
    # Monthly costs
    st.subheader("Monthly Costs")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Monthly Mortgage Payment", 
            value=f"${monthly_mortgage:.2f}",
            delta=f"{mortgage_affordability:.1f}% of income"
        )
        st.markdown(f"<p style='color:{mortgage_color};font-weight:bold;'>{mortgage_status}</p>", unsafe_allow_html=True)
        st.caption(f"Additional monthly costs: Property tax: ${monthly_property_tax:.2f}, Maintenance: ${monthly_maintenance:.2f}")
        st.caption(f"Total monthly cost: ${total_monthly_buying:.2f}")
    
    with col2:
        st.metric(
            label="Monthly Rent", 
            value=f"${monthly_rent:.2f}",
            delta=f"{rent_affordability:.1f}% of income"
        )
        st.markdown(f"<p style='color:{rent_color};font-weight:bold;'>{rent_status}</p>", unsafe_allow_html=True)
        st.caption("No additional ownership costs, but no equity building")
    
    # Long-term comparison
    st.subheader(f"Long-term Comparison (Over {loan_term_years} Years)")
    
    # Create chart data for the cost comparison
    labels = [
        'Buying (Total Cost)', 
        'Buying (Net Cost\nafter Home Sale)', 
        'Renting (Total)', 
        'Renting (After\nInvestment Returns)'
    ]
    values = [
        total_buying_cost, 
        net_buying_cost, 
        total_renting_cost, 
        adjusted_renting_cost
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            text=[f"${val:,.0f}" for val in values],
            textposition='auto',
            marker_color=['#1f77b4', '#2ca02c', '#d62728', '#9467bd']
        )
    ])
    
    fig.update_layout(
        title=f"Cost Comparison over {loan_term_years} Years",
        xaxis_title="Option",
        yaxis_title="Total Cost ($)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Final Home Value", f"${final_home_value:,.2f}")
        st.caption(f"Initial: ${home_price:,.2f} | Appreciation: {capped_appreciation_rate:.1f}%/year")
        if include_selling_costs:
            st.caption(f"Selling costs: ${selling_costs:,.2f} ({selling_cost_percent}%)")
            st.caption(f"Net proceeds: ${net_home_sale_proceeds:,.2f}")
    
    with col2:
        if net_buying_cost < adjusted_renting_cost:
            savings = adjusted_renting_cost - net_buying_cost
            percentage_saved = (savings / adjusted_renting_cost) * 100 if adjusted_renting_cost > 0 else 0
            st.metric("Savings from Buying", f"${savings:,.2f}")
            st.caption(f"{percentage_saved:.1f}% saved compared to renting")
        else:
            savings = net_buying_cost - adjusted_renting_cost
            percentage_saved = (savings / net_buying_cost) * 100 if net_buying_cost > 0 else 0
            st.metric("Savings from Renting", f"${savings:,.2f}")
            st.caption(f"{percentage_saved:.1f}% saved compared to buying")
    
    with col3:
        # CORRECTED BREAK-EVEN CALCULATION
        years_to_break_even = None
        
        # Initialize tracking variables
        current_home_value = home_price
        current_loan_balance = home_price - down_payment
        current_rent = monthly_rent
        
        # Track cumulative costs (out of pocket)
        out_of_pocket_buying = down_payment  # Initial costs include down payment
        out_of_pocket_renting = 0
        investment_value = down_payment  # Initial investment value equals down payment
        
        # Calculate variables for mortgage amortization
        monthly_rate = interest_rate / 100 / 12
        
        # Track for detailed breakdown
        cumulative_mortgage = 0
        cumulative_property_tax = 0
        cumulative_maintenance = 0
        
        # Year-by-year comparison
        for year in range(1, loan_term_years + 1):
            # BUYING: Calculate annual costs
            annual_mortgage = monthly_mortgage * 12
            annual_property_tax = current_home_value * property_tax_rate / 100
            annual_maintenance = maintenance_cost * (1 + min(capped_appreciation_rate, 2.0) / 100) ** (year - 1)
            
            # Track component costs for detailed breakdown
            cumulative_mortgage += annual_mortgage
            cumulative_property_tax += annual_property_tax
            cumulative_maintenance += annual_maintenance
            
            # Update out-of-pocket costs for buying
            out_of_pocket_buying += annual_mortgage + annual_property_tax + annual_maintenance
            
            # Calculate approximate principal and interest for the year
            annual_interest = 0
            annual_principal = 0
            
            # For each month in the year, calculate principal and interest properly
            for month in range(12):
                if current_loan_balance > 0:
                    interest_payment = current_loan_balance * monthly_rate
                    principal_payment = min(monthly_mortgage - interest_payment, current_loan_balance)
                    
                    annual_interest += interest_payment
                    annual_principal += principal_payment
                    
                    current_loan_balance = max(0, current_loan_balance - principal_payment)
            
            # Update home value with appreciation
            current_home_value *= (1 + capped_appreciation_rate / 100)
            
            # RENTING: Calculate annual costs
            annual_rent = current_rent * 12
            out_of_pocket_renting += annual_rent
            
            # Update rent for next year
            current_rent *= (1 + rent_increase_rate / 100)
            
            # Update investment value
            investment_value *= (1 + investment_return_rate / 100)
            
            # Calculate net economic positions
            home_equity = current_home_value - current_loan_balance
            
            # If selling at this point
            selling_costs = current_home_value * selling_cost_percent / 100 if include_selling_costs else 0
            net_proceeds_from_sale = home_equity - selling_costs
            
            # Real economic positions - what you've paid minus what you'd get back
            buying_position = out_of_pocket_buying - net_proceeds_from_sale
            renting_position = out_of_pocket_renting - (investment_value - down_payment)
            
            # Check if buying becomes better than renting
            # A lower position is better (less net cost)
            if buying_position < renting_position and years_to_break_even is None:
                years_to_break_even = year
        
        if years_to_break_even:
            st.metric("Break-even Year", f"Year {years_to_break_even}")
            st.caption(f"Buying becomes more economical after {years_to_break_even} years")
        else:
            st.metric("Break-even Year", "Never (in this time period)")
            st.caption("Renting remains more economical throughout the period")
    
    # Summary and detailed breakdown
    st.subheader("Summary")
    
    if net_buying_cost < adjusted_renting_cost:
        st.success(f"""
        **Buying appears to be more economical over {loan_term_years} years.**
        
        After accounting for home appreciation and the opportunity cost of your down payment,
        buying is projected to save you ${adjusted_renting_cost - net_buying_cost:,.2f} compared to renting.
        """)
    else:
        st.info(f"""
        **Renting appears to be more economical over {loan_term_years} years.**
        
        After accounting for home appreciation and the opportunity cost of your down payment,
        renting is projected to save you ${net_buying_cost - adjusted_renting_cost:,.2f} compared to buying.
        """)
    
    # Detailed breakdown
    with st.expander("See Detailed Breakdown"):
        st.markdown("### Buying Costs")
        st.markdown(f"- **Down Payment:** ${down_payment:,.2f}")
        st.markdown(f"- **Mortgage Payments (over {loan_term_years} years):** ${cumulative_mortgage:,.2f}")
        st.markdown(f"- **Property Taxes (over {loan_term_years} years, increasing with property value):** ${cumulative_property_tax:,.2f}")
        st.markdown(f"- **Maintenance (over {loan_term_years} years, increasing with inflation):** ${cumulative_maintenance:,.2f}")
        st.markdown(f"- **Total Buying Costs:** ${total_buying_cost:,.2f}")
        st.markdown(f"- **Home Value After {loan_term_years} years:** ${final_home_value:,.2f}")
        if include_selling_costs:
            st.markdown(f"- **Selling Costs ({selling_cost_percent}%):** ${selling_costs:,.2f}")
            st.markdown(f"- **Net Proceeds from Home Sale:** ${net_home_sale_proceeds:,.2f}")
        st.markdown(f"- **Net Buying Cost:** ${net_buying_cost:,.2f}")
        
        st.markdown("### Renting Costs")
        st.markdown(f"- **Total Rent Payments (over {loan_term_years} years, with {rent_increase_rate}% annual increases):** ${total_renting_cost:,.2f}")
        st.markdown(f"- **Investment Value of Down Payment After {loan_term_years} years ({investment_return_rate}% return):** ${investment_value:,.2f}")
        st.markdown(f"- **Investment Gain:** ${investment_value - down_payment:,.2f}")
        st.markdown(f"- **Net Renting Cost (after investment returns):** ${adjusted_renting_cost:,.2f}")
    
    # Email results button (placeholder for future functionality)
    st.button("📧 Email These Results", disabled=True)
    st.info("Email functionality will be available in the next version.")

# Future features
st.markdown("---")
st.subheader("Coming Soon in V2:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - Interactive neighborhood map
    - Tax savings calculator
    - Custom inflation scenarios
    """)

with col2:
    st.markdown("""
    - Downloadable PDF reports
    - Multiple property comparison
    - Investment return calculator
    """)

# Footer
st.markdown("---")
st.caption("HomeDecide - Rent vs. Buy Comparator | Not Financial Advice")