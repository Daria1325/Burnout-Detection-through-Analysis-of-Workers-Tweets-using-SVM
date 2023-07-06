import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
import time
time1 = time.perf_counter()

normal_df = pd.read_csv("data\\Dataset1\\Normal_Tweets.csv")
normal_df['type'] = "Normal"
normal_df['type_id'] = 0

stressed_df = pd.read_csv("data\Dataset1\Stressed_Tweets.csv")
stressed_df['type'] = "Stressed"
stressed_df['type_id'] = 2

lonely_df = pd.read_csv("data\Dataset1\Lonely_Tweets.csv")
lonely_df['type'] = "Lonely"
lonely_df['type_id'] = 3

all_data_df = pd.concat([normal_df,lonely_df], ignore_index=True)
all_data_df.drop(columns=['index'])

all_data_df = pd.concat([all_data_df, stressed_df], ignore_index=True)

np.savetxt(r'data\\Dataset1\\alldata.txt', all_data_df.text.values, fmt='%s')

type_id_df = all_data_df[['type', 'type_id']].drop_duplicates().sort_values('type_id')
type_to_id = dict(type_id_df.values)
id_to_type = dict(type_id_df[['type_id', 'type']].values)

fig = plt.figure(figsize=(8,6))
all_data_df.groupby('type').text.count().plot.bar(ylim=0)
# plt.show()


vectorizer = TfidfVectorizer(sublinear_tf=True,norm='l2')
text = vectorizer.fit_transform(all_data_df['text'].apply(lambda x: np.str_(x))).toarray()


labels = all_data_df['type_id']

X_train, X_test, y_train, y_test = train_test_split(text, labels,  test_size=0.2, random_state=0)
# X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,  test_size=0.1, random_state=42)




model = LinearSVC(class_weight='balanced', penalty='l2', C=1, max_iter=100, dual=False, tol=0.0001)

#clf = model.fit(X_train, y_train)
# calibrated_svc = CalibratedClassifierCV(base_estimator=model,cv="prefit")
calibrated_svc = CalibratedClassifierCV(base_estimator=model)
#calibrated_svc.fit(X_val,y_val)
calibrated_svc.fit(X_train,y_train)
predicted = calibrated_svc.predict(X_test)

score = calibrated_svc.score(X_train, y_train)
print("Model calibrated accurace score: ", score)

# print("Number of iterations: ",clf.n_iter_)


filename = 'saved_model\model2\model_dataset2.pkl'
with open(filename,'wb') as f:
    pickle.dump(calibrated_svc,f)

time2 = time.perf_counter()

print(f"Time =  {time2 - time1:0.4f} seconds")

conf_mat = confusion_matrix(y_test, predicted)
fig, ax = plt.subplots(figsize=(8,8))
sns.heatmap(conf_mat, annot=True, fmt='d',
            xticklabels=type_id_df.type.values, yticklabels=type_id_df.type.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()


print(metrics.classification_report(y_test, predicted, target_names=all_data_df['type'].unique()))

