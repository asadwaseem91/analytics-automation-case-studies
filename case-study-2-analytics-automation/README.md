# Case Study 2: Automated Customer Health & Retention Report

## Business Problem
Manual reporting of customer behavior and retention metrics is time-consuming and error-prone. Businesses need a reliable way to monitor customer health, identify churn risk, and act quickly without rebuilding reports every week.

This project automates a 30-day customer health report using Python.

## What This Automation Does
- Processes raw customer transaction data
- Generates key KPIs (overall, by country, by customer tier)
- Identifies at-risk customers based on inactivity and behavior
- Produces executive-ready CSV reports and charts
- Can be scheduled to run weekly or monthly

## Outputs
- Overall KPI summary
- KPI breakdowns by country and customer tier
- At-risk customer list
- Executive charts highlighting risk patterns

## Example Insights
- High-value customers show higher cart abandonment despite strong purchase value
- No immediate churn detected, but behavioral signals highlight future churn risk
- 184 customers flagged for proactive retention efforts

##Tools Used
Python
Pandas
Matplotlib
Datetime utilities

## How to Run
```bash
python scripts/generate_customer_health_report.py