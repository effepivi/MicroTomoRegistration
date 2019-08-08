---
bibliography: 'references.bib'
nocite: '@*'
...


[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4ee04d4ded56412c9b01988a08d6a498)](https://app.codacy.com/app/effepivi/MicroTomoRegistration?utm_source=github.com&utm_medium=referral&utm_content=effepivi/MicroTomoRegistration&utm_campaign=Badge_Grade_Dashboard)


# Registration of Polygon Meshes onto X-ray Projections: Application to 3D Micro-Tomography by Synchrotron Radiation


## Project Description
======================

In this project we propose to solve the registration of 3D triangular models onto 2D X-ray projections [@Wen2019CGVC].
Our approach relies extensively on global optimisation methods and fast X-ray simulation on GPU (see Figure [1](#fig:overview)).
We demonstrate the validity of our approach on the automatic estimation of the position and rigid transformation of geometric shapes (cube and cylinders) to match an actual metallic sample made of Ti/SiC fibre composite with tungsten (W) cores (see Figure [2(a)](#fig:sample_exposure)).
An experiment was conducted at [ESRF](https://www.esrf.eu) to perform a micro-tomography of the sample (see Figure [2(b)](#fig:CT_ref_annotated)).
We minimise the discrepancies between the image obtained during the data acquisition (see Figure [2(c)](#fig:sinogram)) and simulated data.
We rely on [gVirtualXRay](https://sourceforge.net/projects/gvirtualxray/), the opensource library for X-ray simulation from polygon meshes [@Vidal2016ComputMedImagingGraph], and on [opensource implementations of optimisation algorithms](https://github.com/Shatha1978/Optimisation-algorithm-examples).

![Registration pipeline based on X-ray simulation and black-box optimisation techniques](overview.png){#fig:overview}

<div id="fig:figureRef" class="subfigures">
![Scanned object (the Euro coin is used to illustrate the relatively small size of the object)](sample_exposure.png){#fig:sample_exposure width=30%}
![Reference (801 x 801 region of interest from a 1217 x 1217 CT slice)](CT_ref_annotated.png){#fig:CT_ref_annotated width=30%}
![Sinogram of Figure 1b](sinogram_ref.jpg){#fig:sinogram_ref width=30%}


CT slice of a Ti/SiC fibre composite with tungsten cores. Experiment was carried out at [ESRF](https://www.esrf.eu) using synchrotron radiation
</div>

To evaluate our pipeline, each optimisation is repeated 15 times to gather statistically meaningful results, in particular to assess the reproducibility of the outputs. Our registration framework is successful for this both test-cases when using a suitable optimisation algorithm.


## YouTube Videos
=================

A YouTube video of the presentation given at IBFEM-4i (Sept
2018) is available below [@Vidal2018IBFEM-4i].

[![YouTube video of presentation given at IBFEM-4i (Sept
2018)](http://img.youtube.com/vi/Jo1RMb2hKPE/0.jpg)](http://www.youtube.com/watch?v=Jo1RMb2hKPE)


## References
=============
