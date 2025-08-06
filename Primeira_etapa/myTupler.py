from DaVinci import Options, make_config
from DaVinci.algorithms import create_lines_filter
from PyConf.Algorithms import PrintDecayTree
from PyConf.reading import get_particles

def printDecayTree(options: Options):
    # The name of the line we want to look at
    line = "Hlt2B2OC_BdToDsmPi_DsmToKpKmPim"
    input_data = get_particles(f"/Event/HLT2/{line}/Particles")

    # Add a filter: We are not really filtering over particles
    # If the event hasn't fired a HLT2 line then the corresponding TES location does
    # obviously not exist and therefore if any algorithm tries to look for this location,
    # it will of course fail.
    # Resolve this with a filter, where:
    # - 1st argument is a user defined name.
    # - 2nd argument is the line decision (inspect hlt2_starterkit.tck.json if needed))
    my_filter = create_lines_filter("HDRFilter_SeeNoEvil", lines=[f"{line}"])

    # Defining an algorithm. The algorithm here prints the decaytree
    pdt = PrintDecayTree(name="PrintBsToDsPi", Input=input_data)

    user_algorithms = [my_filter, pdt]

    return make_config(options, user_algorithms)
