# Molecular Dynamics with [NeQUIP](https://github.com/mir-group/nequip)
#=========================================================================

This tutorial introduces a Machine Learning Interatomic Potential (MLP) model called NequIP.

This particular tutorial is for the 22-water molecules in a 40 Å³ periodic box. The steps to build the MLP contain three stages:

    1. Data generation
    2. Training
    3. Molecular Dynamics

For data generation, we will use the [Quantum Espresso](https://www.quantum-espresso.org/) package.

Here, I am not going to explain how to generate the initial configuration. However, there are several ways to do that. The easiest way is to perform a classical MD simulation and then take the (M) random configurations and do the ab-initio calculations to get the potential energy and corresponding forces (in this case, we will be using Quantum Espresso).

The initial 500 configurations (input and output) are stored in the **QE_In_File** and **QE_Out_File** folders inside the 00.data directory. (You can re-run the inputs if you want).

The underlying concept and details are given in this article [https://www.nature.com/articles/s41467-022-29939-5].
