# CellProfiler Tutorial: 3d monolayer

# Organizing and importing images

## A note on running CellProfiler

* Currently, 3d functionality is only available when running CellProfiler from source. Follow the instructions on the [CellProfiler GitHub wiki](https://github.com/CellProfiler/CellProfiler/wiki)
* In the future (Q3 2017) the easiest thing to do will be to download the nightly or release with CellProfiler 3D functionality from the [CellProfiler website](http://www.cellprofiler.org/downloads). The release of CellProfiler 3.0 will coincide with the availability of pre-built binaries.

## Z-stacks as TIFFs

* CellProfiler 3D currently only works with TIFF files. TIFF files can be rather complicated, having hyper-stack structures with all channels and z-planes in a single file. The acceptable CellProfiler format for storing z-stacks is to have a separate TIFF file for each channel.
* ImageJ or FIJI can be used to create TIFF stacks. Scripting can be used to create TIFF stacks.

## Importing data in CellProfiler

1. Highlight the Images module.
1. Drag-and-drop the images you will analyze into the Images module window.
1. Highlight the Metadata module.
1. Enter the following regular expression `^(?P<Plate>.*)_xy(?P<Site>[0-9])_ch(?P<ChannelNumber>[0-9])`. This regular expression will parse the filenames and organize the data.
1. Highlight the NamesAndTypes module.
1. Choose “Process as 3D”
1. Populate the fields for voxel size.
  * Fiji > Image > Show Info… (Ctrl + I)
  * Search for something like “Voxel size” or record this metadata when collecting own images
  * The actual units do not matter, rather their relative proportion. The numbers are unitless and therefore the decimal place does not matter.
1. Add three images to NamesAndTypes and give them "variable names" that describe the contents in the image. For example, use the name *dna* or *dapi* to describe an image stained with DAPI.

# Find objects: nuclei and cells

## Segmenting nuclei

## Image pre-processing

Before attempting to segement the cells in the images, conditioning the images with filters and various image processing methods will improve the results.

1. Add a RescaleIntensity module for each channel. It is a good practice to rescale images when processing them in CellProfiler. This standardizes the input in a way that makes processing images more reproducible and suppresses experimental variation and batch effects.
    <p align="center"><img src="docs/images/rescale_5.png" alt="rescale5" width="400"/><img src="docs/images/rescale_6.png" alt="rescale5" width="400"/><img src="docs/images/rescale_7.png" alt="rescale5" width="400"/></p>
1. Add a Resize module. Processing 3D images requires much more computation time than 2D images. Often, downsampling an image can yield large performance gains and at the same time smoothen an image to remove noise. If the objects of interest are relatively large compared to the pixel size, then segmentation results will be minimally affected the final segmentation.
    <p align="center"><img src="docs/images/resize_8.png" alt="rescale5" width="600"/></p>
1. Add a MedianFilter module. A median filter will homogenize the signal within the nucleus and reduce noise in the background. DNA is not uniformly distributed throughout the nucleus, which can lead to holes forming in the downstream object identification. A median filter will preserve boundaries better than other smoothing filters such as the Gaussian filter.
    <p align="center"><img src="docs/images/medianfilter_9.png" alt="rescale5" width="600"/></p>

## Segmentation

  1. Add an ApplyThreshold module. This will separate the foreground (nuclei) from the background.
<p align="center"><img src="docs/images/applythreshold_10.png" alt="rescale5"/></p>
  1. Add a Remove holes module. This module implements an algorithm that will remove small holes within the nucleus. Any remaining holes will contribute to over-segmentation of the nuclei. Choose a size of 100.
<p align="center"><img src="docs/images/removeholes_11.png" alt="rescale5"/></p>
  1. Add a Watershed module. This module implements the watershed algorithm, which will segment the nuclei. For more information on the watershed algorithm refer to the wikipedia page, https://en.wikipedia.org/wiki/Watershed_(image_processing)
<p align="center"><img src="docs/images/watershed_12.png" alt="rescale5"/></p>
  1. Add a ResizeObjects module to return the segmented nuclei to the size of the original image.
<p align="center"><img src="docs/images/resizeobjects_13.png" alt="rescale5"/></p>

## Segmenting the cells

The membrane presents more of a challenge, because unlike the nuclei, the membrane signal is not concentrated or well separated. However, the location of the nuclei can be used to help identify regions with cells.

## Transform nuclei into markers

  1. Add a ConvertObjectsToImageModule and convert the output from the Watershed module.
  <p align="center"><img src="docs/images/convertobjectstoimages_14.png" alt="rescale5"/></p>
  1. Shrink the nuclei to make them more seed-like by adding an Erosion module. Use the ball structuring element with a size of 3. The output of this module will be referred to as the seed image.
  <p align="center"><img src="docs/images/erosion_15.png" alt="rescale5"/></p>

## Transform the membrane channel

The Watershed module finds objects that have high signal. In the case of the cells that will be identified as objects, the cytoplasm should have high signal. However, this is not the case in the membrane channel. Therefore, we will invert the membrane channel to achieve this effect.
  1. Add an ApplyThreshold module and an ImageMath module. First, threshold the rescaled membrane image. Then, within the ImageMath module choose the Invert operation and invert the tresholded membrane.
<p align="center"><img src="docs/images/applythreshold_16.png" alt="rescale5"/></p>
<p align="center"><img src="docs/images/imagemath_17.png" alt="rescale5"/></p>

  1. Add a Remove holes module, again. Choose a size of 100. This result will be referred to as the cytoplasm image, because it contains high signal where cytoplasm exists.
<p align="center"><img src="docs/images/removeholes_18.png" alt="rescale5"/></p>

There is a problem with the thresholded membrane channel or cytoplasm image. The space above and the below the monolayer is also of high signal. The Watershed module cannot distinguish that this is not cytoplasm, so it will have to be removed. To do this we will take advantage of the signal across all channels to define the monolayer.

  1. Add another ImageMath module. Add all of the rescaled images together.
<p align="center"><img src="docs/images/imagemath_19.png" alt="rescale5"/></p>
  1. Add a GuassianFilter module. Choose a size of 30 to blend the signal together. The result should look like a cloud of signal where the monolayer resides.
<p align="center"><img src="docs/images/gaussianfilter_20.png" alt="rescale5"/></p>
  1. Add an ApplyThreshold module and threshold the smoothened monolayer image. This will define what is and is not monolayer. See that the space above and below the monolayer is entirely black.
<p align="center"><img src="docs/images/applythreshold_21.png" alt="rescale5"/></p>

Now we will combine the information from the membrane channel with what we identified about the monolayer through the summed-channel image. We will do this by subtracting the NOT-monolayer region from the image that defines the cytoplasm of the cells.

  1. Add an ImageMath module and invert the thresholded monolayer. This will create a NOT-monolayer image.
<p align="center"><img src="docs/images/imagemath_22.png" alt="rescale5"/></p>
  1. Add another ImageMath module and subtract the NOT-monolayer image from the cytoplasm image. The result is the image that will be used to define the boundaries of the cells.
<p align="center"><img src="docs/images/imagemath_23.png" alt="rescale5"/></p>
  1. Add a Watershed module. The input is the result of the previous ImageMath module. Change the *Generate from* option to *Markers*. The Markers will be the seed image created by the Erosion module. Finally, set the Mask to the same image and the Input. This will help preserve the cell boundaries.
<p align="center"><img src="docs/images/watershed_24.png" alt="rescale5"/></p>

# Creating visuals
Congratulations! The nuclei and cells have been segmented in this monolayer. Visuals that reveal the segmentation can be created within CellProfiler to validate and assess the performance of the pipeline.

  1. Add a OverlayObjects module to the pipeline. The input will be the rescaled DNA image. Choose the Objects to be the nuclei.
<p align="center"><img src="docs/images/overlayobjects_29.png" alt="rescale5"/></p>
  1. Add a Save module. Save the output from the previous module.

After running this pipeline and output image will be created. Use FIJI to inspect the this image.

Thank you for completing the 3d monolayer tutorial!
