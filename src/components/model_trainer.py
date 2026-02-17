import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models



@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=  ModelTrainerConfig()
    

    def initiate_model_trainer(self,train_array,test_array,preproccessor_obj_file_path):
        try:
            logging.info("Splitting training and test input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K-Neighbors Regressor":KNeighborsRegressor(),
                "XGBRegressor":XGBRegressor(),
                "CatBoosting Regressor":CatBoostRegressor(verbose=False)
            }
            params={
                "Decision Tree":{
                    "max_depth":[3,5,7,10],
                    "min_samples_split":[2,5,10],
                    "min_samples_leaf":[1,2,5]
                },
                "Random Forest":{
                    "n_estimators":[100,200,300],
                    "max_depth":[3,5,7]
                },
                "Gradient Boosting":{
                    "learning_rate":[0.1,0.2,0.3],
                    "n_estimators":[100,200,300]
                },
                "XGBRegressor":{
                    "learning_rate":[0.1,0.2,0.3],
                    "n_estimators":[100,200,300]
                },
                "Linear Regression":{},
                "K-Neighbors Regressor":{},
                "CatBoosting Regressor":{}
            }
            model_report, trained_models = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info(f"Best model found on both training and testing dataset: {best_model_name} with r2 score: {best_model_score}")

            best_model_index = list(model_report.keys()).index(best_model_name)
            best_fitted_model = trained_models[best_model_index]

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_fitted_model
            )
            predicted = best_fitted_model.predict(X_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square



        except Exception as e:
            logging.info("Error occured during model training")
            raise CustomException(e,sys)




