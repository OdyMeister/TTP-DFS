#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH -N 16
#SBATCH --ntasks-per-node=16

. /etc/bashrc
# OpenHPC uses lmod.sh instead of the older modules.sh:
. /etc/profile.d/lmod.sh
module load openmpi/gcc/64

APP=./run
ARGS="6 4"
OMPI_OPTS="--mca btl ^usnic"

# OpenHPC openmpi modules do not set MPI_RUN, so:
MPI_RUN=mpirun

$MPI_RUN $OMPI_OPTS $APP $ARGS