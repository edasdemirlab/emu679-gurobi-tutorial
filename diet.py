import gurobipy as gp
from gurobipy import GRB

# Create a new Gurobi model
model = gp.Model("WeeklyMealPlan")

# Define the data (cost, nutritional values, etc.)
n_items = 14
days = 5  # Monday to Friday
costs = [0.59, 1.79, 1.65, 0.68, 1.56, 2.69, 1.96, 1.36, 1.09, 0.63, 0.56, 0.88, 0.68, 0.68]
calories = [255, 320, 500, 220, 270, 170, 50, 280, 90, 105, 110, 80, 80, 90]
protein = [12, 22, 25, 3, 20, 17, 4, 18, 2, 4, 9, 1, 1, 0]
calcium = [10, 15, 25, 0, 0, 15, 4, 25, 2, 10, 30, 0, 0, 0]
iron = [15, 20, 20, 2, 6, 8, 8, 15, 20, 0, 0, 0, 0, 4]
vitamin_a = [4/10, 10/10, 6/10, 0, 0, 100/10, 90/10, 10/10, 20/10, 2/10, 10/10, 0, 0, 0]
b1 = [0.2, 0.25, 0.3, 0.1, 0.08, 0.2, 0.06, 0.3, 0.2, 0.02, 0.08, 0.1, 0.04, 0.02]
b2 = [0.1, 0.2, 0.25, 0.0, 0.08, 0.15, 0.06, 0.2, 0.2, 0.1, 0.3, 0.0, 0.02, 0.0]
fat = [9, 10, 26, 12, 15, 9, 2, 11, 1, 1, 2, 0, 0, 0]


# =============================================================================
# (7.74*18 + 6.88*9)/
# 
# ((7.74*280 + 6.88*110))/20
# =============================================================================

# Define minimum requirements (half of daily recommended intake)
calorie_min = 3000/2
protein_min = 70/2
calcium_min = 1/2
iron_min = 12/2
vitamin_a_min = 3/2
b1_min = 1.8/2
b2_min = 2.7/2
fat_to_calorie_ratio = 1 / 20
min_calorie_density = 200

# Create decision variables for food items
x = model.addVars(n_items, days, vtype=GRB.CONTINUOUS, name="x")

# Set the objective function (minimize cost)
model.setObjective(gp.quicksum(costs[i] * x[i, j] for i in range(n_items) for j in range(days)), GRB.MINIMIZE)

# 1 Add nutritional requirements as constraints for each day
for j in range(days):
    model.addConstr(gp.quicksum(calories[i] * x[i, j] for i in range(n_items)) >= calorie_min, f"CalorieMin_Day{j}")
    model.addConstr(gp.quicksum(protein[i] * x[i, j] for i in range(n_items)) >= protein_min, f"ProteinMin_Day{j}")
    model.addConstr(gp.quicksum(calcium[i] * x[i, j] for i in range(n_items)) >= calcium_min, f"CalciumMin_Day{j}")
    model.addConstr(gp.quicksum(iron[i] * x[i, j] for i in range(n_items)) >= iron_min, f"IronMin_Day{j}")
    model.addConstr(gp.quicksum(vitamin_a[i] * x[i, j] for i in range(n_items)) >= vitamin_a_min, f"VitaminAMin_Day{j}")
    model.addConstr(gp.quicksum(b1[i] * x[i, j] for i in range(n_items)) >= b1_min, f"B1Min_Day{j}")
    model.addConstr(gp.quicksum(b2[i] * x[i, j] for i in range(n_items)) >= b2_min, f"B2Min_Day{j}")

# 2 Add fat-to-calorie ratio constraint (for each day)
for j in range(days):
    model.addConstr(gp.quicksum(fat[i] * x[i, j] for i in range(n_items)) <= fat_to_calorie_ratio * gp.quicksum(calories[i] * x[i, j] for i in range(n_items)), f"FatToCalorie_Day{j}")



# =============================================================================
# # 4 Add weekly total servings limit (at most 15 servings per item over the entire week)
# for i in range(days):
#     model.addConstr(gp.quicksum(x[i, j] for i in range(n_items)) <= 5, f"Daily_Servings_Item{i}")
# 
# =============================================================================


# 4 Add weekly total servings limit (at most 15 servings per item over the entire week)
for i in range(n_items):
    model.addConstr(gp.quicksum(x[i, j] for j in range(days)) <= 5, f"TotalServings_Item{i}")

# 5 Add calorie density constraint (for each day)
for j in range(days):
    model.addConstr(gp.quicksum(calories[i] * x[i, j] for i in range(n_items)) >= min_calorie_density * gp.quicksum(x[i, j] for i in range(n_items)), f"CalorieDensity_Day{j}")

# 6 Add special protein-to-calorie ratio constraint for Wednesday (day 3)
model.addConstr(gp.quicksum(protein[i] * x[i, 2] for i in range(n_items)) >= (1 / 20) * gp.quicksum(calories[i] * x[i, 2] for i in range(n_items)), "ProteinToCalorie_Wednesday")

# Optimize the model
model.optimize()
# model.write('iismodel.ilp')


# Print the results
if model.status == GRB.OPTIMAL:
    print("\nOptimal solution found:")
    for j in range(days):
        print(f"Day {j+1}:")
        for i in range(n_items):
            if x[i, j].X > 0:
                print(f"  Food item {i+1}: {x[i, j].X} servings")
    print(f"Total cost: ${model.ObjVal}")
else:
    print("No optimal solution found.")
