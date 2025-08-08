import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree


names = ['angle1', 'angle2', 'angle3', 'pose']
# Load the data
data = pd.read_csv("data_collection.csv", header=None, names=names)

# Separate features and labels
X = data[['angle1', 'angle2', 'angle3']]
y = data['pose']

grouped = data.groupby(['pose'])

train_parts = []
test_parts = []

for pose_name, group in grouped:
    train_parts.append(group.iloc[:7])  # first 7 rows
    test_parts.append(group.iloc[7:])   # remaining 3 rows

train_data = pd.concat(train_parts)
test_data = pd.concat(test_parts)

X_train = train_data[['angle1', 'angle2', 'angle3']]
y_train = train_data['pose']

X_test = test_data[['angle1', 'angle2', 'angle3']]
y_test = test_data['pose']


# OR Split into training and testing sets with scikitlearn library
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Logisitic regression
model_lr = LogisticRegression()
model_lr.fit(X_train, y_train)
y_res_lr = model_lr.predict(X_test)

#Decision Tree
# model_tree= DecisionTreeClassifier()
# model_tree.fit(X_train, y_train)
# y_res_tree=model_tree.predict(X_test)

#KNN
# model_knn= KNeighborsClassifier(n_neighbors=3)
# model_knn.fit(X_train, y_train)
# y_res_knn=model_knn.predict(X_test)

# Save the model to a file
joblib.dump(model_lr, 'yoga_pose_model.joblib')

#Testing results Logistic Regression
# print("Predictions:", y_res_lr)
# print("Actual labels:", y_test.values)
# print("Accuracy:", model_lr.score(X_test, y_test))

# print("Classes:", model_lr.classes_)
# print("Coefficients:\n", model_lr.coef_)

#Testing results Decision Tree
# print("Predictions:", y_res_tree)
# print("Actual labels:", y_test.values)
# print("Accuracy:", model_tree.score(X_test, y_test))
# plt.figure(figsize=(10, 7))
# plot_tree(model_tree, feature_names=['angle1', 'angle2', 'angle3'], class_names=model_tree.classes_, filled=True)
# plt.show()

#Testing results KNN
# print("Predictions:", y_res_knn)
# print("Actual labels:", y_test.values)
# print("Accuracy:", model_knn.score(X_test, y_test))
# print(model_knn.kneighbors(X_test))