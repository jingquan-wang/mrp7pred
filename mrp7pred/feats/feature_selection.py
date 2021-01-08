"""
Automated feature selection based on training data

Steps:
    1. Remove similar (highly-correlated) features
    2. Remove features with low variance
    3. Feature selection pipeline:
        - sklearn.feature_selection.GenericUnivariateSelect()
            chi2
            f_classif
            mutual_info_classif
        - sklearn.feature_selection.SelectFromModel()
            l1-based
            tree-based
        - sklearn.feature_selection.RFECV()
        - sklearn.feature_selection.SequentialFeatureSelector()

Need to automate the process
"""

from sklearn.feature_selection import (
    VarianceThreshold,
    GenericUnivariateSelect,
    chi2,
    f_classif,
    mutual_info_regression,
    SelectPercentile,
    RFECV,
    SelectFromModel,
    SequentialFeatureSelector,
)

from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Lasso
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from typing import Union, Dict, List, Tuple
from pandas import DataFrame
from numpy import ndarray

import pandas as pd
import numpy as np


def _remove_similar_features(X: DataFrame, threshold: float = 0.9) -> ndarray:
    """
    Remove features with high colinearity
    Use a graph-based method
    The goal is to remove actually identical features with different names
    """

