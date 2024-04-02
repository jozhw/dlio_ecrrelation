
## Interactive Mode on Polaris 

`qsub -A DLIO -l select=1 -q debug -l walltime=0:50:00 -l filesystems=home:eagle`

```
module load conda ; conda activate base

cd dlio_ecrrelation

mpirun -np 64 python src/generate_results_polaris.py

```
