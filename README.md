# Survey Data Simulation & Brand Marketing Analysis

## Project Overview
This repository contains a sophisticated Python-based tool that simulates realistic market research data for a brand marketing study. The code generates a structured dataset that replicates a real-world brand awareness and advertising effectiveness survey, complete with demographic distributions, exposure groups, control groups, and realistic response patterns. The simulation creates 1,065 respondent records with carefully controlled variables to enable statistically meaningful analysis of advertising impact on brand metrics.

## Key Features

- **Demographically Representative Sampling**: Implements accurate Canadian population distributions for age, gender, geographic location, and community types. The code uses actual Canadian demographic proportions (e.g., provincial population distribution, urban/suburban/rural splits) to ensure the simulated sample reflects real-world population characteristics, making analysis results more credible and applicable.

- **Complex Correlation Patterns**: Models realistic relationships between variables such as:
  - Brand familiarity and consideration: Higher familiarity scores correlate with increased consideration scores, reflecting actual consumer behavior patterns
  - Ad exposure and brand recall: Respondents with higher TV viewing frequency have higher ad recall rates and more positive brand perceptions
  - Product usage frequency and brand awareness: Frequent snack consumers show increased awareness of major brands
  - Demographic factors and purchasing behaviors: Shopping roles, presence of children, and community types influence purchasing patterns and spending levels

- **Statistical Integrity**: Maintains proper distributions while incorporating realistic noise and outliers. The simulation balances between perfect correlations (which would be unrealistic) and completely random data (which would be useless for analysis). Variables follow appropriate statistical distributions (normal, uniform, etc.) with parameters calibrated to match real-world survey response patterns.

- **Data Quality Simulation**: Includes simulated survey terminations, partial completions, and data quality issues for realistic analysis scenarios. The code generates early terminations at screening questions, straight-line responses, and extreme completion times, replicating the data cleaning challenges analysts face with real survey data.

## Technical Highlights

- **Probability-Based Sampling**: Uses weighted random sampling to create realistic demographic and response distributions. The implementation carefully applies numpy's random functions with precisely calibrated probability arrays to ensure the output data has the right statistical properties while maintaining appropriate variability.

- **Conditional Logic Patterns**: Implements complex if-then relationships mimicking human response patterns. The code models how responses to one question influence answers to subsequent questions (e.g., how brand awareness affects perception ratings), creating interdependencies that mirror genuine survey data.

- **Data Correlation Modeling**: Mathematically adjusts variables to create realistic interdependencies. The implementation includes functions like `adjust_brandx_ratings()` that apply conditional probabilities to ensure logical consistency in responses while preserving natural variability.

- **Outlier and Anomaly Generation**: Deliberately introduces edge cases for data cleaning practice. The code explicitly generates both valid outliers (genuine but unusual responses) and problematic data points (speeders, straight-liners) that would typically be identified during quality control in real survey analysis.

## Skills Demonstrated

- **Advanced Python programming with NumPy and Pandas**: The code utilizes vectorized operations, probability distributions, and efficient data structuring techniques that demonstrate mastery of scientific Python programming.

- **Statistical modeling and probability distributions**: Implementation of weighted random sampling, conditional probability, and mathematical transformations to maintain statistical properties shows strong understanding of data science fundamentals.

- **Market research methodology knowledge**: The simulation reflects deep understanding of survey design principles, question types (Likert scales, unaided vs. aided recall), sampling methods, and how to control for biases.

- **Survey design and analysis expertise**: The code models real-world survey structure including screening questions, termination logic, and the relationship between demographics, behaviors, and attitudes.

- **Data generation for testing analysis pipelines**: The simulation produces a full dataset suitable for dashboard development, statistical testing, and machine learning algorithm training with controlled experimental and control groups.

- **Documentation of complex statistical systems**: The code includes comprehensive docstrings and comments explaining the statistical reasoning behind simulation decisions, making it accessible for both technical and non-technical audiences.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/survey-data-simulation.git
cd survey-data-simulation

# Install required packages
pip install -r requirements.txt
```

## Usage

```python
# Generate a complete dataset
from src.Simulated_brandx_survey import generate_dataset

# Create the simulated dataset
df = generate_dataset()

# Save to CSV
df.to_csv("data/simulated_survey_data.csv", index=False)
```

## Project Structure

```
survey-data-simulation/
├── data/                               # Sample output data files
├── notebooks/                          # Jupyter notebooks for analysis demonstrations
├── src/                                # Source code for the simulation
│   └── Simulated_brandx_survey.py      # Main simulation code
├── README.md                           # This file
└── requirements.txt                    # Required packages
```

## Potential Applications

- **Testing data visualization dashboards**: The generated dataset provides realistic test data for developing brand tracking dashboards with key performance indicators, demographic breakdowns, and time-series capabilities.

- **Developing and validating statistical analysis methods**: The controlled exposure vs. control group design allows for testing of various statistical approaches to measuring advertising effectiveness.

- **Training junior analysts on data cleaning techniques**: The deliberately included data quality issues provide perfect examples for teaching data preparation, outlier detection, and handling of missing values.

- **Demonstrating marketing research concepts**: The dataset illustrates fundamental marketing principles like the sales funnel (awareness → consideration → recommendation) and advertising impact measurement.

This project showcases my ability to understand both the technical aspects of data science and the practical business applications in market research and brand analytics, demonstrating how technical skills can translate directly to business value.
