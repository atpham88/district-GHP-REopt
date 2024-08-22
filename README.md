## Summary
- This repo provides scripts to process inputs, run REopt model, and post process outputs to perform LCCA for pre-sized district GHP system.
- To prepare to run the scripts in this repo, clone the repo and adjust the inputs in `data` folder and `addInputs.py`.

## 1. Set up environment
`conda env create -f environment.yml`

## 2. Prepare run
Before running the model, you need to prepare your run folder and get your data input ready. 
- To prepare your run folder, in the downloaded repo, copy the `data_folder_sample` folder and place it anywhere on your local or remote machine where you want your outputs to be.
- Rename `data_folder_sample` to the name of the scenario of your run, for example `"with_ghp"` or `"bau"`.
- After renaming the data folder, add your data input in for your run following the data structure and format of the files in the folder. Required data include:
  - Timeseries data (including electric consumption of building and GHX) are defined in `building.xlsx` tab `Timeseries`. Note that building id is identified at the end of each data field after an `_`. For example, `_sdupkgra` means the timeseries associated with `building_sdupkgra`.
  - GHP sizes and building-level data are defined in `building.xlsx` tab `GHP`.
  - GHX sizes and site information are defined in `district.csv`. 

## 3. How to run scripts for district GHP LCCA in REopt's Julia package
- Scripts are run using `run_julia.sh` file.
- Before running, go into `run_julia.sh` and revise:
  - `run_path` argument to include the path of your run folder defined in step 3  
  - `scenario_name` argument to match with the name of the data input folder you just defined above. For example: if you data input folder is `"with_ghp"`, then `scenario_name = "with_ghp"`.
- To run REopt-GHP LCCA, in terminal, simply type `sh run_julia.sh`
- `run_julia.sh` runs a few scripts sequentially:
    1) `processInputs.py` which processes all the inputs specified in `addInputs.py` and generates REopt-format json inputs file for the buildings and the district GHX;
    2) `runREopt.jl` which runs REopt to perform LCCA for each of the buildings and the district GHX;
    3) `processOutputs.py` which processes all the json outputs from REopt and combine them together to create a district json output, as well as a csv summary file with financial outputs for each building, for the district GHX, and total district financial outputs.
- Please use the `ghp-district` branch to run for now. Can use main to run at the end of this FY when changes are merged in.

## 4. How to run scripts for district GHP LCCA by calling REopt's API
- Repeat the same steps as in step 3 but in `run_api.sh`

## 5. Outputs
- Individual json outputs generated directly from running REopt are saved in `results_json` in the run folder.
- Postprocessed total district json output and csv summary are saved in `results_summary` folder.


