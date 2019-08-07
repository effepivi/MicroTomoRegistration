import math
import copy

import numpy as np
from lsf import *

from skimage.transform import radon, iradon, iradon_sart
import scipy.misc

# Import the X-ray simulation library
import gvxrPython3 as gvxr

import ImageMetrics as IM

##### Parameters of the X-ray simulation #####
#detector_width_in_pixels  = math.floor(1024);
#detector_height_in_pixels = math.floor( 615);
detector_width_in_pixels  = 801;
detector_height_in_pixels = 611;
detector_height_in_pixels = 1;

pixel_size_in_micrometer = 1.9;

distance_source_detector_in_m  = 145.0;
distance_object_detector_in_m =    0.08; # = 80 mm

number_of_projections = 900;
number_of_projections = 90;
angular_span_in_degrees = 180.0;

#energy_spectrum_in_keV = [(33, 0.97), (66, 0.02), (99, 0.01)];
energy_spectrum_in_keV = [(33, 1.0)];

angular_step = angular_span_in_degrees / number_of_projections;

theta = np.linspace(0., angular_span_in_degrees, number_of_projections, endpoint=False);

fiber_radius = 140 / 2; # um
fiber_material = [("Si", 0.5), ("C", 0.5)];
fiber_material = "SiC";
fiber_mu = 2.736; # cm-1
fiber_mu = 11; # cm-1
fiber_density = 3.2; # g/cm3

core_radius = 30 / 2; # um
core_material = [("W", 1)];
core_material = "W";
core_mu = 341.61; # cm-1
core_mu = 120; # cm-1
core_density = 19.3 # g/cm3


g_matrix_width = 0;
g_matrix_height = 0;
g_matrix_x = 0;
g_matrix_y = 0;
matrix_material = "Ti90Al6V4";
matrix_mu = 13.1274; # cm-1
matrix_mu = 22; # cm-1
matrix_density = 4.42 # g/cm3

g_reference_CT        = np.zeros(1);
g_reference_sinogram  = np.zeros(1);

g_normalised_reference_CT        = np.zeros(1);
g_normalised_reference_sinogram  = np.zeros(1);

reference_sinogram_entropy = 0.0;
reference_CT_entropy = 0.0;


########################
def initXRaySimulator():
########################

    # Set up the beam
    print("Set up the beam")
    gvxr.setSourcePosition(distance_source_detector_in_m - distance_object_detector_in_m,  0.0, 0.0, "mm");
    gvxr.usePointSource();
    gvxr.useParallelBeam();
    for energy, percentage in energy_spectrum_in_keV:
        gvxr.addEnergyBinToSpectrum(energy, "keV", percentage);

    # Set up the detector
    print("Set up the detector");
    gvxr.setDetectorPosition(-distance_object_detector_in_m, 0.0, 0.0, "m");
    gvxr.setDetectorUpVector(0, 1, 0);
    gvxr.setDetectorNumberOfPixels(detector_width_in_pixels, detector_height_in_pixels);
    gvxr.setDetectorPixelSize(pixel_size_in_micrometer, pixel_size_in_micrometer, "micrometer");

    global angular_step;

    angular_step = angular_span_in_degrees / number_of_projections;

    print("Number of projections: ", str(number_of_projections))
    print("angular_span_in_degrees: ", str(angular_span_in_degrees))
    print("angular_step: ", str(angular_step))


matrix_parameter_set = None;

def setMatrix(apGeneSet):

    global g_matrix_width;
    global g_matrix_height;
    global g_matrix_x;
    global g_matrix_y;
    global matrix_parameter_set;

    matrix_parameter_set = copy.deepcopy(apGeneSet);

    # Matrix
    # Make a cube
    g_matrix_width = apGeneSet[2] * detector_width_in_pixels * pixel_size_in_micrometer / 1.5;
    g_matrix_height = apGeneSet[3] * detector_width_in_pixels * pixel_size_in_micrometer / 1.5;

    g_matrix_x = apGeneSet[0] * detector_width_in_pixels * pixel_size_in_micrometer - detector_width_in_pixels * pixel_size_in_micrometer / 2.0;
    g_matrix_y = apGeneSet[1] * detector_width_in_pixels * pixel_size_in_micrometer - detector_width_in_pixels * pixel_size_in_micrometer / 2.0;


    gvxr.makeCube("Matrix", 1, "micrometer");
    gvxr.setLocalTransformationMatrix("Matrix",
        [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])
    gvxr.translateNode("Matrix", g_matrix_y, 0, g_matrix_x, "micrometer");
    gvxr.scaleNode("Matrix", g_matrix_width, 815, g_matrix_height, "mm");

    '''gvxr.shearNode("Matrix",
               0,
               apGeneSet[5],
               0,
               0,
               apGeneSet[6],
               0);'''


    gvxr.rotateNode("Matrix", apGeneSet[4] * 360.0, 0, 1, 0);

    # Matrix
    #gvxr.addPolygonMeshAsOuterSurface("Matrix");
    gvxr.setMixture("Matrix", matrix_material);
    gvxr.setDensity("Matrix", matrix_density, "g.cm-3");
    gvxr.setLinearAttenuationCoefficient("Matrix", matrix_mu, "cm-1");


def resetMatrix():
    setMatrix(matrix_parameter_set);
    gvxr.applyCurrentLocalTransformation("Matrix");

def addCylinder(x, y, i):
    #print (i, x, y)
    fibre_label = "fibre" + str(i);
    core_label = "core"   + str(i);

    gvxr.makeCylinder(fibre_label, 50, 815, fiber_radius, "micrometer");
    gvxr.makeCylinder(core_label, 50, 815,  core_radius, "micrometer");

    gvxr.setLocalTransformationMatrix(fibre_label, [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);
    gvxr.setLocalTransformationMatrix(core_label, [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]);

    gvxr.translateNode(fibre_label, y, 0, x, "micrometer");
    gvxr.translateNode(core_label,  y, 0, x, "micrometer");

    gvxr.applyCurrentLocalTransformation(fibre_label);
    gvxr.applyCurrentLocalTransformation(core_label);

    # Fiber
    gvxr.setCompound(fibre_label, fiber_material);
    gvxr.setDensity(fibre_label, fiber_density, "g.cm-3");
    gvxr.setLinearAttenuationCoefficient(fibre_label, fiber_mu, "cm-1");

    # Core
    gvxr.setElement(core_label, core_material);
    gvxr.setLinearAttenuationCoefficient(core_label, core_mu, "cm-1");

    gvxr.addMesh("fiber_geometry", fibre_label);
    gvxr.addMesh("core_geometry",  core_label);

activation_set = None;

def setCylinders(apGeneSet):

    gvxr.removePolygonMeshesFromXRayRenderer();
    gvxr.removePolygonMeshesFromSceneGraph();

    number_of_cylinders = round(len(apGeneSet) / 2);

    gvxr.emptyMesh("fiber_geometry", "root");
    gvxr.emptyMesh("core_geometry",  "root");

    for i in range(number_of_cylinders):

        x = g_matrix_x + (apGeneSet[i * 2 + 0] - 0.5) * max(g_matrix_width, g_matrix_height) * 1.25;
        y = g_matrix_y + (apGeneSet[i * 2 + 1] - 0.5) * max(g_matrix_width, g_matrix_height) * 1.25;

        # There is no activation_set, use all the individuals
        if type(activation_set) == type(None):
            #print(i+1, '/', number_of_cylinders, [apGeneSet[i * 2 + 0], apGeneSet[i * 2 + 1]])

            addCylinder(x, y, i);

        # There is an activation_set
        else:
            # Only use the active individuals
            if activation_set[i] == True:
                addCylinder(x, y, i);
            else:
                print('\t', i, " is deactivated ");


    # Matrix
    resetMatrix();
    #gvxr.subtractMesh("Matrix", "fiber_geometry")
    gvxr.setMixture("Matrix", matrix_material);
    gvxr.setDensity("Matrix", matrix_density, "g.cm-3");
    gvxr.saveSTLfile("Matrix")
    gvxr.setLinearAttenuationCoefficient("Matrix", matrix_mu, "cm-1");


    # Fiber
    #gvxr.subtractMesh("fiber_geometry", "core_geometry")
    gvxr.setCompound("fiber_geometry", fiber_material);
    gvxr.setDensity("fiber_geometry", fiber_density, "g.cm-3");
    gvxr.setLinearAttenuationCoefficient("fiber_geometry", fiber_mu, "cm-1");

    # Core
    gvxr.setElement("core_geometry", core_material);
    gvxr.setLinearAttenuationCoefficient("core_geometry", core_mu, "cm-1");

    #gvxr.addPolygonMeshAsOuterSurface("Matrix");
    #gvxr.addPolygonMeshAsOuterSurface("fiber_geometry");
    #gvxr.addPolygonMeshAsInnerSurface("fiber_geometry");
    gvxr.addPolygonMeshAsInnerSurface("core_geometry");


def computeSinogram():

    gvxr.disableArtefactFiltering();
    gvxr.enableArtefactFilteringOnGPU();

# Compute an X-ray image
    #print("Compute sinogram");

    sinogram = np.zeros((number_of_projections, detector_width_in_pixels), dtype=np.float);

    sinogram = np.array(gvxr.computeSinogram(
        0, 1, 0,
        'mm',
        number_of_projections,
        -angular_step));

    #gvxr.saveLastSinogram();
    #gvxr.saveLastLBuffer('saveLastLBuffer.mhd');
    #gvxr.saveLastCumulatedLBuffer('saveLastCumulatedLBuffer.mhd');

    return sinogram;

    for angle_id in range(0, number_of_projections):
        gvxr.resetSceneTransformation();
        gvxr.rotateScene(-angular_step * angle_id, 0, 1, 0);

        #gvxr.displayScene();
        #print (str(angle_id), ":\t", str(angular_step * angle_id), " degrees");
        # Rotate the scene

        # Compute the X-ray projection and save the numpy image
        np_image = np.array(gvxr.computeXRayImage());

        # Display the 3D scene (no event loop)
        #gvxr.displayScene();

        # Append the sinogram
        sinogram[angle_id] = np_image[math.floor(detector_height_in_pixels/2),:];

    total_energy = 0.0;
    for i, j in energy_spectrum_in_keV:
        total_energy += i * j * gvxr.getUnitOfEnergy('keV');


    blur_the_sinogram = False;
    if blur_the_sinogram:
        blurred_sinogram = np.zeros(sinogram.shape);




        t = np.arange(-20., 21., 1.);
        kernel=lsf(t*41)/lsf(0);
        kernel/=kernel.sum();
        #plt.plot(t,kernel);
        #plt.show();


        for i in range(sinogram.shape[0]):
            blurred_sinogram[i]=np.convolve(sinogram[i], kernel, mode='same');

        blurred_sinogram  = total_energy / blurred_sinogram;
        blurred_sinogram  = np.log(blurred_sinogram);
        blurred_sinogram /= (pixel_size_in_micrometer * gvxr.getUnitOfLength("um")) / gvxr.getUnitOfLength("cm");

        #np.savetxt("blurred_sinogram_gvxr.txt", blurred_sinogram);

        return blurred_sinogram;

    # Convert in keV
    sinogram  = total_energy / sinogram;
    sinogram  = np.log(sinogram);
    sinogram /= (pixel_size_in_micrometer * gvxr.getUnitOfLength("um")) / gvxr.getUnitOfLength("cm");

    #np.savetxt("sinogram_gvxr.txt", sinogram);

    gvxr.saveLastLBuffer('saveLastLBuffer.mhd');
    gvxr.saveLastCumulatedLBuffer('saveLastCumulatedLBuffer.mhd');

    np_image = np.array(gvxr.computeLBuffer('Matrix'));
    np.savetxt("l_buffer.txt", np_image);

    return sinogram;


def cropCenter(anImage, aNewSizeInX, aNewSizeInY):
    y, x = anImage.shape
    start_x = x // 2 - (aNewSizeInX // 2);
    start_y = y // 2 - (aNewSizeInY // 2);
    return anImage[start_y : start_y + aNewSizeInY,
            start_x : start_x + aNewSizeInX]


def initEnvironment():
    global g_reference_sinogram
    global g_reference_CT

    global g_normalised_reference_sinogram
    global g_normalised_reference_CT

    global reference_sinogram_entropy
    global reference_CT_entropy

    g_reference_CT       = cropCenter(np.loadtxt("W_ML_20keV.tomo-original.txt"),detector_width_in_pixels,detector_width_in_pixels);

    g_reference_sinogram = radon(g_reference_CT, theta=theta, circle=True).T

    g_normalised_reference_sinogram = IM.normalise(g_reference_sinogram);

    g_normalised_reference_CT = IM.normalise(g_reference_CT);

    reference_CT_entropy       = IM.getEntropy(g_reference_CT);
    reference_sinogram_entropy = IM.getEntropy(g_reference_sinogram);


    np.savetxt("normalised_sinogram_ref.txt", g_normalised_reference_sinogram);
    np.savetxt("normalised_CT_ref.txt",       g_normalised_reference_CT);

    #np.savetxt("sinogram_ref.txt", g_reference_sinogram);
    #np.savetxt("CT_ref.txt",       g_reference_CT);

    scipy.misc.toimage(g_normalised_reference_sinogram).save('sinogram_ref.jpg')
    scipy.misc.toimage(g_normalised_reference_CT).save('CT_ref.jpg')




    # Create an OpenGL context
    print("Create an OpenGL context")
    gvxr.createOpenGLContext();
    gvxr.setWindowSize(512, 512);

    # Create the X-ray simulator
    initXRaySimulator();
    gvxr.disableArtefactFiltering();
    #gvxr.enableArtefactFilteringOnGPU();
