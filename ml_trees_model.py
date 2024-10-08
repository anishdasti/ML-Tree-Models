# -*- coding: utf-8 -*-
"""ML-Trees-Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eqB9PFkef9_W9iLVO1Baz5JwfjWsimrf
"""

import pandas as pd

# Direct URL to the wine quality dataset from UCI ML repository
red_wine_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'

# Loading data
red_wine_data = pd.read_csv(red_wine_url, sep=';')

# Display the first few rows of the data to ensure it's loaded properly
print("Red Wine Data Head:")
print(red_wine_data.head())

# Check for null values
print("Red Wine Null Values:")
print(red_wine_data.isnull().sum())

# Summary statistics for red and white wine data
print("\nRed Wine Data Summary:")
print(red_wine_data.describe())

import matplotlib.pyplot as plt

# Histograms for red wine data
red_wine_data.hist(bins=20, figsize=(10, 10))
plt.suptitle("Red Wine Attributes Distribution")
plt.show()

from sklearn.preprocessing import StandardScaler

# Defining predictors (X) and target (y) for both datasets
X_red = red_wine_data.drop('quality', axis=1)
y_red = red_wine_data['quality']

# Standardize the features
scaler = StandardScaler()
X_red_scaled = scaler.fit_transform(X_red)

import seaborn as sns

# Red Wine Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(red_wine_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix for Red Wine Data')
plt.show()

# Correlation of each attribute with the target variable 'quality'
red_corr_with_quality = red_wine_data.corr()['quality'].sort_values(ascending=False)
print("Red Wine Correlation with Quality:")
print(red_corr_with_quality)

# Selecting attributes with a correlation threshold (e.g., abs(correlation) > 0.1)
important_red_attributes = red_corr_with_quality[abs(red_corr_with_quality) > 0.1].index
print("\nImportant Attributes for Red Wine based on Correlation:")
print(important_red_attributes)

# Subsetting the data to only include important attributes
X_red_selected = red_wine_data[important_red_attributes.drop('quality')]

X_red_scaled_selected = scaler.fit_transform(X_red_selected)

from sklearn.model_selection import train_test_split

# Split the standardized selected features into training and testing sets
X_train_red, X_test_red, y_train_red, y_test_red = train_test_split(
    X_red_scaled_selected, y_red, test_size=0.2, random_state=42)

# Importing necessary libraries
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import graphviz
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Define a function to evaluate models for classification
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Classification report with zero_division parameter
    report = classification_report(y_test, predictions, zero_division=1)

    # Confusion matrix
    cm = confusion_matrix(y_test, predictions)

    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:\n", report)
    print("Confusion Matrix:\n", cm)

"""Plain Decision Tree Classifier"""

from sklearn.tree import DecisionTreeClassifier

# Decision Tree Classifier
dt = DecisionTreeClassifier(random_state=42)

# Parameters for GridSearchCV
params_dt = {'max_depth': [3, 5, 10, None], 'min_samples_split': [2, 5, 10]}

# GridSearchCV for Decision Tree
grid_dt = GridSearchCV(dt, params_dt, cv=5, scoring='accuracy')  # Use accuracy for classification
grid_dt.fit(X_train_red, y_train_red)

# Best estimator
best_dt = grid_dt.best_estimator_
print("Best parameters for Decision Tree:", grid_dt.best_params_)

# Evaluate the Decision Tree
print("Decision Tree Evaluation:")
evaluate_model(best_dt, X_test_red, y_test_red)

"""Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

# Random Forest Classifier
rf = RandomForestClassifier(random_state=42)

# Parameters for GridSearchCV
params_rf = {'n_estimators': [100, 200], 'max_depth': [3, 5, 10], 'min_samples_split': [2, 5, 10]}

# GridSearchCV for Random Forest
grid_rf = GridSearchCV(rf, params_rf, cv=5, scoring='accuracy')  # Use accuracy for classification
grid_rf.fit(X_train_red, y_train_red)

# Best estimator
best_rf = grid_rf.best_estimator_
print("Best parameters for Random Forest:", grid_rf.best_params_)

# Evaluate the Random Forest
print("Random Forest Evaluation:")
evaluate_model(best_rf, X_test_red, y_test_red)

"""Adaboost Classifier"""

from sklearn.ensemble import AdaBoostClassifier

# AdaBoost Classifier
ada = AdaBoostClassifier(random_state=42)

# Parameters for GridSearchCV
params_ada = {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 1.0]}

# GridSearchCV for AdaBoost
grid_ada = GridSearchCV(ada, params_ada, cv=5, scoring='accuracy')  # Use accuracy for classification
grid_ada.fit(X_train_red, y_train_red)

# Best estimator
best_ada = grid_ada.best_estimator_
print("Best parameters for AdaBoost:", grid_ada.best_params_)

# Evaluate the AdaBoost Classifier
print("AdaBoost Evaluation:")
evaluate_model(best_ada, X_test_red, y_test_red)

"""XGBoost Classifier"""

from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

le = LabelEncoder()

# Fit and transform the training target variable
y_train_encoded = le.fit_transform(y_train_red)

# Transform the testing target variable
y_test_encoded = le.transform(y_test_red)

# XGBoost Classifier
xgb = XGBClassifier(eval_metric='mlogloss')  # Removed use_label_encoder parameter

# Parameters for GridSearchCV
params_xgb = {'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1, 0.3], 'max_depth': [3, 5, 10]}

# GridSearchCV for XGBoost
grid_xgb = GridSearchCV(xgb, params_xgb, cv=5, scoring='accuracy')
grid_xgb.fit(X_train_red, y_train_encoded)

# Best estimator
best_xgb = grid_xgb.best_estimator_
print("Best parameters for XGBoost:", grid_xgb.best_params_)

# Evaluate the XGBoost Classifier
print("XGBoost Evaluation:")
evaluate_model(best_xgb, X_test_red, y_test_encoded)

"""Visualizing the models"""

from sklearn.tree import export_graphviz
import graphviz

# Visualize the best Decision Tree
dot_data = export_graphviz(best_dt, out_file=None,
                           feature_names=X_red_selected.columns,
                           filled=True, rounded=True, special_characters=True)

# Create graph from dot data
graph = graphviz.Source(dot_data)
graph

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Visualize a single tree from the Random Forest
plt.figure(figsize=(20, 10))
plot_tree(best_rf.estimators_[0], feature_names=X_red_selected.columns, filled=True, rounded=True)
plt.title("Random Forest - Single Tree Visualization")
plt.show()

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Visualize a single weak learner (tree) from AdaBoost
plt.figure(figsize=(20, 10))
plot_tree(best_ada.estimators_[0], feature_names=X_red_selected.columns, filled=True, rounded=True)
plt.title("AdaBoost - Single Tree Visualization")
plt.show()

from xgboost import plot_tree

# Visualize a single tree from the XGBoost model
plt.figure(figsize=(20, 10))
plot_tree(best_xgb, num_trees=0)  # Visualizing the first tree
plt.title("XGBoost - Single Tree Visualization")
plt.show()

from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support, roc_curve, precision_recall_curve, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import roc_curve, precision_recall_curve, auc
import matplotlib.pyplot as plt
import numpy as np

# Function to plot ROC curve
def plot_roc_curve(model, X_test, y_test, model_name):
    if hasattr(model, "predict_proba"):
        y_pred_prob = model.predict_proba(X_test)
    else:
        y_pred_prob = model.decision_function(X_test)

    # One-vs-Rest strategy: compute ROC curve for each class
    fpr = {}
    tpr = {}
    roc_auc = {}
    n_classes = len(np.unique(y_test))

    # Create ROC curves for each class
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test == i, y_pred_prob[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Plot ROC curve for each class with improved styling
    plt.figure(figsize=(10, 7))
    for i in range(n_classes):
        plt.plot(fpr[i], tpr[i], lw=2, label=f'Class {i} (area = {roc_auc[i]:0.2f})')

    # Reference line
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', lw=2)

    # Set axis limits and labels
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title(f'ROC Curve for {model_name}', fontsize=15)
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True)
    plt.show()

# Function to plot Precision-Recall curve
def plot_precision_recall_curve(model, X_test, y_test, model_name):
    if hasattr(model, "predict_proba"):
        y_pred_prob = model.predict_proba(X_test)
    else:
        y_pred_prob = model.decision_function(X_test)

    # One-vs-Rest strategy: compute Precision-Recall curve for each class
    precision = {}
    recall = {}
    pr_auc = {}
    n_classes = len(np.unique(y_test))

    # Create Precision-Recall curves for each class
    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(y_test == i, y_pred_prob[:, i])
        pr_auc[i] = auc(recall[i], precision[i])

    plt.figure(figsize=(10, 7))
    for i in range(n_classes):
        plt.plot(recall[i], precision[i], lw=2, label=f'Class {i} (area = {pr_auc[i]:0.2f})')

    # Set axis labels and title
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title(f'Precision-Recall Curve for {model_name}', fontsize=15)
    plt.legend(loc="lower left", fontsize=10)
    plt.grid(True)
    plt.show()

plot_roc_curve(best_dt, X_test_red, y_test_red, "Decision Tree")
plot_precision_recall_curve(best_dt, X_test_red, y_test_red, "Decision Tree")

plot_roc_curve(best_rf, X_test_red, y_test_red, "Random Forest")
plot_precision_recall_curve(best_rf, X_test_red, y_test_red, "Random Forest")

plot_roc_curve(best_ada, X_test_red, y_test_red, "AdaBoost")
plot_precision_recall_curve(best_ada, X_test_red, y_test_red, "AdaBoost")

plot_roc_curve(best_xgb, X_test_red, y_test_red, "XGBoost")
plot_precision_recall_curve(best_xgb, X_test_red, y_test_red, "XGBoost")