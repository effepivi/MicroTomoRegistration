# MicroTomoRegistration

In this project we propose to solve the registration of 3D triangular models onto 2D X-ray projections.
Our approach relies extensively on global optimisation methods and fast X-ray simulation on GPU.
We demonstrate the validity of our approach on:

Automatic estimation of the position and rigid transformation of geometric shapes (cube and cylinders) to match an actual metallic sample made of Ti/SiC fibre composite with tungsten (W) cores. We minimise the discrepancies between the data obtained during an actual micro-tomography acquisition and simulated data.
We rely on [gVirtualXRay](https://sourceforge.net/projects/gvirtualxray/), the opensource library for X-ray simulation from polygon meshes, and on [opensource implementations of optimisation algorithms](https://github.com/Shatha1978/Optimisation-algorithm-examples).

To evaluate our pipeline, each optimisation is repeated 15 times to gather statistically meaningful results, in particular to assess the reproducibility of the outputs. Our registration framework is successful for this both test-cases when using a suitable optimisation algorithm.

[![YouTube video of presentation given at IBFEM-4i (Sept 2018)](http://img.youtube.com/vi/Jo1RMb2hKPE/0.jpg)](http://www.youtube.com/watch?v=Jo1RMb2hKPE)


<a href="http://www.youtube.com/watch?feature=player_embedded&v=Jo1RMb2hKPE"
    target="_blank"><img src="http://img.youtube.com/vi/Jo1RMb2hKPE/0.jpg"
alt="YouTube video of presentation given at IBFEM-4i (Sept 2018)" width="240" height="180" border="10" /></a>
