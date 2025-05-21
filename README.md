# HomeDecide - Rent vs. Buy Comparator

![HomeDecide Screenshot](https://via.placeholder.com/800x450.png?text=HomeDecide+Rent+vs+Buy+Comparator)

## 🏠 Live Demo

Try HomeDecide live at: [https://nedwithnohead-homedecide--8501.prod1a.defang.dev/](https://nedwithnohead-homedecide--8501.prod1a.defang.dev/)

## 📋 Overview

HomeDecide is a data-driven web application that helps users make informed decisions about whether to rent or buy a home. By comparing the long-term financial implications of both options, HomeDecide provides personalized insights based on location, income, and financial preferences.

### Key Features

- **Comprehensive Cost Comparison**: Analyzes the total costs of renting versus buying over time
- **Realistic Financial Modeling**: Accounts for mortgage payments, property taxes, maintenance, rent increases, and investment returns
- **Break-Even Analysis**: Calculates when buying becomes more economical than renting
- **Canadian Market Focus**: Optimized with data for major Canadian cities, including Vancouver and Toronto
- **Interactive Visualizations**: Easy-to-understand charts and metrics to compare options
- **Detailed Cost Breakdown**: Complete transparency into all cost components

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/homedecide.git
   cd homedecide
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

### Using Docker

For a containerized setup:

1. Build and run using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Access the application at `http://localhost:8501`

## 🔧 How It Works

HomeDecide performs complex financial calculations to compare the total cost of renting versus buying over a specified time period:

### Buying Calculation Features

- **Mortgage Amortization**: Accurately tracks principal and interest payments month by month
- **Property Tax**: Calculates increasing property taxes based on home appreciation
- **Maintenance Costs**: Accounts for increasing maintenance costs over time
- **Home Appreciation**: Models realistic home value growth with appropriate caps
- **Selling Costs**: Optionally includes realtor fees and closing costs when selling

### Renting Calculation Features

- **Rent Increases**: Models annual rent increases based on market trends
- **Investment Returns**: Calculates potential returns if down payment money was invested instead
- **Opportunity Costs**: Considers the true economic comparison between options

### Break-Even Analysis

The application performs a year-by-year comparison of the net economic position of buying versus renting to determine when (if ever) buying becomes more economical than renting.

## 🧰 Project Structure

```
homedecide/
├── app.py                # Main Streamlit application
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── calculations.py   # Financial calculation functions
│   └── data_handler.py   # Data processing functions
├── data/                 # Data files 
│   └── rent_data.csv     # Rent data for different cities
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── requirements.txt      # Python dependencies
```

## 📊 Example Use Cases

### First-Time Home Buyers
HomeDecide helps first-time buyers understand if they're financially ready to purchase by comparing their current rent to potential mortgage payments and associated costs.

### Relocating to a New City
Users considering a move to Vancouver or Toronto can evaluate whether renting or buying makes more sense in these high-cost markets.

### Financial Planning
The tool helps users plan for the future by showing the long-term financial implications of their housing decisions.

## 🔨 Advanced Customization

Users can adjust various parameters to create personalized scenarios:

- **Property tax rates**: Customize based on specific municipalities
- **Maintenance costs**: Adjust based on property age and condition
- **Investment return rates**: Model different investment strategies
- **Home appreciation**: Create optimistic or conservative scenarios
- **Selling costs**: Include or exclude when planning to stay long-term

## 📈 Technical Details

### Calculation Methodology

HomeDecide uses a comprehensive financial model that includes:

1. **Mortgage Calculation**: Standard PMT formula with monthly compounding
2. **Equity Build-Up**: Tracks principal payments and home appreciation
3. **Opportunity Cost**: Time value of money principles for down payment investments
4. **Inflation Adjustment**: Compounding increases for rent, property taxes, and maintenance

### Data Sources

- Rental data is sourced from a curated dataset of major Canadian cities
- Property tax rates reflect current municipal rates
- Appreciation and return rates are based on historical averages

## 🔮 Future Development

Planned features for upcoming versions:

- Interactive neighborhood map and price visualization
- Tax savings calculator (including principal residence exemption)
- Custom inflation scenarios
- Downloadable PDF reports
- Multiple property comparison
- Investment return calculator with various portfolio models

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Streamlit for the interactive web framework
- Plotly for data visualization
- Canadian real estate data sources for benchmark information

---

### Disclaimer

HomeDecide is for educational purposes only and does not constitute financial advice. Users should consult with a qualified financial advisor before making important financial decisions.
