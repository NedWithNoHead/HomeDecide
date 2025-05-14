# Script to generate sample data
import pandas as pd
import numpy as np

# Create sample data with Canadian cities
cities = ["Vancouver", "Toronto", "Montreal", "Calgary", "Edmonton", 
          "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Victoria"]
          
bedrooms = [1, 2, 3, 4]

data = []
for city in cities:
    for bedroom in bedrooms:
        # Generate reasonable rent prices based on Canadian city and bedroom count
        # These are in CAD$
        base_price = {
            "Vancouver": 2400, "Toronto": 2300, "Montreal": 1200, "Calgary": 1300, 
            "Edmonton": 1200, "Ottawa": 1500, "Winnipeg": 1100, 
            "Quebec City": 1000, "Hamilton": 1400, "Victoria": 1800
        }
        
        rent_price = base_price[city] + (bedroom - 1) * 600
        
        # Add some randomness
        rent_price = int(rent_price * np.random.uniform(0.9, 1.1))
        
        data.append({
            "city": city,
            "bedrooms": bedroom,
            "average_rent": rent_price
        })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("rent_data.csv", index=False)
print("Sample rent data generated successfully!")