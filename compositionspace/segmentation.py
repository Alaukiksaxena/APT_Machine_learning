from compositionspace.datautils import DataPreparation
from compositionspace.models import get_model
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import json 
import h5py
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from tqdm.notebook import tqdm
import os
from pyevtk.hl import pointsToVTK
from pyevtk.hl import gridToVTK#, pointsToVTKAsTIN
import yaml
import pyvista as pv

class CompositionClustering():
    
    def __init__(self, inputfile):
        if isinstance(inputfile, dict):
            self.params = inputfile
        else:
            with open(inputfile, "r") as fin:
                params = yaml.safe_load(fin)
            self.params = params
        self.version = "1.0.0"

    def get_PCA_cumsum(self, vox_ratio_file, vox_file):

        with h5py.File(vox_file,"r") as hdf:
            group = hdf.get("Group_sm_vox_xyz_Da_spec")
            group0 = hdf.get("0")
            spec_lst = list(list(group0.attrs.values())[1])

        with h5py.File(vox_ratio_file , "r") as hdfr:
            ratios = np.array(hdfr.get("vox_ratios"))
            ratios_columns = list(list(hdfr.attrs.values())[0])
            group_name = list(list(hdfr.attrs.values())[1])

        print(len(ratios))
        print((ratios_columns))

        ratios = pd.DataFrame(data=ratios, columns=ratios_columns)   

        X_train=ratios.drop(['Total_no','vox'], axis=1)
        PCAObj = PCA(n_components = len(spec_lst)) 
        PCATrans = PCAObj.fit_transform(X_train)
        PCACumsumArr = np.cumsum(PCAObj.explained_variance_ratio_)
        
        plt.figure(figsize=(5,5))
        plt.plot( range(1,len(PCACumsumArr)+1,1),PCACumsumArr,"-o")
        plt.ylabel("Explained Variance")
        plt.xlabel('Dimensions')
        plt.grid()
        output_path = os.path.join(self.params["output_path"], "PCA_cumsum.png")
        plt.savefig(output_path)
        plt.show()
        
        return PCACumsumArr, ratios

    
    
    def get_bics_minimization(self, vox_ratio_file, vox_file):
        
        with h5py.File(vox_file,"r") as hdf:
            group = hdf.get("Group_sm_vox_xyz_Da_spec")
            group0 = hdf.get("0")
            spec_lst = list(list(group0.attrs.values())[2])

        with h5py.File(vox_ratio_file , "r") as hdfr:
            ratios = np.array(hdfr.get("vox_ratios"))
            ratios_columns = list(list(hdfr.attrs.values())[0])
            group_name = list(list(hdfr.attrs.values())[1])

        ratios = pd.DataFrame(data=ratios, columns=ratios_columns) 
        
        gm_scores=[]
        aics=[]
        bics=[]
        
        X_train=ratios.drop(['Total_no','vox'], axis=1)
        
        n_clusters=list(range(1,self.params["bics_clusters"]))
        
        pbar = tqdm(n_clusters, desc="Clustering")
        for n_cluster in pbar:
            gm = GaussianMixture(n_components=n_cluster,verbose=0)
            gm.fit(X_train)
            y_pred=gm.predict(X_train)
            #gm_scores.append(homogeneity_score(y,y_pred))
            aics.append(gm.aic(X_train))
            bics.append(gm.bic(X_train))
            
        output_path = os.path.join(self.params["output_path"], "bics_aics.png")
        plt.plot(n_clusters, aics, "-o",label="AIC")
        plt.plot(n_clusters, bics, "-o",label="BIC")
        plt.legend()
        plt.savefig(output_path)
        plt.show()
        return self.params["bics_clusters"], aics, bics    
    
   
    def calculate_centroid(self, data):
        """
        Calculate centroid
        Parameters
        ----------
        data: pandas DataFrame or numpy array
        Returns
        -------
        centroid
        """
        if isinstance(data, pd.DataFrame):
            length = len(data['x'])
            sum_x = np.sum(data['x'])
            sum_y = np.sum(data['y'])
            sum_z = np.sum(data['z'])
            return sum_x/length, sum_y/length, sum_z/length
        else:
            length = len(data[:,0])
            sum_x = np.sum(data[:,0])
            sum_y = np.sum(data[:,1])
            sum_z = np.sum(data[:,2])
            return sum_x/length, sum_y/length, sum_z/length



    def get_voxel_centroid(self, vox_file, files_arr):

        with h5py.File(vox_file, "r") as hdf:
            items = list(hdf.items())
            item_lst = []
            for item in range(len(items)):
                item_lst.append([100000*(item),100000*(item+1)])
            item_lst = np.array(item_lst)

            dic_centroids = {}
            dic_centroids["x"]=[]
            dic_centroids["y"]=[]
            dic_centroids["z"] = []
            dic_centroids["file_name"] = []
            df_centroids = pd.DataFrame(columns=['x', 'y', 'z','filename'])
            
            for filename in files_arr:
                group = np.min(item_lst[[filename in range(j[0],j[1]) for j in item_lst]])
                xyz_Da_spec_atoms = np.array(hdf.get("{}/{}".format(group, filename)))
                x, y, z = self.calculate_centroid(xyz_Da_spec_atoms)
                dic_centroids["x"].append(x)
                dic_centroids["y"].append(y)
                dic_centroids["z"].append(z)
                dic_centroids["file_name"].append(filename)            
        return dic_centroids

    
    def get_composition_cluster_files(self, vox_ratio_file, vox_file, n_components):

        ml_params = self.params["ml_models"]
        
        with h5py.File(vox_file,"r") as hdf:
            group = hdf.get("Group_sm_vox_xyz_Da_spec")
            group0 = hdf.get("0")
            spec_lst = list(list(group0.attrs.values())[2])

        with h5py.File(vox_ratio_file , "r") as hdfr:
            ratios = np.array(hdfr.get("vox_ratios"))
            ratios_columns = list(list(hdfr.attrs.values())[0])
            group_name = list(list(hdfr.attrs.values())[1])

        ratios = pd.DataFrame(data=ratios, columns=ratios_columns) 
        
        X_train=ratios.drop(['Total_no','vox'], axis=1)
        
        gm = get_model(ml_params=ml_params)
        gm.fit(X_train)
        y_pred=gm.predict(X_train)
        
        cluster_lst = []
        for phase in range(n_components):
            cluster_lst.append(np.argwhere(y_pred == phase).flatten())        
        df_lst = []
        for cluster in cluster_lst:
            df_lst.append(ratios.iloc[cluster])
            
        #sorting
        cluster_lst_sort = []
        len_arr = np.array([len(x) for x in cluster_lst])
        sorted_len_arr = np.sort(len_arr)
        for length in sorted_len_arr:
            cluster_lst_sort.append(cluster_lst[np.argwhere(len_arr == length)[0,0]])

        #print([len(x) for x in cluster_lst_sort])
        cluster_lst = cluster_lst_sort
        
        return cluster_lst, ratios
    
    def get_composition_clusters(self, vox_ratio_file, vox_file, outfile="vox_centroid_file.h5"):
        voxel_centroid_output_file = []
        n_components = self.params["n_phases"]
        ml_params = self.params["ml_models"]
        cluster_lst, ratios = self.get_composition_cluster_files(vox_ratio_file, vox_file, n_components)

        plot_files = []
        for phase in range(len(cluster_lst)):
            cluster_files = []
            cluster = cluster_lst[phase]
            for voxel_id in cluster:
                cluster_files.append(ratios['vox'][voxel_id])
            plot_files.append(cluster_files)

        plot_files_group = []
        for cluster_files in plot_files:
            plot_files_group.append([int(file_num) for file_num in cluster_files ])
            
        with h5py.File(vox_file,"r") as hdf_sm_r:
            hdf_sm_r = h5py.File(vox_file,"r")
            group = hdf_sm_r.get("0")
            #total_voxels =list(list(group.attrs.values())[0])
            total_voxels =list(list(group.attrs.values())[2])

            total_voxels_int =""
            for number in total_voxels:
                total_voxels_int = total_voxels_int + number

            total_voxels_int = int(total_voxels_int)
            hdf_sm_r.close()
            plot_files_cl_All_group = [file_num for file_num in range(total_voxels_int)]
            
        plot_files_group.append(plot_files_cl_All_group)
        output_path = os.path.join(self.params["output_path"], outfile)
        with h5py.File(output_path,"w") as hdfw:
            for cluster_file_id in range(len(plot_files_group)):

                G = hdfw.create_group(f"{cluster_file_id}")
                G.attrs["what"] = ["Centroid of voxels"]
                G.attrs["howto_Group_name"] = ["Group_sm_vox_xyz_Da_spec/"]
                G.attrs["colomns"] = ["x","y","z","file_name"]

                CentroidsDic = self.get_voxel_centroid(vox_file, plot_files_group[cluster_file_id])
                G.create_dataset(f"{cluster_file_id}", data = pd.DataFrame.from_dict(CentroidsDic).values)

        self.voxel_centroid_output_file = output_path

    
    def generate_plots(self):

        vtk_files = []
        with h5py.File(self.voxel_centroid_output_file, "r") as hdfr:            
            groups =list(hdfr.keys())
            for group in range(len(groups)-1):
                phase_arr =  np.array(hdfr.get(f"{group}/{group}"))
                phase_columns = list(list(hdfr.get(f"{group}").attrs.values())[0])
                phase_cent_df =pd.DataFrame(data=phase_arr, columns=phase_columns)
                
                image = phase_cent_df.values
                
                file_path = self.voxel_centroid_output_file + f"_{group}"
               
                vtk_files.append(file_path + ".vtu")

                x = np.ascontiguousarray(image[:,0])
                y= np.ascontiguousarray(image[:,1])
                z = np.ascontiguousarray(image[:,2])
                label = np.ascontiguousarray( image[:,3])

                pointsToVTK(file_path, x, y, z, data = {"label" : label}  )
        self.vtk_files = vtk_files

    
    def plot3d(self, **kwargs):
        self.generate_plots()
        for file in self.vtk_files:
            grid = pv.read(file)
            grid.plot(**kwargs, jupyter_backend="panel")



