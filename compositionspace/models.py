from ast import Raise
from sklearn.ensemble import RandomForestClassifier
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN

def get_model(ml_params):
    """
    get machine learning model for clustering
    """
    model_name = ml_params["name"]
    model_params = ml_params[model_name]
    _available_models = ["randomforest"]

    if(model_name == "randomforest"):
        model = RandomForestClassifier(max_depth=model_params["max_depth"],
                            n_estimators=model_params["n_estimators"])
        return model
    if(model_name == "GaussianMixture"):
        model =  GaussianMixture(n_components = model_params["n_components"], max_iter=model_params["max_iter"],verbose=model_params["verbose"])
        return model 
    
    if(model_name == "DBScan"):
        model =  DBSCAN(eps= self.params["eps"], min_samples= model_params["min_samples"])
        return model       
        
    else:
        raise ValueError(f"Now implementation is found for the model {model_name}, choose from: {_available_models}")
