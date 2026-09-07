# OTT Content Engagement & Personalization Analytics

A business-analyst style case study on a streaming platform's content, engagement, personalization, and monetisation data — built to answer the kind of question a content/analytics team gets asked: **where should we invest, and is personalization actually working?**

## Business questions answered
1. Are we retaining users, and which signup cohorts are at risk of churn?
2. Which content types (Sports / Originals / general catalog) deserve more investment?
3. Is the recommendation system driving measurably higher engagement?
4. Is the Premium subscription tier earning its price relative to Ad-Supported?
5. Where should QoE/UX investment go by device?

## Key findings
- **+23.7% completion-rate lift** on recommended vs. organically browsed content — personalization is measurably working, though the analysis flags the need for an A/B test to rule out selection bias before using this to justify major spend.
- **Sports and Originals outperform the general catalog by ~10 percentage points** in completion rate — but Sports wins on volume/reach while Originals win on depth, arguing for a balanced content slate rather than a single bet.
- **Premium users average ~35% more sessions** than Ad-Supported users, supporting the tier's pricing power — while also surfacing the ad-tier gap as an open question (content-fit vs. product friction).
- Cohort retention decays with tenure, arguing for **tenure-triggered win-back campaigns** rather than blanket retention pushes.

## Data
No licensed OTT dataset was available for this project, so session-level data (`data/users.csv`, `data/content.csv`, `data/watch_sessions.csv`) was **synthetically generated** (`generate_data.py`) with realistic behavioural assumptions — tenure-based engagement decay, a recommendation-completion lift, and genre-based completion differences. This keeps the focus on analytical methodology and business framing rather than a specific dataset.

- 6,000 users (signup cohort, subscription tier, acquisition channel, device)
- 400 titles across 10 genres (Drama, Sports-Live, Sports-Highlights, Originals, Kids, News, etc.)
- ~160,000 watch sessions (completion rate, recommendation flag, device)

## Method
- `generate_data.py` — synthetic data generation
- `analysis.py` — pandas/seaborn analysis producing all charts in `charts/`
- `OTT_Content_Engagement_Analytics.ipynb` — full notebook with narrative, charts, and business recommendations

## Stack
Python, pandas, numpy, matplotlib, seaborn

## Caveats (worth stating upfront)
This is a portfolio project built on synthetic data to demonstrate analytical framing and business storytelling — not a claim about any real platform's actual metrics. The recommendation-lift finding is explicitly flagged as correlational pending a causal test design.
