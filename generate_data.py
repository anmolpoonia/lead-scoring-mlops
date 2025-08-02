import pandas as pd
import numpy as np
import random

def generate_lead_data(n_samples=1000):
    np.random.seed(42)
    random.seed(42)

    age_groups = ['18-25', '26-35', '36-50', '51+']
    family_backgrounds = ['Single', 'Married', 'Married with Kids']
    city_tiers = ['T1', 'T2', 'T3']
    comments_pool = [
        'urgent need for property',
        'not interested right now',
        'call me later please',
        'just browsing options',
        'looking for 3BHK apartment',
        'interested in investment',
        'need more information',
        'budget is flexible',
        'prefer good location',
        'want to visit soon'
    ]

    data = []
    for i in range(n_samples):
        email = f"lead{i+1}@email.com"
        credit_score = np.random.randint(300, 850)
        income = np.random.randint(30000, 200000)
        clicks = np.random.randint(1, 50)
        time_on_site = np.random.randint(30, 1200)
        age_group = random.choice(age_groups)
        family = random.choice(family_backgrounds)
        tier = random.choice(city_tiers)
        comments = random.choice(comments_pool)

        # Base conversion probability modified by conditions
        p = 0.1
        p += 0.2 * (credit_score > 700)
        p += 0.15 * (income > 100000)
        p += 0.1 * (clicks > 20)
        p += 0.1 * (time_on_site > 600)
        p += 0.1 * (age_group in ['26-35', '36-50'])
        p += 0.15 * (family == 'Married with Kids')
        p += 0.1 * (tier == 'T1')
        if 'urgent' in comments:
            p += 0.2
        elif 'not interested' in comments:
            p -= 0.3
        elif 'call later' in comments:
            p -= 0.1
        elif 'just browsing' in comments:
            p -= 0.2
        elif '3BHK' in comments:
            p += 0.1
        p = max(0, min(1, p))

        converted = int(np.random.random() < p)

        data.append({
            'email': email,
            'credit_score': credit_score,
            'income': income,
            'clicks': clicks,
            'time_on_site': time_on_site,
            'age_group': age_group,
            'family_background': family,
            'city_tier': tier,
            'comments': comments,
            'converted': converted
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_lead_data(1000)
    df.to_csv('leads_data.csv', index=False)
    print(f"Generated {len(df)} leads; conversion rate={df.converted.mean():.2f}")
