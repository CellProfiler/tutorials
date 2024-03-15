
# FISH analysis in *C. elegans* 

**Tutorial for the Association of Biomolecular Research Facilities - Ligh Microscopy Research Group (ABRF/LMRG)**


## **Proposal:**

Segment the objects in a fluorescence z-stack image and provide:

- Centroid location in microns (um) for each spot: x, y, and z coordinates listed in separate columns. Labels x, y, and z.
- Integrated Intensity. Label intensity.
- 3D volume image of your segmented image
- Download CSV template [here](https://drive.google.com/file/d/10Y3er22JJAVUjtivFoP0fxJRAz9ma057/view?usp=sharing).
    (save as LastName_FirstName_ImageName.csv)

## **Input:**

Four different z-stack images that vary in their signal-to-noise ratio
and the clustering of their objects of FISH staining in *C. elegans*.

- Voxel dimensions: 0.162x0.162x0.200 um


**Calibration file**

- Voxel dimensions: 1x1x1 um

## **FishPipeline** - (4 min)


### **Importing data in CellProfiler**

1. Highlight the **Images** module.

   1. Drag-and-drop the images you will analyze into the Images module window.

```{image} media/image15.png
:width: 700
:align: center
```

2. Load the pipeline file (.cppipe). Drag-and-Drop the file or go to
File->Import->Pipeline from File.

> **Note**: The pipeline should populate all information needed, but it’s
always a good practice to check if everything is fine.


> **Tip: Use the question mark button (<img src="media/info.png" width="40"/>) to learn more or if you have questions.**

3. Highlight the **NameAndType** module.

> The **NamesAndTypes** module gives each image a meaningful name by
which modules in the analysis pipeline will refer to it. This module
will also let you define an image stack that should be processed as a
whole 3D volume.

1. Assign a name to: All images This is the simplest choice and the appropriate one because we have only one kind of image.
2. Process as 3D: Yes Selecting “Yes” will load the files as volumes
3. Populate the fields for “Relative Pixel Spacing”. This calibration affects modules that handle 3D images as volumes.

>The relative pixel spacing was provided and is 0.162 um in x and y and
0.200 um in z. To run the calibration file please change the relative
pixel spacing to 1x1x1 um.

4. Assign the images “variable names” that describe the contents in the image. For example, use the name "FISH" or "Worm" or something else that will remind you what the image is.
5. Hit the "Update" button to populate

```{image} media/image13.png
:width: 700
:align: center
```

## This pipeline can be divided into three main parts: Image processing,Segmentation and Measurement/export.

```{image} media/image4.png
:width: 400
:align: center
```

### **Image processing:**

The image processing is used to prepare the image for a correct
segmentation, in this case we have images with different signal-to-noise
ratio (SNR) and an important background signal from the worm. We will
first create a mask image of the worm and use this to remove the noise
and background from the original image. These modules should normalize
the images making the segmentation process work through all image sets.

1. Hit the <img src="media/StartTestMode.png" width="120"/> button.


>**Tip:** You can select different image sets. For that you can hit the <img src="media/NextImageSet.png" width="150"/> button or you can go to the
main tab, hit the test tab and choose another image set 
> <br>
>```{image} media/image16.png
>:width: 200
>:align: center
>```

<br>
2. **GaussianFilter** module: select the input image “fish” (or whatever the name you give for your images in **NamesAndTypes** module), name the output image as “GaussianFilter” and a Sigma value of “3” (larger sigmas induce more blurring). This module will blur the image and make the worm/background more evident for the threshold filter.

```{image} media/image20.png
:width: 700
:align: center
```

Hit the <img src="media/Step.png" width="120"/>  button and a new window will pop up with a resulting image that should look like this. The image can vary depending on the Image set chosen.

```{image} media/image32.png
:width: 700
:align: center
```

In this part of the pipeline we want to identify the worm and
not the spots, so we added a Threshold module to segment the worm.

3. **Threshold** module. This module produces a binary, or black and white, image based on a threshold that can be pre-selected or calculated automatically using one of many methods. After the threshold value has been determined, the Threshold module will set pixel intensities below the value to zero (black) and above the value to one (white).
   1. Select the input image: GaussianFilter (from **GaussianFilter** module)
   2. Name the output image: Threshold
   3. Threshold strategy: Global (We choose a global threshold strategy here because the out of worm background is relatively unifom after the gaussian filter).
   4. Threshold method: Minimum-Cross-Entropy (analyze the intensity distribution probability using the image histogram and define foreground and background)
   5. Threshold smoothing scale: 0.0 (Smoothing improves the uniformity of the resulting objects, by removing jagged edges caused by noise in the acquired image, because we used a gaussian filter module before this module, it’s not necessary to smooth the image prior to the threshold).
   6. Threshold correction factor: 1

> **Tip:** To view pixel intensities in an open image, move your mouse
over the image, the pixel intensities will appear in the bottom bar of
the display window.

```{image} media/image8.png
:width: 700
:align: center
```

```{image} media/image6.png
:width: 700
:align: center
```

4. **DilateObjects** module. The objective of this first part of the
pipeline is to remove the background and the noise on images without
removing information, so dilate the object will prevent objects touching
the edge of the worm to be removed in the following steps.

   1. Select the input object: Threshold
   2. Name the output object: DilateImage
   3. Structuring element: Ball (Size: 3) ( dilate the objects using a ball shape with size of 3).

```{image} media/image12.png
:width: 700
:align: center
```

5. **MaskImage** module. This module will hide the out of worm portions
of an image (based on previously identified objects or a binary image)
so they are ignored by subsequent mask-respecting modules in the
pipeline.

   1. Select the input image: fish (from **NamesAndTypes** module)
   2. Name the output image: MaskWorm
   3. Use objects or an image as a mask?: Image
   4. Select image for mask: DilateImage (from **DilateImage** module)
   5. Invert mask?: No (select the worm and not the background)

```{image} media/image26.png
:width: 700
:align: center
```

The resulting image looks the same as the original image, but the pixels
out the worm has a value of 0.

```{image} media/image11.png
:width: 700
:align: center
```

1. Select images to measure: MaskWorm (from **MaskImage** module)
2. Measure the intensity only from areas enclosed by objects: No
3. Calculate custom percentiles: No

```{image} media/image22.png
:width: 700
:align: center
```

1. Operation: Subtract

2. Name the output image: ImageAfterMath

3. Image or measurement?: Image

4. Select the first image: MaskWorm (from **MaskImage** module)

5. Multiply the first image by: 1.0

6. Image or measurement?: Measurement

   1. Category: Intensity (Select a measurement made on the image. The value of the measurement is used for the operand for all of the pixels of the other operand’s image).
   2. Measurement: MedianIntensity
   3. Image: MaskWorm (the image you choose in the **MeasureImageIntensity** module)

7. Multiply the second image by: 1.0

```{image} media/image3.png
:width: 700
:align: center
```

The resulting image shows just the spots without the background of the
worm.

> Tip: The image tools on the top toolbar may be helpful to see the details on your image/objects:

```{image} media/image31.png
:width: 400
:align: center
```

The 1st icon from the left lets you reset the view back to the original
view.

The 2nd and 3rd icons let you step backwards and forwards through any
changes you made to the view.

The 4th icon lets you change the view by moving in any direction in the
display, by clicking and dragging.

The 5th icon lets you change the view by zooming, by dragging and
drawing a box to zoom in on.

```{image} media/image9.png
:width: 400
:align: center
```

1. Selecting the input image image: ImageAfterMath (from **ImageAfterMath** module)
2. Name the output image: RescaleIntensity
3. Rescaling method: Stretch each image to use the full intensity range (Find the minimum and maximum values within the unmasked part of the image (or the whole image if there is no mask) and rescale every pixel so that the minimum has an intensity of zero and the maximum has an intensity of one).

```{image} media/image28.png
:width: 700
:align: center
```

The resulting image looks the same, but the pixel value differs between
images.

```{image} media/image1.png
:width: 700
:align: center
```

### **Segmentation**

After removing the worm background on different image sets we can start
the segmentation process.

#### Add a **Threshold** module.

   01. Select the input image: ReduceNoise (from **ReduceNoise** module)
   02. Name the output image: ThresholdSpots
   03. Threshold strategy: Global
   04. Threshold method: Robust Background (This method can be helpful if the majority of the image is background).
   05. Lower outliner fraction: 0.05 (discard this fraction of dim objects).
   06. Upper outliner fraction: 0.05 (discard this fraction of bright objects).
   07. Averaging method: Median (This is a good choice if the spot density is variable or high).
   08. Variance method: Standard deviation
   09. \# of deviations: 8 (value to multiply the calculated variance. Adding several deviations raises the threshold well above the average).
   10. Threshold smoothing scale: 0 (the objects are too small, smoothing before the threshold results in a larger object)
   11. Threshold correction factor: 1.2 (adjust the threshold to be more strict)
   12. Lower and upper bounds on threshold: 0, 1.0 (default)

```{image} media/image28.png
:width: 700
:align: center
```

```{image} media/image29.png
:width: 700
:align: center
```

#### **Watershed** module. 

This module is used to separate different objects in an image, which in this case will segment the nuclei.

   01. Use advanced settings: Yes
   02. Select the input image: ThresholdSpots (from the **Threshold** module)
   03. Name the output object: Spots
   04. Generate from: Distance (we don’t have markers to guide the segmentation process so the markers and other inputs for the algorithm will be automatically generated based on the footprint size).
   05. Footprint: 2 (defines the dimensions of the window used to scan the input image for local maxima, this will create a local maxima from a binary image that will be at the centers of objects). Large footprint will suppress local maximas that are close together into a single maxima, so two or more objects will be segmented as one. Small footprint can lead to oversegmenation, this means one nuclei segmented as two or more objects.
   06. Downsample: 1 (if the factor is 1, the image is not downsampled, the spots are too small, downsampling will remove objects).
   07. Declump method: Intensity
   08. Reference Image: MaskWorm (from **MaskImage** module)
   09. Segmentation distance transform smoothing factor: 0
   10. Minimum distance between seeds: 1
   11. Minimum absolute internal distance: 0.0
   12. Pixels from border to exclude: 0 (Default)
   13. Maximum number of seeds: -1 (Default no limit)
   14. Structuring element for seed dilation: Octahedron (Size: 1)

```{image} media/image5.png
:width: 700
:align: center
```

```{image} media/image14.png
:width: 700
:align: center
```

### **Measure and export data**

Now that the spots have been segmented, measurements can be made using
modules from the **Measurements** category. This study is asking for two
particular measurements:

- Centroid location (x, y and z)

- Integrated intensity

In this case we need the **MeasureObjectIntensity** module to extract
this information.

> **Note:** When applying these measurements, be careful to measure the
original images, not rescaled or processed images.

#### **MeasureObjectIntensity** module

   1. Select images to measure: fish (original image from **NamesAndTypes** module)
   2. Select objects to measure: Spots (from **Watershed** module) to have all the intensity measurements from the object.

```{image} media/image25.png
:width: 700
:align: center
```

> **Note:** The measure modules will provide several features for
identified objects and at this point we cannot choose which measurement,
so the module will extract all intensity features possible.

```{image} media/image17.png
:width: 500
:align: center
```

### **Creating visuals**

#### **RescaleIntesity** module. 

This module lets you rescale the intensity of the input images by any of several methods. You should use caution when interpreting intensity and texture measurements derived from images that have been rescaled because certain options for this module do not preserve the relative intensities from image to image.
   1. Selecting the input image image: fish (from **NamesAndTypes** module)
   2. Name the output image: RescaleIntensityFish
   3. Rescaling method: Stretch each image to use the full intensity range (Find the minimum and maximum values within the unmasked part of the image (or the whole image if there is no mask) and rescale every pixel so that the minimum has an intensity of zero and the maximum has an intensity of one).

```{image} media/image7.png
:width: 700
:align: center
```

```{image} media/image30.png
:width: 700
:align: center
```

#### **OverlayOutlines** module. 
This module places outlines of objects over a desired image. We recommend overlaying onto rescaled images, which will be easier to visualize outside of CellProfiler.
   1. Display outlines on a blank image: No
   2. Select image on which to display outlines: RescaleIntensityFish (from **RescaleIntensity** module)
   3. Outline display mode: Color
   4. How to outline: Outer
   5. Select objects to display: Spots (from **Watershed** module)
   6. Select outline color: Red (Default).

```{image} media/image21.png
:width: 700
:align: center
```

```{image} media/image27.png
:width: 700
:align: center
```
#### **SaveImages** module. 

01. Select the type of image to save: Image
02. Select the image to save: SpotsOverlay (from **OverlayOutlines** module)
03. Select method for constructing file names: From image filename (use this option to avoid reassignment of your images)
04. Select image name for file prefix: fish (select the original image name from NamesAndTypes module)
05. Append a suffix to the image file name?: No
06. Saved file format: tiff (tiff is a lossless format, but you can choose others depending on what you need to do with this images)
07. Image bit depth: 8-bit integer (this bit depth is easily read outside Cell Profiler)
08. Save with lossless compression: Yes
09. Output file location: Default Output Folder (or create a new folder just for this images)
10. Overwrite existing files without warning?: No (prevent file overwritten)
11. When to save: Every cycle (Save every image set)
12. Record the file and path information to the saved image?: No
13. Create subfolders in the output folder: No

```{image} media/image18.png
:width: 700
:align: center
```
#### **ConvertObjectsToImage** module. 

1. Select the input objects: Spots (from Watershed module)
2. Name the output image: SpotImage
3. Select the color format: Grayscale

```{image} media/image24.png
:width: 700
:align: center
```

### **Export measurements**

It’s good practice to place all export modules at the end of your
pipeline. CellProfiler automatically calculates execution times for each
module that was run before the export module. By placing your export
modules at the end of your pipeline, you will have access to module
execution times for each module in your pipeline. Save the output of the
measurement modules using **ExportToSpreadsheet** or
**ExportToDatabase**.

#### **ExportToSpreadsheet** module. 

This module exports measurements into
one or more files that can be opened in Excel or other spreadsheet
programs. This module will convert the measurements to a comma-, tab-,
or other character-delimited text format and save them to the hard drive
in one or several files, as requested.

01. Select the column delimiter: Comma (“,”)

02. Output file location: Default Output Folder

03. Add a prefix to file names: Yes

04. Filename prefix: FISH

05. Overwrite existing files without warning: No

06. Add image metadata columns to your object data file: No

07. Add image file and folder names to your object data file: No

08. Representation of Nan/Inf: NaN

09. Select the measurements to export: Yes

10. Press button to select measurements:

    1. Spots:

       1. Intensity: IntegratedIntensity

    2. Location

       1. Center: X, Y and Z

11. Calculate the per-image mean values for object measurements?:No

12. Calculate the per-image median values for object measurements?:No

13. Calculate the per-image standard deviation values for object measurements?:No

14. Output file location:Default Output Folder|

15. Create a GenePattern GCT file?:No

16. Export all measurement types?:No

17. Data to export: Spots

18. Use the object name for the file name?: No

19. File name: Spots.csv

20. Data to export: Experiment

21. Use the object name for the file name?: No

22. File name: Metadata.csv

```{image} media/image23.png
:width: 700
:align: center
```

### **Congratulations!** The spots have been segmented, measured and
exported. 

**End**
