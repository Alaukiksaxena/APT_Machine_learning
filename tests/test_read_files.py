import pytest
import numpy as np
import os
import sys
from compositionspace.datautils import DataPreparation
def test_file_rrng():
    data = DataPreparation("tests/experiment_params.yaml")
    datarrng = data.get_rrng("tests/data/R31_06365-v02.rrng")
    assert datarrng[0]["name"].values[0] == "C"
    
def test_file_pos():
    data = DataPreparation("tests/experiment_params.yaml")
    datapos = data.get_pos("tests/data/R31_06365-v02.pos")
    assert np.isclose(datapos[0][0]+5.3784895, 0)

def test_file_df():
    data = DataPreparation("tests/experiment_params.yaml")
    data = data.get_apt_dataframe()
    assert np.isclose(data[0][0]["x"].values[0]+5.3784895, 0)
    assert data[1][0] == 'R31_06365-v02.pos'
    assert data[2]["name"].values[0] == "C"
    assert np.isclose(data[3]["lower"].values[0]-5.974, 0)

def test_chunkify():
    data = DataPreparation("tests/experiment_params.yaml")
    data.get_big_slices()
    assert os.path.exists(data.chunk_files[0]) == True

def test_voxelise():
    data = DataPreparation("tests/experiment_params.yaml")
    data.get_big_slices()
    data.get_voxels()
    data.calculate_voxel_composition()
    assert os.path.exists(data.voxel_ratio_file) == True

    
