---
bibliography: 'references.bib'
nocite: '@*'
...


# MicroTomoRegistration

In this project we propose to solve the registration of 3D triangular models onto 2D X-ray projections [@Wen2019CGVC].
Our approach relies extensively on global optimisation methods and fast X-ray simulation on GPU.
We demonstrate the validity of our approach on:

Automatic estimation of the position and rigid transformation of geometric shapes (cube and cylinders) to match an actual metallic sample made of Ti/SiC fibre composite with tungsten (W) cores. We minimise the discrepancies between the data obtained during an actual micro-tomography acquisition and simulated data.
We rely on [gVirtualXRay](https://sourceforge.net/projects/gvirtualxray/), the opensource library for X-ray simulation from polygon meshes [@Vidal2016ComputMedImagingGraph], and on [opensource implementations of optimisation algorithms](https://github.com/Shatha1978/Optimisation-algorithm-examples).

<div id="fig:coolFig">
![caption a](sample_exposure.png){#fig:cfa width=30%}
![caption b](sample_exposure.png){#fig:cfb width=60%}
![caption c](sample_exposure.png){#fig:cfc width=10%}

![caption d](sample_exposure.png){#fig:cfd}
![caption e](sample_exposure.png){#fig:cfe}
![caption f](sample_exposure.png){#fig:cff}

Cool figure!
</div>




To evaluate our pipeline, each optimisation is repeated 15 times to gather statistically meaningful results, in particular to assess the reproducibility of the outputs. Our registration framework is successful for this both test-cases when using a suitable optimisation algorithm.

A YouTube video is also available [@Vidal2018IBFEM-4i].

[![YouTube video of presentation given at IBFEM-4i (Sept 2018)](http://img.youtube.com/vi/Jo1RMb2hKPE/0.jpg)](http://www.youtube.com/watch?v=Jo1RMb2hKPE)


# References
