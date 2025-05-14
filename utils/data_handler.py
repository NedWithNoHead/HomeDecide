import pandas as pd

def load_rent_data():
    """Load rent data from CSV file"""
    try:
        return pd.read_csv("data/rent_data.csv")
    except Exception as e:
        print(f"Error loading rent data: {e}")
        return pd.DataFrame(columns=["city", "bedrooms", "average_rent"])

def get_average_rent(city, bedrooms):
    """Get average rent for a specific city and bedroom count"""
    rent_data = load_rent_data()
    
    if rent_data.empty:
        return None
    
    filtered_data = rent_data[(rent_data["city"] == city) & (rent_data["bedrooms"] == bedrooms)]
    
    if filtered_data.empty:
        # If exact match not found, try to find closest match
        city_data = rent_data[rent_data["city"] == city]
        if not city_data.empty:
            closest_bedroom = city_data.iloc[(city_data["bedrooms"] - bedrooms).abs().argsort()[0]]
            return closest_bedroom["average_rent"]
        return None
    
    return filtered_data.iloc[0]["average_rent"]

def get_available_cities():
    """Get list of available cities in the data"""
    rent_data = load_rent_data()
    return sorted(rent_data["city"].unique().tolist())