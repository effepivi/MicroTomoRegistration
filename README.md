MicroTomoRegistration
=====================

In this project we propose to solve the registration of 3D triangular
models onto 2D X-ray projections (Wen et al. 2019). Our approach relies
extensively on global optimisation methods and fast X-ray simulation on
GPU. We demonstrate the validity of our approach on:

Automatic estimation of the position and rigid transformation of
geometric shapes (cube and cylinders) to match an actual metallic sample
made of Ti/SiC fibre composite with tungsten (W) cores. We minimise the
discrepancies between the data obtained during an actual
micro-tomography acquisition and simulated data. We rely on
[gVirtualXRay](https://sourceforge.net/projects/gvirtualxray/), the
opensource library for X-ray simulation from polygon meshes (**F. P.
Vidal** and Villard 2016), and on [opensource implementations of
optimisation
algorithms](https://github.com/Shatha1978/Optimisation-algorithm-examples).

To evaluate our pipeline, each optimisation is repeated 15 times to
gather statistically meaningful results, in particular to assess the
reproducibility of the outputs. Our registration framework is successful
for this both test-cases when using a suitable optimisation algorithm.

A YouTube video is also available (**F. P. Vidal** 2018). [![YouTube
video of presentation given at IBFEM-4i (Sept
2018)](http://img.youtube.com/vi/Jo1RMb2hKPE/0.jpg)](http://www.youtube.com/watch?v=Jo1RMb2hKPE)

References
==========

**F. P. Vidal**. 2018. “gVirtualXRay – Fast X-ray Simulation on GPU.” In
*Workshop on Image-Based Finite Element Method for Industry 2018
(Ibfem-4i 2018)*. Swansea, UK.
doi:[10.5281/zenodo.1452506](https://doi.org/10.5281/zenodo.1452506).

**F. P. Vidal**, and Pierre-Frédéric Villard. 2016. “Development and
Validation of Real-Time Simulation of X-Ray Imaging with Respiratory
Motion.” *Computerized Medical Imaging and Graphics* 49 (April).
Elsevier: 1–15.
doi:[10.1016/j.compmedimag.2015.12.002](https://doi.org/10.1016/j.compmedimag.2015.12.002).

Wen, T., R. P. Mihail, S. Al-Maliki, J.-M. Létang, and **F. P. Vidal**.
2019. “Registration of 3d Triangular Models to 2d X-ray Projections
Using Black-Box Optimisation and X-ray Simulation.” In *Computer
Graphics and Visual Computing (Cgvc)*, edited by G. K. L. Tam and J. C.
Roberts. The Eurographics Association.
