# Case Study 1: Data Cleaning & Validation for E-Commerce Data

## Business Problem
An e-commerce business relies on customer and transaction data to drive decisions around marketing, retention, and customer segmentation. However, raw datasets often contain invalid values, inconsistencies, and structural issues that make analysis unreliable.

This project focuses on validating and cleaning customer and transaction data to ensure it is safe and trustworthy for downstream analytics.

## What Was Done
- Validated customer demographics (age, gender, tenure)
- Identified and handled invalid age values
- Standardized categorical fields
- Performed structural validation on transaction data
- Tested dataset join integrity and documented limitations

## Key Findings
- Over 33% of customer age values were invalid and required correction
- Transaction data was structurally clean but could not be reliably joined with customer data
- Forcing joins would have resulted in misleading analysis

## Outcome
- Clean, analytics-ready datasets
- Clear documentation of data limitations
- A reproducible validation and cleaning workflow

## Tools Used
- Python
- Pandas
- NumPy
- Jupyter Notebook
