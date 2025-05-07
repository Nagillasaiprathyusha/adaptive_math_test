from sklearn.tree import DecisionTreeClassifier

# Sample dataset: [correct, time, prev_difficulty] -> next_difficulty
X = [
    [1, 6.5, 2], [0, 12.0, 2], [1, 5.0, 1],
    [0, 10.0, 3], [1, 4.0, 3], [0, 9.5, 1]
]
y = [3, 1, 2, 2, 3, 1]

model = DecisionTreeClassifier()
model.fit(X, y)

def predict_difficulty(correct, time_taken, current_difficulty):
    # Simplified difficulty adjustment
    if correct:
        return min(3, current_difficulty + 1)
    else:
        return max(1, current_difficulty - 1)
