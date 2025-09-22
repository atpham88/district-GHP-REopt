using Pkg
using Xpress
using JuMP
using REopt
using JSON

dir = @__DIR__
run_path = ARGS[1]
scenario_name = ARGS[2]

results_path = joinpath(run_path, scenario_name, "results", "results_json")          # where to save results
posts_path = joinpath(run_path, scenario_name, "inputs_all")

for file in readdir(posts_path) 
        print("\n",file)
    if file == ".DS_Store"
        continue
    else
        post = JSON.parsefile("$posts_path/$file")
    end
    m = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))
    #m2 = Model(optimizer_with_attributes(Xpress.Optimizer, "OUTPUTLOG" => 0))

    #r = run_reopt([m1,m2], REoptInputs(Scenario(post)))
    r = run_reopt(m, REoptInputs(Scenario(post)))
    write(joinpath(results_path, file), JSON.json(r))
    #end
end