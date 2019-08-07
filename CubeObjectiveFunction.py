import time
import math
import numpy as np
import pandas as pd
from skimage.transform import radon, iradon, iradon_sart
import scipy.misc
import copy
import os, shutil

from ObjectiveFunction import *

# Import the X-ray simulation library
import gvxrPython3 as gvxr

import XRayEnvironment as xrayenv

import ImageMetrics as IM


class CubeObjectiveFunction(ObjectiveFunction):
    def __init__(self):

        number_of_dimensions = 5;

        self.boundaries = [];
        for i in range(number_of_dimensions):
            self.boundaries.append([0,1]);

        self.best_metrics = float('inf');
        #self.best_metrics = 0;

        super().__init__(number_of_dimensions,
                         self.boundaries,
                         self.objectiveFunction,
                         1);

        self.optimiser = "unknown";
        self.run_ID = 0;

        self.elapsed_time = None;

        self.metrics_label_set = [];
        self.metrics_value_set = [];

        self.metrics_label_set.append('sinogram_entropy');
        self.metrics_label_set.append('sinogram_delta_entropy');
        #self.metrics_label_set.append('sinogram_histogram_ncc');
        self.metrics_label_set.append('sinogram_mae');
        self.metrics_label_set.append('sinogram_relative_error');
        self.metrics_label_set.append('sinogram_ssim');
        self.metrics_label_set.append('sinogram_mse');
        self.metrics_label_set.append('sinogram_rmse');
        self.metrics_label_set.append('sinogram_nrmse_euclidean');
        self.metrics_label_set.append('sinogram_nrmse_mean');
        self.metrics_label_set.append('sinogram_nrmse_min_max');
        self.metrics_label_set.append('sinogram_psnr');
        self.metrics_label_set.append('sinogram_zncc');

        self.metrics_label_set.append('fbp_entropy');
        self.metrics_label_set.append('fbp_delta_entropy');
        #self.metrics_label_set.append('fbp_histogram_ncc');
        self.metrics_label_set.append('fbp_mae');
        self.metrics_label_set.append('fbp_relative_error');
        self.metrics_label_set.append('fbp_ssim');
        self.metrics_label_set.append('fbp_mse');
        self.metrics_label_set.append('fbp_rmse');
        self.metrics_label_set.append('fbp_nrmse_euclidean');
        self.metrics_label_set.append('fbp_nrmse_mean');
        self.metrics_label_set.append('fbp_nrmse_min_max');
        self.metrics_label_set.append('fbp_psnr');
        self.metrics_label_set.append('fbp_zncc');


        self.columns = [];
        self.columns.append('Run_ID');
        self.columns.append('Method');
        self.columns.append('elapsed_time');
        self.columns.append('number_of_evaluations');

        for label in self.metrics_label_set:
            self.columns.append(label);

        self.columns.append('X');
        self.columns.append('Y');
        self.columns.append('W');
        self.columns.append('H');
        self.columns.append('alpha');

        self.output_metrics_file = pd.DataFrame(columns=self.columns);

        self.best_solution = [];

    def setExtraParameters(self, optimiser, run_ID):
        self.optimiser = optimiser;
        self.run_ID = run_ID;
        self.number_of_evaluation = 0;
        self.elapsed_time = None;
        self.best_metrics = float('inf');
        self.ZNCC_sinogram = 0.0;
        self.ZNCC_fbp = 0.0;
        self.metrics_value_set = []
        self.best_solution = [];

        if os.path.exists(self.getOutputDirectory()):
            print ('*** Delete' + self.getOutputDirectory() + '***')
            shutil.rmtree(self.getOutputDirectory());

        os.makedirs(self.getOutputDirectory())

    def getOutputDirectory(self):
        return self.optimiser + '_' + ('%03d' % self.run_ID)

    def objectiveFunction(self, aSolution):

        start = time.time();

        gvxr.removePolygonMeshesFromXRayRenderer();
        gvxr.removePolygonMeshesFromSceneGraph();

        xrayenv.setMatrix(aSolution);
        gvxr.applyCurrentLocalTransformation("Matrix");
        gvxr.addPolygonMeshAsInnerSurface("Matrix");

        raw_sinogram = xrayenv.computeSinogram();

        if self.elapsed_time == None:
            self.elapsed_time = time.time() - start;
        else:
            self.elapsed_time += time.time() - start;

        normalised_sinogram = IM.normalise(raw_sinogram);
        #test_image = iradon(sinogram.T, theta=xrayenv.theta, circle=True);

        # Display the 3D scene (no event loop)
        #gvxr.displayScene();

        #sinogram = (sinogram - sinogram.mean()) / sinogram.std();



        #aFlyAlgorithm.getIndividual(ind_id).computeMetrics();


        # Fitness based on NCC
        #ncc =  np.multiply(xrayenv.g_reference_sinogram, sinogram).mean();
        #ncc =  np.multiply(xrayenv.g_reference_CT, FBP).mean();

        # NCC of histograms
        #metrics = abs(IM.getNCC(IM.getHistogram(xrayenv.g_reference_sinogram, 32)[0], IM.getHistogram(sinogram, 32)[0]));

        # NCC of sinograms
        start = time.time();
        #metrics = IM.getMAE(xrayenv.g_normalised_reference_sinogram, normalised_sinogram);
        metrics = IM.getMAE(xrayenv.g_reference_sinogram, raw_sinogram);
        self.elapsed_time += time.time() - start;

        if self.best_metrics > metrics:

            FBP = iradon(raw_sinogram.T, theta=xrayenv.theta, circle=True);
            normalised_FBP = IM.normalise(FBP);

            #FBP       = (test_image       - test_image.mean())       / test_image.std();

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_CT.txt', FBP);

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_normalised_CT.txt', IM.zeroMeanNormalisation(FBP));

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_sinogram.txt', raw_sinogram);

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_normalised_sinogram.txt', IM.zeroMeanNormalisation(raw_sinogram));

            absolute_error_normalised_sinogram = np.abs(xrayenv.g_normalised_reference_sinogram - normalised_sinogram);

            absolute_error_sinogram = np.abs(xrayenv.g_reference_sinogram - raw_sinogram);

            absolute_error_normalised_CT = np.abs(xrayenv.g_normalised_reference_CT - normalised_FBP);

            absolute_error_CT = np.abs(xrayenv.g_reference_CT - FBP);

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_normalised_sinogram.txt', absolute_error_normalised_sinogram);

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_sinogram.txt', absolute_error_sinogram);

            scipy.misc.toimage(absolute_error_normalised_sinogram).save(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_normalised_sinogram.jpg')

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_normalised_CT.txt', absolute_error_normalised_CT);

            np.savetxt(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_CT.txt', absolute_error_CT);

            scipy.misc.toimage(absolute_error_normalised_CT).save(self.getOutputDirectory() + '/' + self.optimiser + '_absolute_error_normalised_CT.jpg')



            scipy.misc.toimage(normalised_sinogram).save(self.getOutputDirectory() + '/sinogram_gvxr_' + str(self.number_of_evaluation) + '.jpg')

            scipy.misc.toimage(normalised_sinogram).save(self.getOutputDirectory() + '/' + self.optimiser + '_sinogram.jpg')

            scipy.misc.toimage(normalised_FBP).save(self.getOutputDirectory() + '/CT_gvxr_' + str(self.number_of_evaluation) + '.jpg')

            scipy.misc.toimage(normalised_FBP).save(self.getOutputDirectory() + '/' + self.optimiser + '_CT.jpg')

            self.best_metrics = metrics;
            #print("Best ncc so far", self.number_of_evaluation, ncc*100, genes)

            self.ZNCC_sinogram = IM.getNCC(xrayenv.g_normalised_reference_sinogram, normalised_sinogram);

            self.ZNCC_fbp = IM.getNCC(xrayenv.g_normalised_reference_CT, normalised_FBP);

            metrics_all  = self.optimiser + ',';
            metrics_all += str(self.run_ID) + ',';
            metrics_all += str(self.number_of_evaluation) + ',';
            metrics_all += str(round(self.elapsed_time)) + ',';
            metrics_all += str(metrics) + ',';

            sinogram_entropy = IM.getEntropy(raw_sinogram);
            fbp_entropy      = IM.getEntropy(FBP);

            self.metrics_value_set = [];

            self.metrics_value_set.append(sinogram_entropy);

            self.metrics_value_set.append(abs(sinogram_entropy - xrayenv.reference_sinogram_entropy));

            #self.metrics_value_set.append((IM.getNCC(IM.getHistogram(xrayenv.g_normalised_reference_sinogram, 32)[0], IM.getHistogram(normalised_sinogram, 32)[0])));

            self.metrics_value_set.append(IM.getMAE(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getMeanRelativeError(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getSSIM(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getMSE(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getRMSE(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getNRMSE_euclidean(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getNRMSE_mean(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getNRMSE_minMax(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(IM.getPSNR(xrayenv.g_normalised_reference_sinogram, normalised_sinogram));

            self.metrics_value_set.append(self.ZNCC_sinogram);






            self.metrics_value_set.append(fbp_entropy);

            self.metrics_value_set.append(abs(fbp_entropy - xrayenv.reference_CT_entropy));

            #self.metrics_value_set.append((IM.getNCC(IM.getHistogram(xrayenv.g_normalised_reference_CT, 32)[0], IM.getHistogram(normalised_FBP, 32)[0])));

            self.metrics_value_set.append(IM.getMAE(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getMeanRelativeError(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getSSIM(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getMSE(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getRMSE(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getNRMSE_euclidean(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getNRMSE_mean(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getNRMSE_minMax(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(IM.getPSNR(xrayenv.g_normalised_reference_CT, normalised_FBP));

            self.metrics_value_set.append(self.ZNCC_fbp);


            for value in self.metrics_value_set:
                metrics_all += str(value) + ',';


            print("\tBest MAE so far (", self.number_of_evaluation, ") =", "%0.4f" % metrics,
                '\tBest ZNCC (sinogram) = ', "%0.2f" % (100 * self.ZNCC_sinogram),
                '\tBest ZNCC (CT) = ', "%0.2f" % (100 * self.ZNCC_fbp))


            row = [];
            row.append(self.run_ID);
            row.append(self.optimiser);
            row.append(self.elapsed_time);
            row.append(self.number_of_evaluation);

            for metric in self.metrics_value_set:
                row.append(metric);

            self.best_solution = copy.deepcopy(aSolution);

            row.append(self.best_solution[0]);
            row.append(self.best_solution[1]);
            row.append(self.best_solution[2]);
            row.append(self.best_solution[3]);
            row.append(self.best_solution[4]);

            self.output_metrics_file = self.output_metrics_file.append(pd.DataFrame([row], columns=self.columns), ignore_index=True);

            self.output_metrics_file.to_csv ('cube_output_metrics_file_' + str(self.run_ID) + '.csv', index = None, header=True)


        return (metrics);
