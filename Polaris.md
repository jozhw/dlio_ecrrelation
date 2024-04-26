
## Interactive Mode on Polaris 

`qsub -A DLIO -l select=2 -q debug -l walltime=1:00:00 -l filesystems=home:eagle`

```
module use /soft/modulefiles

module load conda ; conda activate base

cd dlio_ecrrelation

mpiexec -n 128 --ppn 64 python src/generate_results_polaris.py

```
