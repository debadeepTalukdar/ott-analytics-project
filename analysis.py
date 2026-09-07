import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 110

users = pd.read_csv('data/users.csv')
content = pd.read_csv('data/content.csv')
sessions = pd.read_csv('data/watch_sessions.csv')

df = sessions.merge(users, on='user_id').merge(content, on='content_id')

# ---------------- 1. Retention / cohort analysis ----------------
today = 400
users['tenure_days'] = today - users['signup_day']
active_users = sessions[sessions['session_day'] >= today - 30]['user_id'].unique()
users['active_last_30d'] = users['user_id'].isin(active_users)

cohort_retention = users.groupby('signup_cohort_month')['active_last_30d'].mean().sort_index()
cohort_retention = cohort_retention[cohort_retention.index <= 10]  # keep readable window

plt.figure(figsize=(8,4.5))
cohort_retention.plot(kind='line', marker='o', color='#5b3fd6')
plt.gca().invert_xaxis()
plt.title('30-Day Active Retention by Signup Cohort (0 = most recent)')
plt.xlabel('Signup cohort (months ago)')
plt.ylabel('% active in last 30 days')
plt.tight_layout()
plt.savefig('charts/01_cohort_retention.png')
plt.close()

# ---------------- 2. Content performance by genre/type ----------------
genre_perf = df.groupby('genre').agg(
    avg_completion=('completion_rate', 'mean'),
    total_sessions=('user_id', 'count')
).sort_values('avg_completion', ascending=False)

plt.figure(figsize=(8,5))
sns.barplot(x=genre_perf['avg_completion'], y=genre_perf.index, color='#3fb6d6')
plt.title('Average Completion Rate by Content Genre')
plt.xlabel('Avg completion rate')
plt.tight_layout()
plt.savefig('charts/02_genre_completion.png')
plt.close()

type_perf = df.groupby('content_type').agg(
    avg_completion=('completion_rate','mean'),
    sessions=('user_id','count')
).sort_values('avg_completion', ascending=False)

# ---------------- 3. Personalization lift ----------------
reco_lift = df.groupby('is_recommended')['completion_rate'].mean()
reco_lift.index = ['Organic/Browse', 'Recommended']
lift_pct = (reco_lift['Recommended'] / reco_lift['Organic/Browse'] - 1) * 100

plt.figure(figsize=(5,4.5))
sns.barplot(x=list(reco_lift.index), y=reco_lift.values, hue=list(reco_lift.index), palette=['#a3a3a3', '#5b3fd6'], legend=False)
plt.title(f'Completion Rate: Recommended vs Organic\n(+{lift_pct:.1f}% lift)')
plt.ylabel('Avg completion rate')
plt.xlabel('Discovery path')
plt.tight_layout()
plt.savefig('charts/03_recommendation_lift.png')
plt.close()

# ---------------- 4. Monetisation: tier engagement ----------------
tier_engagement = df.groupby('subscription_tier').agg(
    avg_completion=('completion_rate','mean'),
    sessions_per_user=('user_id', lambda x: len(x))
)
sessions_per_user_actual = df.groupby(['subscription_tier','user_id']).size().groupby('subscription_tier').mean()

plt.figure(figsize=(5,4.5))
sns.barplot(x=list(sessions_per_user_actual.index), y=sessions_per_user_actual.values, hue=list(sessions_per_user_actual.index), palette=['#e07b39','#5b3fd6'], legend=False)
plt.title('Avg Sessions per User by Subscription Tier')
plt.xlabel('Subscription tier')
plt.ylabel('Avg sessions/user')
plt.tight_layout()
plt.savefig('charts/04_tier_engagement.png')
plt.close()

# ---------------- 5. Device engagement ----------------
device_completion = df.groupby('device_x')['completion_rate'].mean().sort_values(ascending=False)

plt.figure(figsize=(6,4.5))
sns.barplot(x=device_completion.index, y=device_completion.values, color='#3fb6d6')
plt.title('Avg Completion Rate by Viewing Device')
plt.ylabel('Avg completion rate')
plt.tight_layout()
plt.savefig('charts/05_device_completion.png')
plt.close()
df = df.rename(columns={'device_x':'session_device','device_y':'account_device'})

# Save summary numbers for README / notebook narrative
summary = {
    'lift_pct': round(lift_pct,1),
    'top_genre': genre_perf.index[0],
    'top_genre_completion': round(genre_perf.iloc[0]['avg_completion'],3),
    'premium_sessions_per_user': round(sessions_per_user_actual['Premium'],2),
    'ad_sessions_per_user': round(sessions_per_user_actual['Ad-Supported'],2),
    'best_device': device_completion.index[0],
    'sports_vs_regular': round(type_perf.loc['Sports','avg_completion'] - type_perf.loc['Regular','avg_completion'],3) if 'Sports' in type_perf.index and 'Regular' in type_perf.index else None,
}
import json
with open('summary.json','w') as f:
    json.dump(summary, f, indent=2)
print(summary)
print(genre_perf)
print(type_perf)
