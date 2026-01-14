import numpy as np

class AOMatrixR: 
    """
    Properties:
    ----------
    Rs : np.array((N_R, 3), dtype=int)
        Lattice displacements for inter-cell hoppings.
        The displacements are expressed in terms of the lattice vectors.
        N_R is the number of displacements.
    
    MRs : np.array((N_R, N_b, N_b), dtype=float/complex)
        Overlap matrix in real space. MRs[i, :, :] = S(Rijk_list[i, :]).
        The dtype is float if spinful is false, otherwise the dtype is complex.
    """
    def __init__(self, Rs, MRs):
        self.Rs = Rs
        self.MRs = MRs

    def r2k(self, ks):
        # ks: (Nk, 3), Rs: (NR, 3) -> phase: (Nk, NR)
        phase = np.exp(2j * np.pi * np.matmul(ks, self.Rs.T))
        # MRs: (NR, Nb, Nb) -> flat: (NR, Nb*Nb)
        MRs_flat = self.MRs.reshape(len(self.Rs), -1)
        # (Nk, NR) @ (NR, Nb*Nb) -> (Nk, Nb*Nb)
        Mks_flat = np.matmul(phase, MRs_flat)
        return Mks_flat.reshape(len(ks), *self.MRs.shape[1:])


class AOMatrixK:
    """
    Properties:
    ----------
    ks : np.array((N_k, 3), dtype=float)
        Reciprocal lattice points for the Fourier transform.
        N_k is the number of points.
    
    MKs : np.array((N_k, N_b, N_b), dtype=float/complex)
        Overlap matrix in reciprocal space. MKs[i, :, :] = S(ks[i, :]).
        The dtype is float if spinful is false, otherwise the dtype is complex.
    """
    def __init__(self, ks, MKs):
        self.ks = ks
        self.MKs = MKs  
    
    def k2r(self, Rs, weights=None):
        # weights: (Nk,)
        if weights is None:
            weights = np.ones(len(self.ks)) / len(self.ks)
        else:
            weights = np.array(weights)
        # Rs: (NR, 3), ks: (Nk, 3) -> phase: (NR, Nk)
        phase = np.exp(-2j * np.pi * np.matmul(Rs, self.ks.T))
        # MKs: (Nk, Nb, Nb) -> flat: (Nk, Nb*Nb)
        MKs_flat = self.MKs.reshape(len(self.ks), -1)
        # (NR, Nk) @ (Nk, Nb*Nb) -> (NR, Nb*Nb)
        MRs_flat = np.matmul(phase, MKs_flat * weights[:, None])
        return MRs_flat.reshape(len(Rs), *self.MKs.shape[1:])