import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

# -------------------------------
# 1. Create Synthetic Dataset
# -------------------------------
np.random.seed(42)
n = 200
df = pd.DataFrame({
    "Patient_ID": range(1, n+1),
    "Age": np.random.randint(20, 90, n),
    "Gender": np.random.choice(["Male", "Female"], n),
    "Readmitted": np.random.choice(["Yes", "No"], n, p=[0.3, 0.7]),
    "billed_amount": np.random.uniform(5000, 50000, n),
    "collected_amount": np.random.uniform(3000, 45000, n),
    "denial_reason": np.random.choice(
        ["Coding Error", "Lack of Info", "Not Covered", "Duplicate Claim", "Timely Filing"], n
    ),
    "payer": np.random.choice(
        ["Medicare", "Medicaid", "Blue Cross", "Aetna", "UnitedHealth"], n
    ),
    "days_in_ar": np.random.randint(15, 90, n)
})

# -------------------------------
# 2. Financial Capture: Billed vs Collected
# -------------------------------
billed_total = df['billed_amount'].sum()
collected_total = df['collected_amount'].sum()

fig1 = go.Figure(data=[
    go.Bar(name='Billed', x=['Total Revenue'], y=[billed_total], marker_color='#3498db'),
    go.Bar(name='Collected', x=['Total Revenue'], y=[collected_total], marker_color='#2ecc71')
])
fig1.update_layout(title='Total Billed vs. Total Collected', barmode='group', template='plotly_white')
fig1.show()

# -------------------------------
# 3. Top 5 Denial Reasons
# -------------------------------
denials = df['denial_reason'].value_counts().nlargest(5).reset_index()
denials.columns = ['Reason', 'Count']

fig2 = px.pie(denials, values='Count', names='Reason', title='Top 5 Denial Reasons', hole=0.4,
             color_discrete_sequence=px.colors.sequential.RdBu)
fig2.show()

# -------------------------------
# 4. Days in A/R by Payer
# -------------------------------
ar_by_payer = df.groupby('payer')['days_in_ar'].mean().sort_values(ascending=False).reset_index()

fig3 = px.bar(ar_by_payer, x='payer', y='days_in_ar',
             title='Average Days in A/R by Payer',
             labels={'days_in_ar': 'Avg Days', 'payer': 'Insurance Provider'},
             color='days_in_ar', color_continuous_scale='Viridis')
fig3.show()

# -------------------------------
# 5. Collection Rate by Payer
# -------------------------------
collection_stats = df.groupby('payer').agg({
    'billed_amount': 'sum',
    'collected_amount': 'sum'
}).reset_index()

collection_stats['collection_rate'] = (collection_stats['collected_amount'] / collection_stats['billed_amount']) * 100

fig4 = px.bar(collection_stats.sort_values('collection_rate', ascending=False),
             x='payer', y='collection_rate',
             title='Collection Rate (%) by Payer',
             labels={'collection_rate': 'Collection Rate (%)', 'payer': 'Insurance Provider'},
             text_auto='.2f',
             color='collection_rate', color_continuous_scale='Greens')
fig4.update_layout(yaxis_range=[0, 100], template='plotly_white')
fig4.show()

# -------------------------------
# 6. Collection Rate vs Days in A/R
# -------------------------------
comparison_df = pd.merge(collection_stats, ar_by_payer, on='payer')

fig5 = make_subplots(specs=[[{"secondary_y": True}]])
fig5.add_trace(
    go.Bar(x=comparison_df['payer'], y=comparison_df['collection_rate'],
           name="Collection Rate (%)", marker_color='#2ecc71'),
    secondary_y=False,
)
fig5.add_trace(
    go.Scatter(x=comparison_df['payer'], y=comparison_df['days_in_ar'],
               name="Avg Days in A/R", mode='lines+markers', marker_color='#e74c3c'),
    secondary_y=True,
)
fig5.update_layout(title_text="Collection Rate vs. Days in A/R by Payer", template='plotly_white')
fig5.update_yaxes(title_text="Collection Rate (%)", secondary_y=False, range=[0, 100])
fig5.update_yaxes(title_text="Average Days in A/R", secondary_y=True)
fig5.show()

# -------------------------------
# 7. Denial Reasons for Lowest Performing Payer
# -------------------------------
lowest_payer = collection_stats.sort_values('collection_rate').iloc[0]['payer']
lowest_payer_denials = df[df['payer'] == lowest_payer]['denial_reason'].value_counts().reset_index()
lowest_payer_denials.columns = ['Reason', 'Count']

fig6 = px.bar(lowest_payer_denials,
             x='Reason', y='Count',
             title=f'Denial Reason Distribution for {lowest_payer}',
             labels={'Count': 'Number of Denials', 'Reason': 'Denial Category'},
             color='Count', color_continuous_scale='Reds')
fig6.update_layout(template='plotly_white')
fig6.show()

print(f"The lowest performing payer is {lowest_payer}.")
