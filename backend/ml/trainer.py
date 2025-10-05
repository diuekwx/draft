import pandas as pd
import numpy as np
from syngergy import get_counter_score, get_synergy_score, build_stats, encode_matches 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier

df = pd.read_csv("matches.csv")
df = df.dropna(subset=["winners", "losers"])

df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

all_champs = set()
for col in ["winners", "losers"]:
    df[col].str.split(",").apply(all_champs.update)
all_champs = sorted(all_champs)
champ_to_idx = {champ: i for i, champ in enumerate(all_champs)}

pair_winrates_train, counter_winrates_train = build_stats(df_train)

X_train, y_train = encode_matches(df_train, champ_to_idx)
X_test, y_test = encode_matches(df_test, champ_to_idx)

# print("Train features:", X_train.shape, "Test features:", X_test.shape)

# # train model
# model = LogisticRegression(max_iter=1000)
# model.fit(X_train, y_train)

# # evaluate
# y_pred_train = model.predict(X_train)
# y_pred_test = model.predict(X_test)

# print("Train Accuracy:", accuracy_score(y_train, y_pred_train))
# print("Test Accuracy:", accuracy_score(y_test, y_pred_test))

mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64),  
    activation='relu',
    solver='adam',
    alpha=1e-4,                    
    learning_rate_init=0.001,      
    max_iter=100,                  
    early_stopping=True,          
    n_iter_no_change=10,
    random_state=42
)
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)

print("Train Accuracy:", mlp.score(X_train, y_train))
print("Test Accuracy:", mlp.score(X_test, y_test))