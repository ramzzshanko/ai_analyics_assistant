from matplotlib.colors import LinearSegmentedColormap
from app import db_conn
from langchain_core.tools import tool
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def run_sql_query(query: str) -> pd.DataFrame:
    """Executes SQL queries on DuckDB database with mobile money data."""
    try:
        result = db_conn.execute(query).fetchdf()
        return result
    except Exception as e:
        return f"Error: {str(e)}"
@tool    
def plot_bar(df, x_col, y_col, title="Bar Plot"):
    """Generate a bar plot from DataFrame columns."""
    plt.figure(figsize=(10, 4))
    sns.barplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()
    return plt.gcf()

@tool
def plot_heatmap(df, index_col, columns_col, values_col, title="Heatmap"):
    """Generate a heatmap from pivoted DataFrame."""
    pivot = df.pivot_table(index=index_col, columns=columns_col, values=values_col)
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot, annot=True, cmap='Blues', fmt=".1f")
    plt.title(title)
    plt.tight_layout()
    return plt.gcf()

@tool
def plot_pie(df, labels_col, values_col, title="Pie Chart"):
    """Generate a pie chart from DataFrame columns."""
    plt.figure(figsize=(8, 8))
    plt.pie(df[values_col], labels=df[labels_col], autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures circular shape
    return plt.gcf()

@tool
def plot_line(df, x_col, y_col, title="Line Plot"):
    """Generate a line plot from DataFrame columns."""
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x=x_col, y=y_col, marker='o')
    plt.title(title)
    plt.grid(True)
    return plt.gcf()

@tool
def plot_area(df, x_col, y_col, title="Area Plot"):
    """Generate a stacked area plot from DataFrame columns."""
    plt.figure(figsize=(10, 5))
    plt.fill_between(df[x_col], df[y_col], alpha=0.5)
    plt.title(title)
    plt.grid(True)
    return plt.gcf()

# Custom Seaborn-style colormap for tables
SEABORN_CMAP = LinearSegmentedColormap.from_list(
    'seaborn_table', 
    ['#e6f2ff', '#cce5ff', '#99ccff'], 
    N=256
)

@tool
def generate_html_table(df, title="Data Table", cmap=SEABORN_CMAP):
    """
    Generate a Seaborn-styled HTML table from DataFrame with gradient coloring.

    Args:
        df (pd.DataFrame): Input data
        title (str): Table title
        cmap: Color map for gradient styling

    Returns:
        str: HTML string of the styled table
    """
    styled_df = df.style\
        .background_gradient(cmap=cmap, axis=0)\
        .set_table_attributes('class="seaborn-table"')\
        .set_caption(title)\
        .format(precision=2)\
        .set_properties(**{
            'font-family': 'Arial',
            'border': '1px solid #ddd',
            'text-align': 'center',
            'font-size': '12px'
        })

    return styled_df.to_html()
