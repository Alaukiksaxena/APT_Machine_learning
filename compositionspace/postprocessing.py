import pandas as pd
import os
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import numpy as np
import h5py    
from sklearn.cluster import DBSCAN
from pyevtk.hl import pointsToVTK
from pyevtk.hl import gridToVTK
import yaml

class DataPostprocess:
    
    def __init__(self, inputfile):
        if isinstance(inputfile, dict):
            self.params = inputfile
        else:
            with open(inputfile, "r") as fin:
                params = yaml.safe_load(fin)
            self.params = params
        self.version = "1.0.0"

    def get_post_centroids(self, voxel_centroid_phases_files, cluster_id):
        
        """
        Reads the voxel centroids for a phase  

        Parameters
        ----------
        voxel_centroid_phases_files : str, Voxel cetroids corresponding to each phase
        cluster_id: int, phase id in Voxel_centroid_phases_files

        Returns
        -------
        pandas dataframe for voxel cetroids(x,y,z, voxelId), pandas dataframe for voxel cetroids(x,y,z),
        list of coloumn names (x,y,z, voxelId)
        
        Notes
        -----
        input is taken from composition space based segmentation of phases.
        """


        with h5py.File(voxel_centroid_phases_files , "r") as hdfr:
            group = cluster_id
            Phase_arr =  np.array(hdfr.get(f"{group}/{group}"))
            Phase_columns = list(list(hdfr.get(f"{group}").attrs.values())[0])
            Phase_cent_df =pd.DataFrame(data=Phase_arr, columns=Phase_columns)

            Df_centroids = Phase_cent_df.copy()
            Df_centroids_no_files = Df_centroids.drop(['file_name'] , axis=1)
            files = Df_centroids['file_name']

        return Df_centroids_no_files, Df_centroids, Phase_columns

        
    def DBSCAN_clustering(self, voxel_centroid_phases_files, cluster_id, 
        plot= False, plot3d = False, save =False):
        """
        Get individual clusters or precipitates corresponding to each phase/ chemical domain.
        DBSCAN is applied on the centroids of the voxels helping to remove noisy voxels around clusters.

        Parameters
        ----------
        cluster_id: int,id of the phase/chemical domain in Output_voxel_cetroids_phases.h5
        
        eps: float,epsilon is a hyperparameter for DBSCAN.The maximum distance between two samples for one to be 
        considered as in the neighborhood of the other. This is not a maximum bound on the distances of 
        points within a cluster.
        
        min_smaples: int, min_smaples is a hyperparameter for DBSCAN. The number of samples (or total weight) in a
        neighborhood for a point to be considered as a core point. This includes the point itself.
        
        plot: boolean, if true plots the histogram of the cluster for found by the DBSCAN algorithm.
        
        plot3d: boolean, if true plots voxel centroids in corresponding to each precipitate and outputs a .vtu file .
        
        save: boolean, saves a .h5 file corresponding to a cluster_id containing centroids for each precipitate.
        

        Returns
        -------
        Voxel centroids corresponding to each precipitate.
        
        
        Notes
        -----
        input is taken from composition space based segmentation of phases.
        """        
        eps = self.params["ml_models"]["DBScan"]["eps"]
        min_samples = self.params["ml_models"]["DBScan"]["min_samples"]

        Df_centroids_no_files, Df_centroids, Phase_columns = self.get_post_centroids( voxel_centroid_phases_files ,cluster_id)

        db = DBSCAN(eps=eps, min_samples= min_samples).fit(Df_centroids_no_files.values) #eps=5., min_samples= 35
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)
        if plot == True:
            plt.hist(labels,bins = 100);

        cluster_combine_lst = []

        for i in np.unique(labels):
            if i !=-1:
                cl_idx =np.argwhere(labels==i).flatten()
                cl_cent=Df_centroids_no_files.iloc[cl_idx]
                cl_cent["ID"] = [i]*len(cl_cent)
                cluster_combine_lst.append(cl_cent)

        if plot3d == True: 
            OutFile = os.path.join(self.params["output_path"], f"Output_DBSCAN_segmentation_phase{cluster_id}")
            Df_comb = pd.concat(cluster_combine_lst)
            image = Df_comb.values
            x = np.ascontiguousarray(image[:,0])
            y= np.ascontiguousarray(image[:,1])
            z = np.ascontiguousarray(image[:,2])
            label = np.ascontiguousarray( image[:,3])
            pointsToVTK(OutFile,x,y,z, data = {"label" : label}  )

        if save == True:
            OutFile = os.path.join(self.params["output_path"], f"Output_DBSCAN_segmentation_phase{cluster_id}")
            with h5py.File(OutFile, "w") as hdfw:
                G = hdfw.create_group(f"{cluster_id}")
                G.attrs["columns"] = Phase_columns
                for i in tqdm(np.unique(labels)):
                    if i !=-1:
                        cl_idx =np.argwhere(labels==i).flatten()
                        cl_cent=Df_centroids.iloc[cl_idx]
                        G.create_dataset("{}".format(i), data = cl_cent.values)


    


 