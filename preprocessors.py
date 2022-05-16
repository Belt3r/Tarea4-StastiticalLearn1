from select import select
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

### ============ Imputación de Variabel Numéricas ========
class NumericalImputerOperator(BaseEstimator, TransformerMixin):
    
    def __init__(self, imputerType = 'mean', varNames = None):
        self.varNames = varNames
        if(imputerType == 'mean'):
            self.imputerType = 'mean'
        elif(imputerType == 'median'):
            self.imputerType = 'median'
        else:
            print("Mecanismo de imputación invalido.\n")
 
    def fit(self, X, y = None):
        return self

    def transform(self, X, y = None):
        X = X.copy()
        for col in self.varNames:
            if(self.imputerType == 'mean'):
                imputerValue = np.round(X[col].mean(), 0)
            else:
                imputerValue = np.round(X[col].median(), 0)
            X[col].fillna(imputerValue, inplace=True)
        return X

### ============ Imputación de Variables Categoricas ========

### ============ Codificación de Variables Categoricas ========
class CategoricalEncoderOperator(BaseEstimator, TransformerMixin):

    def __init__(self, varNames = None, map_type='freq'):
        self.encoder_dict = {}
        self.varNames = varNames
        self.map_type = map_type

    def fit(self, X, y = None) -> None:
        """
            fit para calculo de diccionario de codificación
        """
        for col in self.varNames:
            factor_div = 1 if (self.map_type == 'freq') else len(X[col])
            self.encoder_dict[col] = (X[col].value_counts().sort_values(ascending=False)/factor_div).to_dict()
        return self
    
    def transform(self, X, y = None):
        """
            transforamción para variables, según diccionario de codificación
        """
        X = X.copy()
        for col in self.varNames:
            X[col] = X[col].map(self.encoder_dict[col])
        return X

### ============ Tratamiendo de Outliers ========
class OutliersTreatmentOperator(BaseEstimator, TransformerMixin):

    def __init__(self, factor = 1.75, varNames = None):
        self.varNames = varNames
        self.factor = factor

    def fit(self, X, y = None):
        for col in self.varNames:
            q3 = X[col].quantile(0.75)
            q1 = X[col].quantile(0.25)
            self.IQR = q3 - q1
            self.upper = q3 + self.factor*self.IQR
            self.lower = q1 - self.factor*self.IQR
        return self

    def transform(self, X, y = None):
        X = X.copy()
        for col in self.varNames:
            X[col] = np.where(X[col] >= self.upper, self.upper,
                np.where(
                    X[col] < self.lower, self.lower, X[col]
                )    
            )
        return X