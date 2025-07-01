#!/bin/bash

#SBATCH -J TTP_n8
#SBATCH -t 5-00:00:00

#SBATCH -p rome
#SBATCH -N 6
#SBATCH --ntasks-per-node 128

#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=basloyen@gmail.com
#SBATCH --output=n8.out
#SBATCH --error=n8.err

# Load the necessary modules
module load 2024
module load OpenMPI/5.0.3-GCC-13.3.0

make

APP=./run
ARGS="8 5"
OMPI_OPTS="--mca btl ^usnic"

# OpenHPC openmpi modules do not set MPI_RUN, so:
MPI_RUN=mpirun

$MPI_RUN $OMPI_OPTS $APP $ARGS