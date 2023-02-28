# QHack 2023 - Open Hackaton

## Problem description

This repository attempts to calculate the ground state energy of the $BeH_2$ molecule using quantum computing algorithms, in the most accurate way.

VQE is the natural approach for solving such problems. The key component is the choice of an ansatz (UCCSD, Givens rotations,...), with certain approximations. Typical approximations are

* Frozen core (orbital removal)
* Simple orbital basis set (sto-3G), which should be increased for more accurate results

The goal of these approximations is to reduce the qubit cost. The latter can be adressed by tapering the Hamiltonian operator to reduce the search of the ground state in a certain symetry sector.

Nonetheless VQE methods are sensitive to Barren plateaus. In addition the classical optimisation task is often facing high dimensional non-convex playgrounds, which complexify the problem. The ansatz often used are also quite deep and lead to issues on NISQ devices.

All in all, alternative methods can lead to better answers. This repository will explore the following results from Bharti, K., & Haug, T. (n.d.).  *Iterative Quantum Assisted Eigensolver* . [https://arxiv.org/pdf/2010.05638.pdf](https://arxiv.org/pdf/2010.05638.pdf)

## Project description

The project is described as follow:

* IQAE_Krylov.ipynb : Main notebook containing VQE and IQAE algorithm
* IQAE_toolbox.py : contains toolbox functions for the main notebook
