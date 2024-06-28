using Pkg
using JSON
using CSV
using DataFrames
#using GhpGhx
#using Xpress
using HiGHS
using JuMP
using REopt

dir = @__DIR__
results_path = joinpath(dir, "results", "results_json")
posts_path = joinpath(dir, "data", "inputs_all")
data_path = joinpath(dir, "data")

## Process buildings inputs:
# Read site's info
site_info = CSV.read(joinpath(dir, "data", "dist_sys_data.csv"), DataFrame)
building_list = site_info[:,"Site"]

for item in building_list
    building_data_path = joinpath(data_path, "buildings", item)

    # Create individual building input post
    post = Dict()
    post["Site"] = Dict()
    post["Site"]["latitude"] = site_info[site_info.Site .== item, :].latitude[1]
    post["Site"]["longitude"] = site_info[site_info.Site .== item, :].longitude[1]

    # Read individual building's electric and heating load
    electric_load = CSV.read(joinpath(building_data_path, "electric_load.csv"), DataFrame, header=false)
    electric_load_v = vec(Array(electric_load))

    heating_load = CSV.read(joinpath(building_data_path, "heating_load.csv"), DataFrame, header=false)
    heating_load_v = vec(Array(heating_load))

    post["SpaceHeatingLoad"] = Dict()
    post["DomesticHotWaterLoad"] = Dict()
    post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = heating_load_v
    post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = heating_load_v*0

    post["ElectricLoad"] = Dict()
    post["ElectricLoad"]["loads_kw"] = electric_load_v

    # Read individual building's utility tariff
    tarrif_file = "utility_rates.json"
    post["ElectricTariff"] = Dict()
    post["ElectricTariff"]["urdb_response"] = JSON.parsefile("$building_data_path/$tarrif_file")

    # Read GHP output from URBANopt
    ghpghx_file = "ghpghx_response.json"
    ghpghx_output1 = JSON.parsefile("$building_data_path/$ghpghx_file")
    ghpghx_output2 = JSON.parsefile("$building_data_path/$ghpghx_file")
    ghpghx_output = [ghpghx_output1, ghpghx_output1]

    post["GHP"] = Dict()
    post["GHP"]["ghpghx_responses"] = ghpghx_output

    # Read in building's building_sqft
    post["GHP"]["building_sqft"] = site_info[site_info.Site .== item, :].GHP_building_sqft[1]

    # Reading existing boiler (back up system)
    post["ExistingBoiler"] = Dict()
    post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = site_info[site_info.Site .== item, :].ExistingBoiler_fuel_cost_per_mmbtu[1]

    # Write individual building post to inputs_all directory
    write(joinpath(posts_path, "GHP_"*item*".json"), JSON.json(post))

end

## Run REopt
for file in readdir(posts_path) 
        print("\n",file)
    if file == ".DS_Store"
        continue
    else
        post = JSON.parsefile("$posts_path/$file")
    end
    #m1 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))
    #m2 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))

    m1 = Model(optimizer_with_attributes(HiGHS.Optimizer))
    m2 = Model(optimizer_with_attributes(HiGHS.Optimizer))

    r = run_reopt([m1,m2], REoptInputs(Scenario(post)))
    mkpath(results_path)
    write(joinpath(results_path, file), JSON.json(r))
    #end
end