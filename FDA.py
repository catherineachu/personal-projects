import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from scipy.linalg import inv, det
from sklearn.metrics import accuracy_score

#circular data
def generate_circular_data():
    X, y = make_circles(n_samples=400, noise=0.1, factor=0.3, random_state=42)
    return X, y

#plot the data
def plot_dataset(X, y, title):
    plt.figure(figsize=(6, 5))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, edgecolors="k")
    plt.title("Original Space")
    plt.xlabel("x1: feature 1")
    plt.ylabel("x2: feature 2")
    plt.show()

#compute class means
def compute_class_means(X, y):
    X_class1 = X[y == 0]
    X_class2 = X[y == 1]
    
    #mean of class1, class2
    mu1 = np.mean(X_class1, axis=0) 
    mu2 = np.mean(X_class2, axis=0)
    return mu1, mu2

#create the scatter matrix for both variables
def compute_within_class_scatter(X, y, mu1, mu2):
    X_class1 = X[y == 0]
    X_class2 = X[y == 1]
    
    # Compute the scatter matrix for class 1
    S1 = np.sum([(x - mu1).reshape(-1, 1) @ (x - mu1).reshape(1, -1) for x in X_class1], axis=0)
    # Compute the scatter matrix for class 2
    S2 = np.sum([(x - mu2).reshape(-1, 1) @ (x - mu2).reshape(1, -1) for x in X_class2], axis=0)
    SW = S1 + S2
    return SW

#scatter matrix between classes
def compute_between_class_scatter(mu1, mu2):
    SB = np.outer((mu1 - mu2), (mu1 - mu2))
    return SB

#eigenvalue
def compute_fda_projection(SW, SB):
    eigvals, eigvecs = np.linalg.eig(np.linalg.inv(SW).dot(SB)) 
    #choose the eigenvector with the largest eigenvalue
    w = eigvecs[:, np.argmax(eigvals)]
    return w

#project data onto the new discriminant axis
def apply_fda(X, w):
    return X @ w 

#gaussian parameters
def compute_gaussian_params(X_fda, y):
    means = {}
    covariance = {}
    priors = {}
    
    for class_id in np.unique(y):
        class_proj = X_fda[y == class_id]
        means[class_id] = np.mean(class_proj, axis=0)  # Mean of each class in the new space
        covariance[class_id] = np.atleast_2d(np.cov(class_proj, rowvar=False))  # Covariance matrix
        priors[class_id] = class_proj.shape[0] / len(y)  # Prior probability of each class
    
    return means, covariance, priors

def gaussian_distribution(x, mean, cov):
    scalar = (1. / np.sqrt(2 * np.pi * det(cov))) 
    x_sub_mean = x - mean
    return scalar * np.exp(-0.5 * (x_sub_mean.T @ inv(cov) @ x_sub_mean))

def classify_gaussian(X_fda, means, covariance, priors):
    predictions = []
    
    for x in X_fda:
        likelihoods = []
        for class_id in means.keys():
            likelihood = priors[class_id] * gaussian_distribution(x, means[class_id], covariance[class_id])
            likelihoods.append(likelihood)
        
        predictions.append(np.argmax(likelihoods))  # Select class with highest likelihood
    
    return np.array(predictions)

#train and evaluate models
def evaluate_fda_classifier(X_fda, y, means, covariance, priors):
    X_train, X_test, y_train, y_test = train_test_split(X_fda, y, test_size=0.3, random_state=42)
    y_pred = classify_gaussian(X_test, means, covariance, priors)
    #get the accuracy for each value
    accuracy = np.sum(y_pred == y_test) / len(y_test) 
    return accuracy

#linear regression model is the baseline model
def evaluate_baseline_classifier(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    baseline_clf = LogisticRegression()
    baseline_clf.fit(X_train, y_train)
    y_pred = baseline_clf.predict(X_test)
    #get the accuracy for the logistic model
    accuracy = accuracy_score(y_test, y_pred) 
    return accuracy

#generate the plot
X, y = generate_circular_data()
plot_dataset(X, y, "Original Circular Dataset")
X = StandardScaler().fit_transform(X) 

#call the functions made above
mu1, mu2 = compute_class_means(X, y)  
SW = compute_within_class_scatter(X, y, mu1, mu2) 
SB = compute_between_class_scatter(mu1, mu2)  
w = compute_fda_projection(SW, SB)  

#apply FDA and compute gaussian parameters
X_fda = apply_fda(X, w).reshape(-1, 1)  
means, covariance, priors = compute_gaussian_params(X_fda, y) 
fda_accuracy = evaluate_fda_classifier(X_fda, y, means, covariance, priors)
baseline_accuracy = evaluate_baseline_classifier(X, y)

# Compare Performance
print(f"Baseline Model (logistic regression) Accuracy: {baseline_accuracy:.2f}")
print(f"FDA + Gaussian Classifier Accuracy: {fda_accuracy:.2f}")

#plot the FDA axis
plt.figure(figsize=(6, 5))
plt.scatter(X_fda, np.zeros_like(X_fda), c=y, cmap=plt.cm.Paired, edgecolors="k")
plt.title("FDA Projection - 1D Separation")
plt.xlabel("FDA Component")
plt.ylabel("x2")
plt.show()

#performance 
plt.figure(figsize=(6, 5))
plt.bar(["Baseline linear Model", "FDA Classifier"], [baseline_accuracy, fda_accuracy], color=['red', 'green'])
plt.ylim(0, 1)
plt.ylabel("Classification Accuracy")
plt.title("Performance Comparison")
plt.show()
