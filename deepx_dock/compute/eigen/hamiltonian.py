from pathlib import Path
import h5py
import os
import threadpoolctl

import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
from tqdm import tqdm
from joblib import Parallel, delayed

from deepx_dock.misc import load_json_file, load_poscar_file
from deepx_dock.CONSTANT import DEEPX_POSCAR_FILENAME
from deepx_dock.CONSTANT import DEEPX_INFO_FILENAME
from deepx_dock.CONSTANT import DEEPX_OVERLAP_FILENAME
from deepx_dock.CONSTANT import DEEPX_HAMILTONIAN_FILENAME
from deepx_dock.compute.eigen.matrix import AOMatrixObj

class HamiltonianObj(AOMatrixObj):
    def __init__(self, data_path, H_file_path=None):
        super().__init__(data_path, H_file_path)
        overlap_obj = AOMatrixObj(data_path, matrix_type="overlap")
        self.assert_compatible(overlap_obj)
        self.SR = overlap_obj.mats

    @property
    def HR(self):
        return self.mats

    @staticmethod
    def _r2k(ks, Rijk_list, mats):
        # ks: (Nk, 3), Rs: (NR, 3) -> phase: (Nk, NR)
        phase = np.exp(2j * np.pi * np.matmul(ks, Rijk_list.T))
        # MRs: (NR, Nb, Nb) -> flat: (NR, Nb*Nb)
        MRs_flat = mats.reshape(len(Rijk_list), -1)
        # (Nk, NR) @ (NR, Nb*Nb) -> (Nk, Nb*Nb)
        Mks_flat = np.matmul(phase, MRs_flat)
        return Mks_flat.reshape(len(ks), *mats.shape[1:])

    def Sk_and_Hk(self, k):
        # Support batch k or single k.
        # k: (3,) or (Nk, 3)
        if k.ndim == 1:
            ks = k[None, :]
            squeeze = True
        else:
            ks = k
            squeeze = False
            
        Sk = self._r2k(ks, self.Rijk_list, self.SR)
        Hk = self._r2k(ks, self.Rijk_list, self.HR)
        
        if squeeze:
            return Sk[0], Hk[0]
        return Sk, Hk
        
    def diag(self, ks, k_process_num=1, thread_num=None, sparse_calc=False, bands_only=False, **kwargs):
        """
        Diagonalize the Hamiltonian at specified k-points to obtain eigenvalues (bands) 
        and optionally eigenvectors (wave functions).

        This function supports both dense (scipy.linalg.eigh) and sparse (scipy.sparse.linalg.eigsh) 
        solvers and utilizes parallel computing via joblib.

        Parameters
        ----------
        ks : array_like, shape (Nk, 3)
            List of k-points in reduced coordinates (fractional).
        k_process_num : int, optional
            Number of parallel processes to use (default is 1).
            If > 1, BLAS threads per process are restricted to 1 to avoid oversubscription.
        sparse_calc : bool, optional
            If True, use sparse solver (eigsh). If False, use dense solver (eigh).
            Default is False.
        bands_only : bool, optional
            If True, only compute and return eigenvalues. Faster and uses less memory.
            Default is False.
        **kwargs : dict
            Additional keyword arguments passed to the solver.
            - For sparse_calc=True (eigsh): 'k' (num eigenvalues), 'which' (e.g., 'SA'), 'sigma', etc.
            - For sparse_calc=False (eigh): 'driver', 'type', etc.

        Returns
        -------
        eigvals : np.ndarray
            The eigenvalues (band energies).
            Shape: (Nband, Nk)
        eigvecs : np.ndarray, optional
            The eigenvectors (coefficients). Returned only if bands_only is False.
            Shape: (Norb, Nband, Nk)
        """

        HR = self.HR
        SR = self.SR

        def process_k(k):
            # Hk, Sk: (Norb, Norb)
            # Use vectorized r2k for single k (1, 3) -> (1, Norb, Norb) -> (Norb, Norb)
            Sk = self._r2k(k[None, :], self.Rijk_list, SR)[0]
            Hk = self._r2k(k[None, :], self.Rijk_list, HR)[0]
            
            if sparse_calc:
                if bands_only:
                    # vals: (k,)
                    vals = eigsh(Hk, M=Sk, return_eigenvectors=False, **kwargs)
                    return np.sort(vals)
                else:
                    # vals: (k,), vecs: (Norb, k)
                    vals, vecs = eigsh(Hk, M=Sk, **kwargs)
                    idx = np.argsort(vals)
                    return vals[idx], vecs[:, idx]
            else:
                if bands_only:
                    # vals: (Norb,)
                    vals = eigh(Hk, Sk, eigvals_only=True)
                    return vals 
                else:
                    # vals: (Norb,), vecs: (Norb, Norb)
                    vals, vecs = eigh(Hk, Sk)
                    return vals, vecs

        # Limit BLAS threads per process to prevent CPU contention during parallel execution
        if thread_num is None:
            thread_num = int(os.environ.get('OPENBLAS_NUM_THREADS', "1"))
        with threadpoolctl.threadpool_limits(limits=thread_num, user_api='blas'):
            if k_process_num == 1:
                results = [process_k(k) for k in tqdm(ks, leave=False)]
            else:
                results = Parallel(n_jobs=k_process_num)(
                    delayed(process_k)(k) for k in tqdm(ks, leave=False)
                )

        # Reorganize results into arrays
        if bands_only:
            # results: List of (Nband,) -> Stack -> (Nband, Nk)
            return np.stack(results, axis=1)
        else:
            # results: List of ((Nband,), (Norb, Nband))
            
            # vals: List of (Nband,) -> Stack -> (Nband, Nk)
            eigvals = np.stack([res[0] for res in results], axis=1)
            
            # vecs: List of (Norb, Nband) -> Stack -> (Norb, Nband, Nk)
            eigvecs = np.stack([res[1] for res in results], axis=2)
            
            return eigvals, eigvecs
