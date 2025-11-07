#!/usr/bin/env python3
"""
Generate sample cybersecurity vulnerability data
Similar to what might be available from Transilience.ai
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_vulnerability_data(n_records=1000):
    """Generate sample vulnerability/threat intelligence data"""
    
    print(f"Generating {n_records} sample vulnerability records...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define data categories
    severities = ['Critical', 'High', 'Medium', 'Low']
    severity_weights = [0.15, 0.25, 0.35, 0.25]
    
    vendors = ['Microsoft', 'Apache', 'Oracle', 'Cisco', 'Adobe', 'Google', 
               'Mozilla', 'Linux', 'VMware', 'IBM', 'SAP', 'Fortinet']
    
    vulnerability_types = ['Buffer Overflow', 'SQL Injection', 'XSS', 
                          'Remote Code Execution', 'Privilege Escalation',
                          'Denial of Service', 'Information Disclosure',
                          'Authentication Bypass', 'CSRF', 'Path Traversal']
    
    products = ['Windows Server', 'Apache HTTP Server', 'Oracle Database',
                'Cisco IOS', 'Adobe Reader', 'Chrome Browser', 'Firefox',
                'Linux Kernel', 'vSphere', 'WebSphere', 'SAP NetWeaver',
                'FortiGate', 'Exchange Server', 'Tomcat', 'MySQL']
    
    statuses = ['Open', 'Patched', 'Mitigated', 'Under Investigation']
    status_weights = [0.20, 0.50, 0.20, 0.10]
    
    # Generate data
    data = {
        'CVE_ID': [f'CVE-{random.randint(2020, 2024)}-{random.randint(1000, 99999)}' 
                   for _ in range(n_records)],
        'Severity': np.random.choice(severities, n_records, p=severity_weights),
        'CVSS_Score': [],
        'Vendor': np.random.choice(vendors, n_records),
        'Product': np.random.choice(products, n_records),
        'Vulnerability_Type': np.random.choice(vulnerability_types, n_records),
        'Published_Date': [],
        'Last_Modified': [],
        'Status': np.random.choice(statuses, n_records, p=status_weights),
        'Exploitability': [],
        'Impact_Score': [],
        'Affected_Systems': [],
        'Patch_Available': [],
        'Days_Since_Publication': [],
        'Priority_Score': []
    }
    
    # Generate CVSS scores based on severity
    for severity in data['Severity']:
        if severity == 'Critical':
            score = round(np.random.uniform(9.0, 10.0), 1)
        elif severity == 'High':
            score = round(np.random.uniform(7.0, 8.9), 1)
        elif severity == 'Medium':
            score = round(np.random.uniform(4.0, 6.9), 1)
        else:
            score = round(np.random.uniform(0.1, 3.9), 1)
        data['CVSS_Score'].append(score)
    
    # Generate dates
    start_date = datetime.now() - timedelta(days=730)  # 2 years ago
    for _ in range(n_records):
        pub_date = start_date + timedelta(days=random.randint(0, 730))
        mod_date = pub_date + timedelta(days=random.randint(0, 90))
        data['Published_Date'].append(pub_date.strftime('%Y-%m-%d'))
        data['Last_Modified'].append(mod_date.strftime('%Y-%m-%d'))
        data['Days_Since_Publication'].append((datetime.now() - pub_date).days)
    
    # Generate exploitability scores
    data['Exploitability'] = [round(np.random.uniform(1.0, 10.0), 1) for _ in range(n_records)]
    data['Impact_Score'] = [round(np.random.uniform(1.0, 10.0), 1) for _ in range(n_records)]
    
    # Generate affected systems count
    data['Affected_Systems'] = [random.randint(10, 10000) for _ in range(n_records)]
    
    # Patch availability (higher for older vulnerabilities)
    data['Patch_Available'] = [
        'Yes' if random.random() < 0.7 else 'No' 
        for _ in range(n_records)
    ]
    
    # Calculate priority score (combination of CVSS, exploitability, and affected systems)
    data['Priority_Score'] = [
        round((cvss * 0.4 + exploit * 0.3 + min(affected/100, 10) * 0.3), 2)
        for cvss, exploit, affected in zip(data['CVSS_Score'], 
                                           data['Exploitability'], 
                                           data['Affected_Systems'])
    ]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df


def generate_superstore_data(n_records=1000):
    """Generate sample retail/superstore data"""
    
    print(f"Generating {n_records} sample superstore records...")
    
    np.random.seed(42)
    random.seed(42)
    
    categories = ['Technology', 'Furniture', 'Office Supplies']
    sub_categories = {
        'Technology': ['Phones', 'Computers', 'Accessories', 'Copiers'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Pens', 'Storage', 'Art']
    }
    
    regions = ['East', 'West', 'Central', 'South']
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    data = {
        'Order_ID': [f'ORD-{random.randint(10000, 99999)}' for _ in range(n_records)],
        'Order_Date': [],
        'Ship_Date': [],
        'Ship_Mode': np.random.choice(ship_modes, n_records),
        'Customer_ID': [f'CUS-{random.randint(1000, 9999)}' for _ in range(n_records)],
        'Customer_Name': [f'Customer_{i}' for i in range(n_records)],
        'Segment': np.random.choice(segments, n_records),
        'Region': np.random.choice(regions, n_records),
        'Category': [],
        'Sub_Category': [],
        'Product_Name': [],
        'Sales': [],
        'Quantity': [],
        'Discount': [],
        'Profit': []
    }
    
    # Generate dates
    start_date = datetime.now() - timedelta(days=1095)  # 3 years
    for _ in range(n_records):
        order_date = start_date + timedelta(days=random.randint(0, 1095))
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        data['Order_Date'].append(order_date.strftime('%Y-%m-%d'))
        data['Ship_Date'].append(ship_date.strftime('%Y-%m-%d'))
    
    # Generate category and sub-category
    for _ in range(n_records):
        category = random.choice(categories)
        sub_category = random.choice(sub_categories[category])
        data['Category'].append(category)
        data['Sub_Category'].append(sub_category)
        data['Product_Name'].append(f'{sub_category}_{random.randint(100, 999)}')
    
    # Generate sales metrics
    for category in data['Category']:
        if category == 'Technology':
            sales = round(np.random.uniform(50, 5000), 2)
        elif category == 'Furniture':
            sales = round(np.random.uniform(100, 3000), 2)
        else:
            sales = round(np.random.uniform(10, 500), 2)
        data['Sales'].append(sales)
    
    data['Quantity'] = [random.randint(1, 10) for _ in range(n_records)]
    data['Discount'] = [round(random.choice([0, 0.1, 0.15, 0.2, 0.25, 0.3]), 2) 
                       for _ in range(n_records)]
    
    # Calculate profit (sales * profit margin - discount impact)
    data['Profit'] = [
        round(sales * np.random.uniform(0.1, 0.4) - (sales * discount * 0.5), 2)
        for sales, discount in zip(data['Sales'], data['Discount'])
    ]
    
    df = pd.DataFrame(data)
    return df


def main():
    """Main function"""
    print("="*80)
    print("SAMPLE DATA GENERATOR")
    print("="*80 + "\n")
    
    print("Select dataset type:")
    print("1. Cybersecurity Vulnerability Data (similar to Transilience.ai)")
    print("2. Retail Superstore Data")
    print("3. Both\n")
    
    choice = input("Enter choice (1/2/3) [default: 3]: ").strip() or "3"
    
    if choice in ['1', '3']:
        df_vuln = generate_vulnerability_data(1000)
        output_file = 'vulnerability_data.csv'
        df_vuln.to_csv(output_file, index=False)
        print(f"✓ Vulnerability data saved as '{output_file}'")
        print(f"  Shape: {df_vuln.shape[0]} rows × {df_vuln.shape[1]} columns\n")
    
    if choice in ['2', '3']:
        df_store = generate_superstore_data(1000)
        output_file = 'SampleSuperstore.csv'
        df_store.to_csv(output_file, index=False)
        print(f"✓ Superstore data saved as '{output_file}'")
        print(f"  Shape: {df_store.shape[0]} rows × {df_store.shape[1]} columns\n")
    
    print("="*80)
    print("Data generation complete!")
    print("="*80)
    print("\nYou can now run analysis using:")
    if choice in ['1', '3']:
        print("  python3 data_analysis.py vulnerability_data.csv")
    if choice in ['2', '3']:
        print("  python3 data_analysis.py SampleSuperstore.csv")


if __name__ == "__main__":
    main()
