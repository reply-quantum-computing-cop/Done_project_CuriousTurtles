# QHack 2023 - Open Hackaton

## Problem description

In this repository we set out to calculate the the ground state energy of the $BeH_2$ molecule as accurately as 
possible using a hybrid quantum-classical algorithm.

With the presently available Near-term Intermediate-Scale Quantum (NISQ) hardware, some of the most common approaches 
to such problems are the so-called Variational Quantum Eigensolvers (VQE). The key component is the choice of an 
ansatz (UCCSD, Givens rotations, etc.), with certain approximations, for example:

* Frozen core
* Simple orbital basis set (sto-3G), which should be increased for more accurate results

The goal of these approximations is to reduce the qubit cost. This can also be adressed by tapering the Hamiltonian 
operator to reduce the search space by making use of any symmetries to a particular molecule. The ground state can 
then be searched for in a certain symmetry sector.

However, VQE methods are prone to so-called Barren plateaus, which seriously hinder finding the optimum. In addition, 
the classical optimisation task is often facing high dimensional non-convex playgrounds, which complicate the problem 
further. The result is also sensitive to the ansatz being used, which often needs to have many layers in order to 
be expressive enough. On present-day NISQ devices the latter presents a variety of different challenges on its own.

Due to the issues outlined above people have been searching for alternative methods for finding the ground state
energy of molecules, which would lead to better answers. In this repository, we follow the Iterative Quantum Assisted 
Eigensolver (IQAE) approach described by Bharti and Haug 
[https://arxiv.org/pdf/2010.05638.pdf](https://arxiv.org/pdf/2010.05638.pdf). The IQAE algorithm builds the ansatz as 
a linear combination of Krylov subspace basis. Based on that it computes overlap matrices on quantum hardware. The
overlap matrices then form an optimization program to be minimized. The resulting optimization problem is then a 
quadratically constrained quadratic program (QCQP) which is a class of problems that has been well-studied 
classically. The IQAE has been found to be sensitive to its input state. Thus, we use a VQE method with a 
straightforward ansatz to come to a first estimation of the ground state and then feed the result to the IQAE 
algorithm.

