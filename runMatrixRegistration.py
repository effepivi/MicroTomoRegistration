#!/usr/bin/env python3

import Comparison

from CubeObjectiveFunction import *
from XRayEnvironment import *

# Stopping criteria
max_iterations = 250;

# Instantiate the objective function
test_problem = CubeObjectiveFunction();

# Number of runs
number_of_runs = 15;

def callback(optimiser, file_prefix, run_id):
    test_problem.setExtraParameters(optimiser.short_name, run_id);

initEnvironment();

Comparison.run(test_problem=test_problem, max_iterations=max_iterations, number_of_runs=number_of_runs, file_prefix="matrix_registration_", visualisation=False, aPreCallback=callback);
