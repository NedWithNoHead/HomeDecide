def calculate_mortgage_payment(loan_amount, interest_rate, loan_term_years):
    """
    Calculate monthly mortgage payment using the PMT formula
    
    Parameters:
    loan_amount (float): The total loan amount
    interest_rate (float): Annual interest rate (in percentage)
    loan_term_years (int): Loan term in years
    
    Returns:
    float: Monthly mortgage payment
    """
    if interest_rate == 0:
        return loan_amount / (loan_term_years * 12)
    
    monthly_rate = interest_rate / 100 / 12
    months = loan_term_years * 12
    
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return monthly_payment

def calculate_affordability(monthly_payment, monthly_income):
    """
    Calculate affordability as percentage of income
    
    Parameters:
    monthly_payment (float): Monthly payment (rent or mortgage)
    monthly_income (float): Monthly income
    
    Returns:
    float: Affordability percentage
    """
    if monthly_income == 0:
        return float('inf')
    
    return (monthly_payment / monthly_income) * 100

def get_affordability_status(affordability_percentage):
    """
    Get affordability status based on percentage
    
    Parameters:
    affordability_percentage (float): Affordability percentage
    
    Returns:
    tuple: (status, color)
    """
    if affordability_percentage <= 25:
        return "Affordable", "green"
    elif affordability_percentage <= 35:
        return "Borderline", "orange"
    else:
        return "Unaffordable", "red"

def calculate_total_buying_cost(home_price, down_payment, monthly_mortgage, property_tax_rate, 
                                maintenance_cost, loan_term_years, appreciation_rate):
    """
    Calculate total cost of buying over the loan term
    
    Parameters:
    home_price (float): Home price
    down_payment (float): Down payment amount
    monthly_mortgage (float): Monthly mortgage payment
    property_tax_rate (float): Annual property tax rate (percentage)
    maintenance_cost (float): Annual maintenance cost
    loan_term_years (int): Loan term in years
    appreciation_rate (float): Annual home appreciation rate (percentage)
    
    Returns:
    tuple: (total_cost, final_home_value)
    """
    # Initial costs
    total_cost = down_payment
    
    # Monthly costs over loan term
    monthly_property_tax = home_price * property_tax_rate / 100 / 12
    monthly_maintenance = maintenance_cost / 12
    
    # Total monthly payment including property tax and maintenance
    total_monthly_payment = monthly_mortgage + monthly_property_tax + monthly_maintenance
    
    # Total cost over loan term
    total_cost += total_monthly_payment * loan_term_years * 12
    
    # Final home value after appreciation
    final_home_value = home_price * (1 + appreciation_rate / 100) ** loan_term_years
    
    return total_cost, final_home_value

def calculate_total_renting_cost(monthly_rent, loan_term_years, rent_increase_rate):
    """
    Calculate total cost of renting over the loan term
    
    Parameters:
    monthly_rent (float): Initial monthly rent
    loan_term_years (int): Time period in years (same as loan term for comparison)
    rent_increase_rate (float): Annual rent increase rate (percentage)
    
    Returns:
    float: Total cost of renting
    """
    total_cost = 0
    current_rent = monthly_rent
    
    for year in range(loan_term_years):
        annual_rent = current_rent * 12
        total_cost += annual_rent
        current_rent *= (1 + rent_increase_rate / 100)
    
    return total_cost