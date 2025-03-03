# Source code for the survey simulation

This directory contains the Python implementation of the survey data simulation engine. The code generates synthetic market research data with realistic demographic distributions, behavioral patterns, and correlated response variables.

## Key Components

- **Demographic Generation Functions**: Functions like `pick_gender()`, `pick_age()`, and `pick_province()` that create realistic Canadian population distributions
- **Response Simulation Functions**: Functions that model survey response patterns with appropriate statistical distributions
- **Correlation Management**: The `adjust_brandx_ratings()` function ensures logical relationships between brand familiarity, consideration, and recommendation scores
- **Respondent Generation**: Functions that create complete or terminated survey respondents with appropriate demographic and behavioral attributes
- **Exposure Group Logic**: Implementation of advertising exposure control that deterministically assigns respondents to test and control groups

## Technical Implementation

The simulation uses NumPy's random functions with precisely calibrated probability distributions to create realistic data points. The code employs conditional probability to establish correlations between variables (e.g., higher brand familiarity leads to higher consideration scores), while maintaining appropriate statistical noise.

The core function `generate_dataset()` produces a complete dataset of 1,065 respondents with:
- 500 exposed respondents
- 500 control respondents
- 15 outliers (with suspicious patterns)
- 50 terminated/incomplete respondents

Each respondent is represented as a dictionary of attributes, which are then collected into a Pandas DataFrame and can be exported to CSV format.
