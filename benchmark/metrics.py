"""
Metrics
Author: Gerald M

Metrics to check the similarity between predicted and true masks. Each function
takes the true and predicted masks as a binary/boolean image. They should
already be thresholded before testing for similarity.
"""

import numpy as np
from skimage.measure import regionprops, label

# Jaccard similarity score
# Returns the same as the sklearn.metrics.jaccard_score, but not the same as
# sklearn.metrics.jaccard_similarity_score.
def jaccard(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    return np.float(np.sum(true * pred))/np.sum((true + pred)>0)

def truepos(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    return np.sum(true * pred)

def falsepos(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    return np.sum((1-true) * pred)

def trueneg(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    return np.sum((1-true) * (1-pred))

def falseneg(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    return np.sum(true * (1-pred))

def accuracy(true, pred):
    tp = truepos(true, pred)
    fp = falsepos(true, pred)
    tn = trueneg(true, pred)
    fn = falseneg(true, pred)

    return np.float(tp+tn)/(tp+tn+fp+fn)

def precision(true, pred):
    tp = truepos(true, pred)
    fp = falsepos(true, pred)

    return np.float(tp)/(tp+fp)

def recall(true, pred):
    tp = truepos(true, pred)
    fn = falseneg(true, pred)

    return np.float(tp)/(tp+fn)

def colocalisedhits(true, pred):
    # Threshold the images to generate boolean masks
    true = (true>(np.max(true)-np.min(true))/2.).astype(np.int)
    pred = (pred>(np.max(pred)-np.min(pred))/2.).astype(np.int)

    true_label = label(true, connectivity=true.ndim)

    # Get centroids for centre of true objects
    centroids = np.array([list(region.centroid) for region in regionprops(true_label)]).astype(np.int)

    # Get the values at location of true centroids
    true_hits = true[centroids[:,0], centroids[:,1]]
    pred_hits = pred[centroids[:,0], centroids[:,1]]

    true_sum = np.sum(true_hits) # The number of true objects
    pred_sum = np.sum(pred_hits) # The number of predicted objects at true object position

    return np.float(pred_sum)/true_sum
