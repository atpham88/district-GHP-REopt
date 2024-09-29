using Pkg
using JSON
using CSV
using DataFrames
using GhpGhx
using Xpress
using JuMP
using REopt

dir = @__DIR__
results_path = joinpath(dir, "results", "results_json")
posts_path = joinpath(dir, "data")
file = "ghp_test.json"
tarrif_file = "utility_rates.json"
ghpghx_file = "GHP_input.json"
ghpghx_input_v = JSON.parsefile("$posts_path/$ghpghx_file")

inputs_dict = JSON.parsefile("$posts_path/$file")

electric_load = CSV.read(joinpath(dir, "data", "electric_load.csv"), DataFrame, header=false)
heating_load = CSV.read(joinpath(dir, "data", "heating_load.csv"), DataFrame, header=false)
electric_load_v = vec(Array(electric_load))
heating_load_v = vec(Array(heating_load))

# Run REopt:
# Prepare input
post = Dict()
post["Site"] = Dict()
post["Site"]["latitude"] = 39.991532318981605
post["Site"]["longitude"] = -105.2648427364457

post["SpaceHeatingLoad"] = Dict()
post["DomesticHotWaterLoad"] = Dict()
post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = heating_load_v
post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = heating_load_v*0

post["ElectricLoad"] = Dict()
post["ElectricLoad"]["loads_kw"] = electric_load_v

# GHP:
post["GHP"] = Dict()
post["GHP"]["building_sqft"] = 10000.0

# GHPGHX respinse
#post["GHP"]["ghpghx_responses"] = ghpghx_input_v

# Existing Boiler:
post["ExistingBoiler"] = Dict()
post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = 37.0

# Electric Tariff:
post["ElectricTariff"] = Dict()
post["ElectricTariff"]["urdb_response"] = JSON.parsefile("$posts_path/$tarrif_file")

write(joinpath(posts_path, "GHP_inputs.json"), JSON.json(post))

post_REopt = REoptInputs(Scenario(post))

m1= Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))
m2 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))

r = run_reopt([m1,m2], post_REopt)
write(joinpath(results_path, "GHP_results.json"), JSON.json(r))






