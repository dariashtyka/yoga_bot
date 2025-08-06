import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


names=['angle1', 'angle2', 'angle3', 'pose']
# Load the data
data = pd.read_csv("data_collection.csv", header=None, names=names)

# Separate features and labels
X = data[['angle1', 'angle2', 'angle3']]
y = data['pose']

grouped=data.groupby(['pose'])

# train_data=[]
# test_data=[]

# for pose_name, data_group in group:
#     if pose_name=="warrior2":
#         train_data_w2 = data_group[:7]  # first 7 rows
#         test_data_w2 = data_group[7:]   # remaining 3 rows
#     elif pose_name=="tree":
#         train_data_tree = data_group[:7]  # first 7 rows
#         test_data_tree = data_group[7:]   # remaining 3 rows
#     else:
#         train_data_dd = data_group[:7]  # first 7 rows
#         test_data_dd = data_group[7:]   # remaining 3 rows
#     #merge all data
#     train_data = pd.concat([train_data_tree, train_data_w2, train_data_dd])
#     test_data = pd.concat([test_data_tree, test_data_w2, test_data_dd])

train_parts = []
test_parts = []

for pose_name, group in grouped:
    train_parts.append(group.iloc[:7])  # first 7 rows
    test_parts.append(group.iloc[7:])   # remaining 3 rows

train_data = pd.concat(train_parts)
test_data = pd.concat(test_parts)

X_train=train_data[['angle1', 'angle2', 'angle3']]
y_train=train_data['pose']

X_test=test_data[['angle1', 'angle2', 'angle3']]
y_test=test_data['pose']


# Split into training and testing sets with scikitlearn library
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model= LogisticRegression()
model.fit(X_train, y_train)
y_res=model.predict(X_test)

#Testing results
print("Predictions:", y_res)
print("Actual labels:", y_test.values)
print("Accuracy:", model.score(X_test, y_test))