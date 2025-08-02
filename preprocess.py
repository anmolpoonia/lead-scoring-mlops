import pandas as pd

class LeadPreprocessor:
    def __init__(self):
        self.age_map = {'18-25': 0, '26-35': 1, '36-50': 2, '51+': 3}
        self.family_map = {'Single': 0, 'Married': 1, 'Married with Kids': 2}
        self.city_map = {'T1': 0, 'T2': 1, 'T3': 2}

    def preprocess_features(self, df):
        df = df.copy()
        df['age_group_encoded'] = df['age_group'].map(self.age_map)
        df['family_background_encoded'] = df['family_background'].map(self.family_map)
        df['city_tier_encoded'] = df['city_tier'].map(self.city_map)

        feature_cols = [
            'credit_score',
            'income',
            'clicks',
            'time_on_site',
            'age_group_encoded',
            'family_background_encoded',
            'city_tier_encoded'
        ]
        return df[feature_cols]

    def preprocess_single_lead(self, lead_data: dict):
        df = pd.DataFrame([lead_data])
        return self.preprocess_features(df).values[0]

    def apply_reranker_adjustment(self, initial_prob, comments):
        adjust = 0
        c = comments.lower()
        if 'urgent' in c:
            adjust += 10
        elif 'not interested' in c:
            adjust -= 10
        elif 'call later' in c:
            adjust -= 5
        elif 'just browsing' in c:
            adjust -= 15
        elif '3bhk' in c:
            adjust += 5

        score_pct = initial_prob * 100 + adjust
        # Clamp between 0 and 100
        return max(0, min(100, score_pct))
