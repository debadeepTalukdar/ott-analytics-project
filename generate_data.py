import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# ---------- Content catalog ----------
n_content = 400
genres = ['Drama', 'Comedy', 'Action', 'Sports-Live', 'Sports-Highlights',
          'Kids', 'Reality', 'Originals-Drama', 'News', 'Documentary']
content_type_map = {
    'Sports-Live': 'Sports', 'Sports-Highlights': 'Sports',
    'Originals-Drama': 'Original', 'News': 'News'
}

content = pd.DataFrame({
    'content_id': range(1, n_content + 1),
    'genre': rng.choice(genres, n_content, p=[.14,.12,.12,.08,.06,.09,.08,.11,.10,.10]),
})
content['content_type'] = content['genre'].map(content_type_map).fillna('Regular')
content['runtime_min'] = np.where(
    content['genre'].isin(['Sports-Live']), rng.integers(90, 210, n_content),
    rng.integers(20, 140, n_content)
)
content['is_premium_exclusive'] = rng.choice([0, 1], n_content, p=[.65, .35])

# ---------- Users ----------
n_users = 6000
signup_days_ago = rng.integers(1, 400, n_users)
users = pd.DataFrame({
    'user_id': range(1, n_users + 1),
    'signup_day': signup_days_ago,   # days before "today" (day 400 = today)
    'subscription_tier': rng.choice(['Ad-Supported', 'Premium'], n_users, p=[.62, .38]),
    'device': rng.choice(['Mobile', 'CTV', 'Web', 'Tablet'], n_users, p=[.5, .25, .18, .07]),
    'acquisition_channel': rng.choice(['Organic', 'Paid-Social', 'Telco-Bundle', 'Referral'],
                                       n_users, p=[.35, .25, .3, .1]),
})
users['signup_cohort_month'] = (users['signup_day'] // 30).astype(int)  # 0 = most recent

# ---------- Watch sessions ----------
# Each user gets a variable number of sessions depending on tenure & tier (proxy for engagement/churn)
rows = []
today = 400
for _, u in users.iterrows():
    tenure = today - u['signup_day']
    tier_mult = 1.35 if u['subscription_tier'] == 'Premium' else 1.0
    # base engagement decays with tenure (simulates natural churn risk) with noise
    base_sessions = max(0, rng.poisson(lam=min(40, tenure * 0.12) * tier_mult))
    n_sessions = int(base_sessions)
    if n_sessions == 0:
        continue
    session_days = rng.integers(u['signup_day']*-1+u['signup_day'], today, n_sessions) if tenure>0 else []
    session_days = rng.integers(max(0, today - tenure), today, n_sessions)
    picked_content = content.sample(n_sessions, replace=True, weights=None, random_state=None)
    for i in range(n_sessions):
        c = picked_content.iloc[i]
        is_recommended = rng.choice([1, 0], p=[.42, .58])
        # recommended content + sports/originals -> higher completion (the "personalization lift" signal)
        base_completion = rng.normal(0.55, 0.15)
        if is_recommended:
            base_completion += 0.14
        if c['content_type'] in ['Sports', 'Original']:
            base_completion += 0.10
        completion = min(1.0, max(0.02, base_completion))
        rows.append((
            u['user_id'], c['content_id'], session_days[i], u['device'],
            is_recommended, round(completion, 3)
        ))

sessions = pd.DataFrame(rows, columns=[
    'user_id', 'content_id', 'session_day', 'device', 'is_recommended', 'completion_rate'
])

users.to_csv('data/users.csv', index=False)
content.to_csv('data/content.csv', index=False)
sessions.to_csv('data/watch_sessions.csv', index=False)
print(users.shape, content.shape, sessions.shape)
