
import pytest
import os

import metawards as mw

from pygsl import rng as gsl_rng

script_dir = os.path.dirname(__file__)
ncovparams_csv = os.path.join(script_dir, "data", "ncovparams.csv")


def test_integration():
    """This test repeats main_RepeatsNcov.c and validates that the
       various stages report the same results as the original C code
    """
    seed = 15324

    inputfile = ncovparams_csv

    line_num = 0

    UV = 1.0

    rng = gsl_rng.rng()

    rng.set(seed)

    params = mw.Parameters.create("ncov")

    params.read_file(inputfile, line_num)

    params.UV = UV

    params.set_input_files(4)

    to_seed = mw.read_done_file(params.input_files.seed)

    nseeds = len(to_seed)

    print(to_seed)
    print(f"Number of seeds equals {nseeds}")

    print("Building the network...")
    network = mw.build_wards_network_distance(params)
    print("Network built!")

    infections = mw.initialise_infections(network=network, params=params)

    play_infections = mw.initialise_play_infections(network=network,
                                                    params=params)

    (mindist, maxdist) = mw.get_min_max_distances(network)

    params.dyn_dist_cutoff = maxdist + 1

    s = -1

    params.static_play_at_home = 0

    mw.reset_everything(network=network, params=params)

    mw.rescale_play_matrix(network=network, params=params)

    params.play_to_work = 0
    params.work_to_play = 0

    # TOMORROW - WRITE THIS BELOW FUNCTION
    #mw.move_population_from_play_to_work(network=network, params=params,
    #                                     rng=rng)

if __name__ == "__main__":
    test_integration()