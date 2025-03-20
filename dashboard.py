import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load dataset
file_path = r"C:\Users\Admin\Downloads\DataScience_salaries_2025.csv"   # Adjust path if needed
df = pd.read_csv(file_path)

# Convert work_year to integer (if not already)
df['work_year'] = df['work_year'].astype(int)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Data Science Salaries Dashboard", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id="job_title_dropdown",
        options=[{"label": j, "value": j} for j in df["job_title"].unique()],
        value=df["job_title"].unique()[0],
        clearable=False,
        style={'width': "50%"}
    ),
    
    dcc.Graph(id="salary_trend_graph"),
    
    dcc.Graph(id="top_paying_jobs"),
    
    dcc.Graph(id="salary_distribution_experience"),
    
    dcc.Graph(id="salary_by_company_size")
])

# Callback for updating graphs
@app.callback(
    [Output("salary_trend_graph", "figure"),
     Output("top_paying_jobs", "figure"),
     Output("salary_distribution_experience", "figure"),
     Output("salary_by_company_size", "figure")],
    [Input("job_title_dropdown", "value")]
)
def update_graphs(selected_job):
    # Salary trend over years
    trend_fig = px.line(df[df["job_title"] == selected_job], x="work_year", y="salary_in_usd",
                        title=f"Salary Trend for {selected_job}", markers=True)

    # Top 10 highest-paying jobs
    top_jobs_fig = px.bar(df.groupby("job_title")["salary_in_usd"].mean().nlargest(10).reset_index(),
                          x="job_title", y="salary_in_usd", title="Top 10 Highest-Paying Job Titles")

    # Salary distribution by experience level
    experience_fig = px.box(df, x="experience_level", y="salary_in_usd",
                            title="Salary Distribution by Experience Level", color="experience_level")

    # Salary comparison by company size
    company_fig = px.bar(df.groupby("company_size")["salary_in_usd"].mean().reset_index(),
                         x="company_size", y="salary_in_usd", title="Salary by Company Size")

    return trend_fig, top_jobs_fig, experience_fig, company_fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050)
