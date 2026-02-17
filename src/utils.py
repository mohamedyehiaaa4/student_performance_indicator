import os 
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from src.logger import logging 
from src.exception import CustomException
import dill as pickle
from sklearn.model_selection import GridSearchCV


def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        logging.info("Error occured while saving the object")
        raise CustomException(e,sys)


def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report = {}
        model_list = []
        for i in range(len(models)):
            model = list(models.values())[i]
            param_grid = param.get(list(models.keys())[i], {})
            grid_search = GridSearchCV(model,param_grid,cv=5)
            grid_search.fit(X_train,y_train)
            
            y_test_pred = grid_search.predict(X_test)

            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            model_list.append(grid_search)

        return report, model_list

    except Exception as e:
        logging.info("Error occured while evaluating the model")
        raise CustomException(e,sys)