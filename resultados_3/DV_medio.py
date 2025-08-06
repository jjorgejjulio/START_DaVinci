import Functors as F
import FunTuple.functorcollections as FC
from DaVinci import Options, make_config
from DaVinci.algorithms import create_lines_filter
from FunTuple import FunctorCollection
from FunTuple import FunTuple_Particles as Funtuple
from PyConf.reading import get_particles, get_pvs
from RecoConf.event_filters import require_pvs


def main(options: Options):
    line = "Hlt2B2OC_BdToDsmPi_DsmToKpKmPim"
    data = get_particles(f"/Event/HLT2/{line}/Particles")
    line_prefilter = create_lines_filter(name=f"PreFilter_{line}", lines=[line])
    pvs = get_pvs()

    fields = {
        "Bs": "[B0 -> (D_s- -> K- K+ pi-) pi+]CC",
        "Ds": "[B0 -> ^(D_s- -> K- K+ pi-) pi+]CC",
        "Bs_pi": "[B0 -> (D_s- -> K- K+ pi-) ^pi+]CC",
        "Ds_pi": "[B0 -> (D_s- -> K- K+ ^pi-) pi+]CC",
        "Km": "[B0 -> (D_s- -> ^K- K+ pi-) pi+]CC",
        "Kp": "[B0 -> (D_s- -> K- ^K+ pi-) pi+]CC",
    }

    all_vars = FunctorCollection({
        "M": F.MASS,
        "P": F.P,
        "PT": F.PT,
        "ENERGY": F.ENERGY,
        "PX": F.PX,
        "PY": F.PY,
        "PZ": F.PZ,
        "ID": F.PARTICLE_ID,            # PDG ID of the particle
        "Q": F.CHARGE,                  # Electric charge
        "ETA": F.ETA,                   # Pseudorapidity
        "PHI": F.PHI,                   # Azimuthal angle
        "CHI2": F.CHI2,                 # χ²
        "CHI2DOF": F.CHI2DOF,           # χ² of degrees of freedom
        "OWNPVIP": F.OWNPVIP,           # Impact parameter wrt own PV
        "OWNPVIPCHI2": F.OWNPVIPCHI2,   # Impact parameter χ² wrt own PV

    })

    base_composite_variables = FunctorCollection({
        "VTXCHI2NDOF": F.CHI2DOF,         # Vertex fit χ²/ndf
        "END_VX": F.END_VX,               # x-coordinate of decay vertex
        "END_VY": F.END_VY,               # y-coordinate of decay vertex
        "END_VZ": F.END_VZ,               # z-coordinate of decay vertex
        # OWNPV values
        "OWNPV_X": F.OWNPVX,              # x-coordinate of best PV
        "OWNPV_Y": F.OWNPVY,              # y-coordinate of best PV
        "OWNPV_Z": F.OWNPVZ,              # z-coordinate of best PV
        "OWNPV_DIRA": F.OWNPVDIRA,        # Direction angle cosine wrt own PV
        "OWNPV_FD": F.OWNPVFD,            # Flight distance wrt own PV
        "OWNPV_FDCHI2": F.OWNPVFDCHI2,    # Flight distance χ² wrt own PV
        "OWNPV_VDRHO": F.OWNPVVDRHO,      # Radial flight distance wrt own PV
        "OWNPV_VDZ": F.OWNPVVDZ,          # z-direction flight distance
        "OWNPV_LTIME": F.OWNPVLTIME,      # Proper lifetime
        "OWNPV_DLS": F.OWNPVDLS,          # Decay length significance
        # DOCA
        "DOCA12": F.DOCA(1, 2),           # DOCA between first and second daughter
        "DOCA12CHI2": F.DOCACHI2(1, 2),   # DOCA χ² between first and second daughter
        # Daughter Max, Min and Sums
        "MAX_PT": F.MAX(F.PT),            # Maximum PT of daughters
        "MIN_PT": F.MIN(F.PT),            # Minimum PT of daughters
        "SUM_PT": F.SUM(F.PT),            # Sum of daughters' PT
        "MAX_P": F.MAX(F.P),              # Maximum momentum of daughters
        "MIN_P": F.MIN(F.P),              # Minimum momentum of daughters
        "SUM_P": F.SUM(F.P),              # Sum of daughters' momentum
        "MAX_OWNPVIPCHI2": F.MAX(F.OWNPVIPCHI2),  # Max IP χ² of daughters
        "MIN_OWNPVIPCHI2": F.MIN(F.OWNPVIPCHI2),  # Min IP χ² of daughters
        "SUM_OWNPVIPCHI2": F.SUM(F.OWNPVIPCHI2),  # Sum of daughters' IP χ²
        "MAXDOCACHI2": F.MAXDOCACHI2,      # Maximum DOCA χ² between any daughters
        "MAXDOCA": F.MAXDOCA,              # Maximum DOCA between any daughters
        "MAXSDOCACHI2": F.MAXSDOCACHI2,    # Maximum signed DOCA χ²
        "MAXSDOCA": F.MAXSDOCA,            # Maximum signed DOCA

    })

    # Need extra DOCA combinations since Ds decays to 3 final state particles
    Ds_extra_doca = FunctorCollection({
        "DOCA13": F.DOCA(1, 3),
        "DOCA23": F.DOCA(2, 3),
        "DOCA13CHI2": F.DOCACHI2(1, 3),
        "DOCA23CHI2": F.DOCACHI2(2, 3),
    })

    track_variables = FunctorCollection({
        # Standard PID
        "PIDp": F.PID_P,              # Proton PID likelihood
        "PIDK": F.PID_K,              # Kaon PID likelihood
        "PIDPi": F.PID_PI,            # Pion PID likelihood
        "PIDe": F.PID_E,              # Electron PID likelihood
        "PIDmu": F.PID_MU,            # Muon PID likelihood
        # PROBNNs
        "PROBNN_pi": F.PROBNN_PI,        # Neural net probability of being a pion
        "PROBNN_p": F.PROBNN_P,          # Neural net probability of being a proton
        "PROBNN_K": F.PROBNN_K,          # Neural net probability of being a kaon
        "PROBNN_e": F.PROBNN_E,          # Neural net probability of being an electron
        "PROBNN_mu": F.PROBNN_MU,        # Neural net probability of being a muon
        "PROBNN_GHOST": F.PROBNN_GHOST,  # Neural net probability of being a ghost track
        "ISMUON": F.ISMUON,              # Boolean: is it identified as a muon 0 or 1?
        # Additional track related info
        # F.TRACK gets the track object
        # F.NDOF gets the NDOF for that track
        # F.VALUE_OR(-1) means if no value exists return -1 instead of failing
        "TRNDOF": F.VALUE_OR(-1) @ F.NDOF @ F.TRACK,                # NDOF in track fit, if this is higher then more hits used in fit
        "NHITS": F.VALUE_OR(-1) @ F.NHITS @ F.TRACK,                # Total number of hits in all detectors
        "NVPHITS": F.VALUE_OR(-1) @ F.NVPHITS @ F.TRACK,            # Total number of hits in VELO phi sensors
        "NUTHITS": F.VALUE_OR(-1) @ F.NUTHITS @ F.TRACK,            # Total number of hits in UT
        "NFTHITS": F.VALUE_OR(-1) @ F.NFTHITS @ F.TRACK,            # Total number of hits in Fibre Tracker (SciFi)
        "TRACKHISTORY": F.VALUE_OR(-1) @ F.TRACKHISTORY @ F.TRACK,  # Track reconstruction history
    })

    variables = {
        "ALL": all_vars,                                    # Variables for all particles
        "Bs": base_composite_variables,                     # Variables specific to Bs
        "Ds": base_composite_variables + Ds_extra_doca,     # Variables specific to Ds 
        "Bs_pi": track_variables,                           # Variables for pion
        "Ds_pi": track_variables,                           # Variables for pion 
        "Kp":    track_variables,                           # Variables for kaon 
        "Km":    track_variables,                           # Variables for kaon 
    }

    funtuple = Funtuple(
        name=line,
        tuple_name="DecayTree",
        fields=fields,
        variables=variables,
        inputs=data,
    )

    algs = {line: [line_prefilter, require_pvs(pvs), funtuple]}
    return make_config(options, algs)
