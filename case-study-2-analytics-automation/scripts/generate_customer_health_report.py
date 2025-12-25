# This script can be scheduled to run weekly/monthly
# Automated Customer Health Report Generator
# Generates KPI tables, at-risk customer lists, and executive charts

import pandas
import numpy
import os
import matplotlib.pyplot as plt

def main():
    print("=" * 60)
    print("CUSTOMER HEALTH REPORT GENERATOR")
    print("=" * 60)
    
    # Load the customer transactions data
    print("\n[1/6] Loading data...")
    df = pandas.read_csv('../data/Customer_Transactions.csv')
    df['last_purchase_date'] = pandas.to_datetime(df['last_purchase_date'])
    print(f"✓ Loaded {len(df)} records")
    
    # Define reporting window (last 30 days)
    print("\n[2/6] Defining 30-day reporting window...")
    current_date = df['last_purchase_date'].max()
    window_start = current_date - pandas.Timedelta(days=30)
    df_window = df[df['last_purchase_date'] >= window_start].copy()
    print(f"✓ Window: {window_start.date()} to {current_date.date()}")
    print(f"✓ {len(df_window)} customers in window")
    
    # Calculate days since purchase
    df_window['days_since_purchase'] = (current_date - df_window['last_purchase_date']).dt.days
    
    # Create customer tier
    def categorize_tier(score):
        if score < 40:
            return 'Low'
        elif score <= 70:
            return 'Medium'
        else:
            return 'High'
    
    df_window['customer_tier'] = df_window['spending_score'].apply(categorize_tier)
    
    # Identify at-risk customers
    print("\n[3/6] Identifying at-risk customers...")
    at_risk_condition = (df_window['days_since_purchase'] >= 30) | (df_window['cart_abandon_rate'] >= 0.9)
    at_risk_customers = df_window[at_risk_condition].copy()
    at_risk_customers = at_risk_customers.sort_values(
        by=['days_since_purchase', 'cart_abandon_rate'], 
        ascending=[False, False]
    )
    print(f"✓ {len(at_risk_customers)} at-risk customers identified")
    
    # Calculate overall KPIs
    print("\n[4/6] Computing KPIs...")
    kpi_overall = pandas.DataFrame({
        'total_customers': [len(df_window)],
        'active_customers': [(df_window['churned'] == 0).sum()],
        'churned_customers': [(df_window['churned'] == 1).sum()],
        'churn_rate': [(df_window['churned'] == 1).sum() / len(df_window)],
        'avg_purchase_value': [df_window['avg_purchase_value'].mean()],
        'avg_website_visits_per_month': [df_window['website_visits_per_month'].mean()],
        'avg_cart_abandon_rate': [df_window['cart_abandon_rate'].mean()],
        'avg_days_since_purchase': [df_window['days_since_purchase'].mean()],
        'revenue_proxy': [(df_window['avg_purchase_value'] * df_window['num_purchases']).sum()]
    })
    
    # KPI breakdown by country
    kpi_by_country = df_window.groupby('country').agg(
        total_customers=('customer_id', 'count'),
        churn_rate=('churned', 'mean'),
        avg_cart_abandon_rate=('cart_abandon_rate', 'mean'),
        avg_days_since_purchase=('days_since_purchase', 'mean')
    ).reset_index()
    kpi_by_country = kpi_by_country.sort_values(
        by=['avg_cart_abandon_rate', 'avg_days_since_purchase'],
        ascending=[False, False]
    )
    
    # KPI breakdown by customer tier
    kpi_by_tier = df_window.groupby('customer_tier').agg(
        total_customers=('customer_id', 'count'),
        churn_rate=('churned', 'mean'),
        avg_cart_abandon_rate=('cart_abandon_rate', 'mean'),
        avg_purchase_value=('avg_purchase_value', 'mean')
    ).reset_index()
    tier_order = {'Low': 0, 'Medium': 1, 'High': 2}
    kpi_by_tier['sort_order'] = kpi_by_tier['customer_tier'].map(tier_order)
    kpi_by_tier = kpi_by_tier.sort_values('sort_order').drop('sort_order', axis=1)
    print("✓ Overall, country, and tier KPIs computed")
    
    # Export data
    print("\n[5/6] Exporting reports...")
    os.makedirs('../output', exist_ok=True)
    os.makedirs('../output/charts', exist_ok=True)
    
    kpi_overall.to_csv('../output/kpi_overall_30_days.csv', index=False)
    kpi_by_country.to_csv('../output/kpi_by_country_30_days.csv', index=False)
    kpi_by_tier.to_csv('../output/kpi_by_tier_30_days.csv', index=False)
    
    # Export at-risk customers (all columns for actionability)
    at_risk_export = at_risk_customers[[
        'customer_id', 'country', 'gender', 'days_since_purchase', 
        'cart_abandon_rate', 'num_purchases', 'avg_purchase_value', 
        'churned', 'customer_tier'
    ]]
    at_risk_export.to_csv('../output/at_risk_customers.csv', index=False)
    
    print("✓ Exported: kpi_overall_30_days.csv")
    print("✓ Exported: kpi_by_country_30_days.csv")
    print("✓ Exported: kpi_by_tier_30_days.csv")
    print(f"✓ Exported: at_risk_customers.csv ({len(at_risk_customers)} customers)")
    
    # Generate charts
    print("\n[6/6] Generating executive charts...")
    
    # Chart A: At-Risk Days Since Purchase
    plt.figure(figsize=(10, 6))
    plt.hist(at_risk_customers['days_since_purchase'], bins=15, edgecolor='black', color='steelblue')
    plt.xlabel('Days Since Last Purchase', fontsize=12)
    plt.ylabel('Number of At-Risk Customers', fontsize=12)
    plt.title('At-Risk Customer Distribution by Inactivity', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('../output/charts/at_risk_days_since_purchase.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart saved: at_risk_days_since_purchase.png")
    
    # Chart B: Abandon Rate by Tier
    plt.figure(figsize=(10, 6))
    bars = plt.bar(kpi_by_tier['customer_tier'], 
                   kpi_by_tier['avg_cart_abandon_rate'], 
                   edgecolor='black', 
                   color='steelblue')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1%}',
                 ha='center', va='bottom', fontsize=11)
    
    plt.xlabel('Customer Tier', fontsize=12)
    plt.ylabel('Average Cart Abandon Rate', fontsize=12)
    plt.title('Cart Abandon Rate by Customer Tier', fontsize=14, fontweight='bold')
    plt.ylim(0, max(kpi_by_tier['avg_cart_abandon_rate']) * 1.15)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('../output/charts/abandon_rate_by_tier.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Chart saved: abandon_rate_by_tier.png")
    
    # Summary
    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETE")
    print("=" * 60)
    churn_rate_pct = kpi_overall['churn_rate'].iloc[0] * 100
    avg_abandon_rate_pct = kpi_overall['avg_cart_abandon_rate'].iloc[0] * 100
    print(f"\n📊 Summary: In the last 30 days, {churn_rate_pct:.1f}% of customers churned,")
    print(f"   with an average cart abandon rate of {avg_abandon_rate_pct:.1f}%.")
    print(f"\n⚠️  {len(at_risk_customers)} at-risk customers require immediate attention.")
    print("\nAll reports saved to: ../output/")
    print("=" * 60)

if __name__ == "__main__":
    main()
