#!/usr/bin/env python3
"""
Comprehensive Data Analysis Script
Performs exploratory data analysis on CSV files
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import sys
import os

warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class DataAnalyzer:
    def __init__(self, file_path):
        """Initialize the analyzer with a CSV file path"""
        self.file_path = file_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load CSV data"""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✓ Successfully loaded data from {self.file_path}")
            print(f"  Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns\n")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            sys.exit(1)
    
    def basic_info(self):
        """Display basic information about the dataset"""
        print("="*80)
        print("BASIC DATASET INFORMATION")
        print("="*80)
        
        print("\n1. Dataset Shape:")
        print(f"   Rows: {self.df.shape[0]}")
        print(f"   Columns: {self.df.shape[1]}")
        
        print("\n2. Column Names and Types:")
        print(self.df.dtypes)
        
        print("\n3. First 5 Rows:")
        print(self.df.head())
        
        print("\n4. Last 5 Rows:")
        print(self.df.tail())
        
        print("\n5. Dataset Info:")
        self.df.info()
        
        print("\n6. Memory Usage:")
        print(f"   {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    def missing_values_analysis(self):
        """Analyze missing values"""
        print("\n" + "="*80)
        print("MISSING VALUES ANALYSIS")
        print("="*80)
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing_Count': missing.values,
            'Missing_Percentage': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
        
        if len(missing_df) > 0:
            print("\nColumns with missing values:")
            print(missing_df.to_string(index=False))
            
            # Visualize missing values
            if len(missing_df) > 0:
                plt.figure(figsize=(10, 6))
                plt.barh(missing_df['Column'], missing_df['Missing_Percentage'])
                plt.xlabel('Missing Percentage (%)')
                plt.title('Missing Values by Column')
                plt.tight_layout()
                plt.savefig('/vercel/sandbox/missing_values.png', dpi=300, bbox_inches='tight')
                print("\n✓ Missing values visualization saved as 'missing_values.png'")
                plt.close()
        else:
            print("\n✓ No missing values found in the dataset!")
    
    def statistical_summary(self):
        """Generate statistical summary"""
        print("\n" + "="*80)
        print("STATISTICAL SUMMARY")
        print("="*80)
        
        print("\n1. Numerical Columns Summary:")
        print(self.df.describe())
        
        print("\n2. Categorical Columns Summary:")
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                print(f"\n   {col}:")
                print(f"   - Unique values: {self.df[col].nunique()}")
                print(f"   - Most common: {self.df[col].mode().values[0] if len(self.df[col].mode()) > 0 else 'N/A'}")
                print(f"   - Value counts (top 5):")
                print(self.df[col].value_counts().head().to_string())
    
    def correlation_analysis(self):
        """Analyze correlations between numerical variables"""
        print("\n" + "="*80)
        print("CORRELATION ANALYSIS")
        print("="*80)
        
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) > 1:
            corr_matrix = self.df[numerical_cols].corr()
            
            print("\nCorrelation Matrix:")
            print(corr_matrix)
            
            # Visualize correlation matrix
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       fmt='.2f', square=True, linewidths=1)
            plt.title('Correlation Matrix Heatmap')
            plt.tight_layout()
            plt.savefig('/vercel/sandbox/correlation_matrix.png', dpi=300, bbox_inches='tight')
            print("\n✓ Correlation matrix saved as 'correlation_matrix.png'")
            plt.close()
            
            # Find strong correlations
            print("\nStrong Correlations (|r| > 0.7):")
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corr.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': corr_matrix.iloc[i, j]
                        })
            
            if strong_corr:
                strong_corr_df = pd.DataFrame(strong_corr)
                print(strong_corr_df.to_string(index=False))
            else:
                print("   No strong correlations found.")
        else:
            print("\n⚠ Not enough numerical columns for correlation analysis")
    
    def distribution_analysis(self):
        """Analyze distributions of numerical variables"""
        print("\n" + "="*80)
        print("DISTRIBUTION ANALYSIS")
        print("="*80)
        
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) > 0:
            # Create distribution plots
            n_cols = min(3, len(numerical_cols))
            n_rows = (len(numerical_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
            axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
            
            for idx, col in enumerate(numerical_cols):
                if idx < len(axes):
                    self.df[col].hist(bins=30, ax=axes[idx], edgecolor='black')
                    axes[idx].set_title(f'Distribution of {col}')
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
            
            # Hide empty subplots
            for idx in range(len(numerical_cols), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            plt.savefig('/vercel/sandbox/distributions.png', dpi=300, bbox_inches='tight')
            print("\n✓ Distribution plots saved as 'distributions.png'")
            plt.close()
            
            # Normality tests
            print("\nNormality Tests (Shapiro-Wilk):")
            for col in numerical_cols:
                if len(self.df[col].dropna()) > 3:
                    stat, p_value = stats.shapiro(self.df[col].dropna().sample(min(5000, len(self.df[col].dropna()))))
                    result = "Normal" if p_value > 0.05 else "Not Normal"
                    print(f"   {col}: p-value = {p_value:.4f} ({result})")
    
    def outlier_detection(self):
        """Detect outliers using IQR method"""
        print("\n" + "="*80)
        print("OUTLIER DETECTION")
        print("="*80)
        
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        
        outliers_summary = []
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outliers_summary.append({
                'Column': col,
                'Outliers_Count': len(outliers),
                'Outliers_Percentage': (len(outliers) / len(self.df)) * 100,
                'Lower_Bound': lower_bound,
                'Upper_Bound': upper_bound
            })
        
        outliers_df = pd.DataFrame(outliers_summary)
        print("\nOutliers Summary (IQR Method):")
        print(outliers_df.to_string(index=False))
        
        # Box plots
        if len(numerical_cols) > 0:
            n_cols = min(3, len(numerical_cols))
            n_rows = (len(numerical_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
            axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
            
            for idx, col in enumerate(numerical_cols):
                if idx < len(axes):
                    self.df.boxplot(column=col, ax=axes[idx])
                    axes[idx].set_title(f'Box Plot: {col}')
            
            # Hide empty subplots
            for idx in range(len(numerical_cols), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            plt.savefig('/vercel/sandbox/outliers_boxplots.png', dpi=300, bbox_inches='tight')
            print("\n✓ Box plots saved as 'outliers_boxplots.png'")
            plt.close()
    
    def categorical_analysis(self):
        """Analyze categorical variables"""
        print("\n" + "="*80)
        print("CATEGORICAL VARIABLES ANALYSIS")
        print("="*80)
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) > 0:
            for col in categorical_cols[:5]:  # Limit to first 5 categorical columns
                print(f"\n{col}:")
                value_counts = self.df[col].value_counts()
                print(value_counts.head(10))
                
                # Create bar plot for top categories
                if len(value_counts) > 0:
                    plt.figure(figsize=(12, 6))
                    value_counts.head(10).plot(kind='bar')
                    plt.title(f'Top 10 Categories in {col}')
                    plt.xlabel(col)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.savefig(f'/vercel/sandbox/categorical_{col.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
                    print(f"✓ Bar plot saved as 'categorical_{col.replace(' ', '_')}.png'")
                    plt.close()
        else:
            print("\n⚠ No categorical columns found")
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE ANALYSIS REPORT")
        print("="*80 + "\n")
        
        self.basic_info()
        self.missing_values_analysis()
        self.statistical_summary()
        self.correlation_analysis()
        self.distribution_analysis()
        self.outlier_detection()
        self.categorical_analysis()
        
        # Save summary to file
        with open('/vercel/sandbox/analysis_summary.txt', 'w') as f:
            f.write("DATA ANALYSIS SUMMARY\n")
            f.write("="*80 + "\n\n")
            f.write(f"Dataset: {self.file_path}\n")
            f.write(f"Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns\n\n")
            f.write("Columns:\n")
            for col in self.df.columns:
                f.write(f"  - {col} ({self.df[col].dtype})\n")
            f.write("\n" + self.df.describe().to_string())
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print("\nGenerated files:")
        print("  - analysis_summary.txt")
        print("  - missing_values.png (if applicable)")
        print("  - correlation_matrix.png (if applicable)")
        print("  - distributions.png")
        print("  - outliers_boxplots.png")
        print("  - categorical_*.png (for each categorical variable)")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 data_analysis.py <csv_file_path>")
        print("\nExample: python3 data_analysis.py data.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found!")
        sys.exit(1)
    
    analyzer = DataAnalyzer(csv_file)
    analyzer.generate_report()


if __name__ == "__main__":
    main()
