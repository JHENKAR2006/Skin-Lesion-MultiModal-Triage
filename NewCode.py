import pandas as pd
df = pd.read_csv('HAM10000_metadata.csv')
print("File loaded successfully! Shape:", df.shape)

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 1. Encode Target Diagnosis Labels (0 to 6)
label_encoder = LabelEncoder()
df['target'] = label_encoder.fit_transform(df['dx'])
class_names = list(label_encoder.classes_)
print("Target Class Mapping:", dict(zip(range(len(class_names)), class_names)))

# 2. Define Feature Columns
num_cols = ['age']
cat_cols = ['sex', 'localization']

# 3. Construct Preprocessing Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ]
)

# 4. Stratified Group K-Fold Split (80% Train, 20% Test grouped by lesion_id)
sgkf = StratifiedGroupKFold(n_splits=5)
trai
train_df = df.iloc[train_idx].reset_index(drop=True)
test_df = df.iloc[test_idx].reset_index(drop=True)

# 5. Fit Preprocessor on Train Set ONLY
X_train_tab = preprocessor.fit_transform(train_df[num_cols + cat_cols])
y_train = n_idx, test_idx = next(sgkf.split(df, df['target'], groups=df['lesion_id']))
train_df['target'].values
X_test_tab = preprocessor.transform(test_df[num_cols + cat_cols])
y_test = test_df['target'].values

print("\n--- Tabular Data Splitting Complete ---")
print(f"X_train_tab shape: {X_train_tab.shape}")
print(f"X_test_tab shape:  {X_test_tab.shape}")

import matplotlib.pyplot as plt
import seaborn as sns


# 2. Define Full Clinical Disease Names & Risk Categories
dx_mapping = {
    'nv': 'Melanocytic nevi (nv)',
    'mel': 'Melanoma (mel)',
    'bkl': 'Benign keratosis (bkl)',
    'bcc': 'Basal cell carcinoma (bcc)',
    'akiec': 'Actinic keratoses (akiec)',
    'vasc': 'Vascular lesions (vasc)',
    'df': 'Dermatofibroma (df)'
}

malignancy_map = {
    'nv': 'Benign', 'bkl': 'Benign', 'df': 'Benign', 'vasc': 'Benign',
    'mel': 'Malignant / Pre-Malignant', 
    'bcc': 'Malignant / Pre-Malignant', 
    'akiec': 'Malignant / Pre-Malignant'
}

df['disease_name'] = df['dx'].map(dx_mapping)
df['malignancy'] = df['dx'].map(malignancy_map)

# 3. Compute counts & percentages
counts = df['disease_name'].value_counts()
percents = df['disease_name'].value_counts(normalize=True) * 100

# 4. Set Plot Aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Custom color palette for disease types
color_dict = {
    'Melanocytic nevi (nv)': '#2b5c8f',
    'Melanoma (mel)': '#d95f02',
    'Benign keratosis (bkl)': '#41b6c4',
    'Basal cell carcinoma (bcc)': '#e7298a',
    'Actinic keratoses (akiec)': '#e6ab02',
    'Vascular lesions (vasc)': '#a6edd5',
    'Dermatofibroma (df)': '#7570b3'
}
bar_colors = [color_dict[name] for name in counts.index]
# Chart 1: Horizontal Bar Chart with Annotations
bars = axes[0].barh(counts.index, counts.values, color=bar_colors, edgecolor='black', alpha=0.85)
axes[0].invert_yaxis()
axes[0].set_title('Detailed Disease Class Distribution in HAM10000', fontsize=14, fontweight='bold', pad=15)
axes[0].set_xlabel('Number of Image Samples', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Skin Lesion Diagnosis Class', fontsize=12, fontweight='bold')

# Annotate exact count and percentage on each bar
for bar, count, pct in zip(bars, counts.values, percents.values):
    axes[0].text(
        bar.get_width() + 100, 
        bar.get_y() + bar.get_height()/2, 
        f'{count:,} ({pct:.2f}%)', 
        va='center', ha='left', fontsize=10, fontweight='bold'
    )
axes[0].set_xlim(0, 7800)

# Chart 2: Donut Chart (Benign vs. Malignant Breakdown)
mal_counts = df['malignancy'].value_counts()
colors_donut = ['#2b5c8f', '#d95f02']
wedges, texts, autotexts = axes[1].pie(
    mal_counts, 
    labels=mal_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors_donut, 
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
    textprops=dict(fontsize=12, fontweight='bold')
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)

axes[1].set_title('Overall Diagnostic Risk Profile\n(Benign vs. Malignant / Pre-Malignant)', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.show()
