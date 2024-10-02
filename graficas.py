import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_missing_values_vertical(df):
    """
    Creates a heatmap showing missing values for each variable (column) of the DataFrame,
    with column names on the Y-axis.

    Args:
    df (DataFrame): The pandas DataFrame to analyze for missing values.
    """
    # Calculate the missing values in each column
    missing = df.isnull()

    # Create a heatmap visualization with rows and columns inverted
    plt.figure(figsize=(8, max(2, len(df.columns) * 0.25)))  # Adjust the figure size based on the number of columns
    sns.heatmap(missing.transpose(), cbar=False, cmap='viridis', yticklabels=True)

    # Add titles and labels in Spanish
    plt.title('Valores Faltantes en Cada Variable')
    plt.xlabel('Índice de Filas')
    plt.ylabel('Nombres de Columnas')

    # Show the plot
    plt.show()