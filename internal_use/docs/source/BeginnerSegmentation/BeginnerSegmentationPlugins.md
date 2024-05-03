# Interfacing CellProfiler with other software tools via files and plugins

Beth Cimini 
<br>
Broad Institute of MIT and Harvard, Cambridge, MA.

## **Background information**

### General background information

This exercise is meant to extend and build upon the Beginner Segmentation exercise available from [the CellProfiler tutorials page](tutorials.cellprofiler.org) . Please consult that tutorial for general information on how to configure CellProfiler as well as information about the images. It will be generally assumed you understand the modules covered in that tutorial, including input, object creation, overlays, and saving. 

### What is this exercise?

There are a number of great software tools available to life scientists wishing to analyze images these days - [forum.image.sc](forum.image.sc) alone has more than 60 open-source tools! Sometimes, though, it helps to have a multi-tool workflow - do one step in Tool A, and then another in Tool B (and then possibly C, D, etc, but hopefully not!). In this tutorial, you'll try 3 different ways of accessing work you did in other tools. 

1. Loading masks created by other segmentation tools (in this case, [Cellpose](https://www.cellpose.org/), but the same strategy works for many tools which use this format).
1. Accessing [ilastik](https://www.ilastik.org/) to use a trained pixel classification model via CellProfiler's plugins system.
1. Running Cellpose in CellProfiler via CellProfiler's plugins system and a Docker container.

### Plugins

While CellProfiler doesn't have as many plugins as, say, Fiji, it does have many for you to try! 
You can visit plugins.cellprofiler.org to learn more. To quote from that site:

>Plugins advance the capabilities of CellProfiler but are not officially supported in the same way as modules. A module may be in CellProfiler-plugins instead of CellProfiler itself because:
>- it is under active development
>- it has a niche audience
>- it is not documented to CellProfiler’s standards
>- it only works with certain version of CellProfiler
>- it requires extra libraries or other dependencies we are unable or unwilling to require for CellProfiler
>- it has been contributed by a community member

```{tip}
- While that documentation has instructions for [installing plugins](https://plugins.cellprofiler.org/using_plugins.html#installing-plugins-without-dependencies), in step 2 it suggests downloading all of the CellProfiler plugins; this isn't a bad thing to do, but you can download individual plugins from GitHub with the website button below as well or instead.
```

````{tip}
- We strongly recommend making a dedicated folder to store your CellProfiler plugins, as loading can be slow if there are a lot of other miscellaneous files around (such if they sit in the Downloads folder, for example).

```{figure} ./TutorialImages/GitHubDownloadButton.png
:width: 400
:align: center

GitHub's "Download Raw Files" button
```
````

### Docker Desktop

In Exercise 3 (and for Windows users, optionally Excercise 2 as well), we want to access software that we either don't want to install locally because it's painful if you're not pretty comfortable in Python (Cellpose) or that we CAN install locally but may not play nicely with other tools' multiprocessing setup (ilastik). 

Computer scientists will often use software **containers** to ship tools or data that are hard to install - [here](https://journals.sagepub.com/doi/10.1177/25152459211017853) is a good introduction and overview for non-computer scientists. You can think of containers as "a pre-configured operating system in a box". Because they come to you pre-configured, installation of any software happens once-and-only-once (by the creator of the container, not by you), and should stay working for long after ie the latest Mac upgrade breaks a certain older software installation. Groups like [biocontainers](https://biocontainers.pro/) have already containerized many of the tools you know and love. There are a number of types of software containers, but one of the most common is called a **Docker** container. 

Most life scientists aren't aware of or don't use containers, especially because typical usage involves accessing them via your terminal. But Docker doesn't have to mean terminal! There are [containers that spit out interactive websites for you to use](https://github.com/COBA-NIH/docker_gradio_demo), and CellProfiler has plugins that are specifically set up to call other tools that live (and are executed) inside Docker containers. 

To do this, CellProfiler needs to have the infrastructure for Docker containers up and running, which you can give it by installing a free program called [**Docker Desktop**](https://www.docker.com/products/docker-desktop/). You don't need to make an account to use it, but you probably will need to reboot your computer after installation is complete. Then, whenever you want to use a Docker-calling plugin in CellProfiler, you simply must make sure that Docker Desktop is open and running, CellProfiler will take care of everything else!

```{figure} ./TutorialImages/DockerDesktop.png
:width: 700
:align: center

The Docker Desktop interface for Mac. Containers can be searched for in the top search bar!
```

```{warning}
Anytime you're installing a program that can run other programs, you must of course be careful. Dockers give you access to a huge variety of tools that might otherwise be hard to install (or install together), but exercise caution in only running containers you recognize or trust!
```

## **Exercise 1: Importing masks from another segmentation tool**

In this exercise, we will be loading in *label masks* (sometimes also called *label matrices*) made in Cellpose. Simply, a label mask is an image in which all the background pixels have a value of 0, all the pixels of object 1 have a value of 1, all the pixels of object 2 have a value of 2, etc. It is a commonly used format by many tools that do object segmentation (though unsuitable for applications where you have overlapping objects). Since many tools (including CellProfiler) can make these masks, CellProfiler has the ability to read them in and automatically detect them as objects.

We've used Cellpose 2.2.2 to generate nuclear masks from the DNA images and cell masks from the ActinGolgi images. 

### Only if you are curious - how did we make these label masks?
Cellpose was installed in a conda environment according to the [official instructions](https://github.com/MouseLand/cellpose?tab=readme-ov-file#installation) for installation with the GUI. The software was started in that conda environment using the command `cellpose`.

Nuclear masks were made by dragging each DNA image into the GUI, selecting the 'nuclei' model with default settings, and then saving them individually as PNG using *Cmd+N* (Mac) *Ctl+N* (Windows). Since there were only 10 images and the hotkeys were available, this was not too time-consuming to do.

```{figure} ./TutorialImages/CellposeGUI.png
:width: 700
:align: center

Nuclei segmented in the Cellpose GUI
```

Cell masks were made by navigating into the image folder and then running the command below; this requires some knowledge of the [Cellpose command line syntax](https://cellpose.readthedocs.io/en/latest/cli.html) but is much easier for large numbers of images.

`python -m cellpose --dir . --img_filter Ch4 --pretrained_model cyto2 --diameter 40 --save_png --verbose`

```{figure} ./TutorialImages/CellposeCLI.png
:width: 700
:align: center

 Command line execution of Cellpose
 ```

### Loading the label masks into CellProfiler

1. Open up a clean copy of CellProfiler (or run File -> New Project) and drag `bonus_1_import_masks.cppipe` into the pipeline panel.
1. Drag the `images_Illum-corrected` subfolder from the main Beginner Segmentation exercise and also the `cellpose_masks_cells` subfolder from this exercise. *Do not drag in the `cellpose_masks_nuclei` folder.*
1. Put CellProfiler into TestMode <img src="./TutorialImages/startTestMode.png" width="120"/>, open the eye icon <img src="./TutorialImages/EyeOpen.png" width="50"/> next to OverlayOutlines, and then hit <img src="./TutorialImages/Step.png" width="120"/> 3 times to create a classical segmentation and compare it with the Cellpose-generated version. You can check the settings in the OverlayOutlines module to see which outline color corresponds to which segmentation in the output.
1. Optionally, open the Workspace Viewer using <img src="./TutorialImages/WorkspaceViewer.png" width="120"/> to create easily on-the-fly customizable overlays.
1. Hit <img src="./TutorialImages/NextImageSet.png" width="120"/> and repeat a couple of times to examine the segmentations on more images.

```{admonition} Question for you
Are there cases where you think classical segmentation typically performs better? Where Cellpose performs better?
```

```{figure} ./TutorialImages/WorkspaceViewerImportedMasks.png
:width: 700
:align: center

Visualization of images and objects in the Workspace Viewer
```
### Reverse engineer how this worked
1. Open the NamesAndTypes module. 
1. Scroll down in NamesAndTypes to find the entry that adds the masks - is there any setting you notice about it that is different than for the other images?
1. Find the entry in NamesAndTypes that has 2 rules the image has to pass, not just one - do you understand why that is?

### Bonus-to-the-Bonus - add the provided nuclear segmentations as well
1. Drag and drop the `cellpose_masks_nuclei` folder in the Images module to add the nuclear masks to the image list.
1. Go to the NamesAndTypes module and configure it so both kinds of masks can be loaded (hint: there's a duplicate button!)
  - You'll probably have to modify the existing settings for loading the cell masks by changing its rule or adding a second rule. Do you understand how/why?

## **Exercise 2: Running ilastik locally or from a Docker container**

Classical segmentation requires the thing you care about in an image be bright and every single other pixel dark(er). If you have a good clean fluorescent signal for the thing you care about, great! If not, you may need to resort to some tricks.

One such trick is to train a classifier on a pixel-by-pixel basis to say "here is what I think is the likelihood that this is a pixel you want to end up in your segmentation"; this classifier then ends up creating for each  pixel a *probability value* that corresponds to how likely it thinks it is you want to segment that pixel. If your classifier is good, that will give you an image where the pixels you care about are high-probability (bright) and everywhere else is low-probability (dark). That's exactly what we want! Life scientists tend to call this **"Pixel Classification"**; computer scientists will sometimes refer to it as **"Semantic Segmentation"**.

There are a few popular Fiji plugins for doing this, including Weka Trainable Segmentation and Labkit, and you should absolutely use them if they work better for you! We tend to use ilastik, because it makes it easy to automate creating a classifier from a very small number of images and then bulk-applying it to many others in "Batch Processing" mode. You can check out a tutorial we have written for running ilastik, and *then* CellProfiler at [tutorials.cellprofiler.org](https://tutorials.cellprofiler.org/) (look for Pixel-based Classification). 

```{figure} ./TutorialImages/IlastikBatchMode.png
:width: 700
:align: center

ilastik's Batch Processing mode
```

Why do two steps though, when you can do one instead? In this tutorial we'll take a pre-trained ilastik classifer and run it inside our CellProfiler pipeline, so we can find and measure objects all in one step.

You will need either ilastik or Docker Desktop installed on your computer for this exercise. If ilastik, make sure it is CLOSED, if Docker Desktop, make sure it is OPEN. We recommend installing ilastik because it is a good and helpful tool, and will allow you to do this exercise's bonus challenge.

```{warning}
If you are on Windows, execute RunIlastik in Local mode (working on an installed copy of ilastik, rather than a copy inside a Docker file), this exercise will work in TestMode, but not will not run in analysis mode - we are working with the ilastik developers to determine why that is. This is fine for the purpose of this exercise; if you have a lot of your own data you want to run later, you can still use ilastik in a two step process, and/or use Dockerized ilastik.
```

### Only if you are curious - how did we train the classifier?

This classifer was made in ilastik 1.4.1b5 by training on 4 images (A14_site1, E18_site1, D16_site1, and C12_site1) in which we labeled just two classes: one class for nucleoli (yellow in the figure below), and one class for every other part of the image (blue in the imagebelow). One COULD have made more classes, but this, in practice, worked.

```{figure} ./TutorialImages/IlastikLiveUpdate.png
:width: 700
:align: center

Screenshot of this ilastik classifer
```

When using ilastik for fluorescence microscopy, you will likely get the best performance if you **keep your annotations extremely minimal** - the classifier you're going to use was trained by using 31 total pixels of annotation across the 4 images (13 pixels of annotation inside nucleoli, and 18 pixels outside of them); no image had more than 14 pixels annotated in total. We strongly suggest you make your classifiers one pixel at a time, doing point annotations! Resist the urge to draw squiggly lines all over the image! This feels counterintuitive but we promise it's true.

### Grab the Runilastik plugin
1. Download [the plugin](https://github.com/CellProfiler/CellProfiler-plugins/blob/master/active_plugins/runilastik.py) into a folder on your local computer. As stated above, we strongly suggest a folder that contains ONLY plugins.
1. In CellProfiler's File -> Preferences menu (CellProfiler -> Preferences in Mac), set the `CellProfiler plugins directory` to the folder containing the plugin.
1. Close and reopen CellProfiler to load the plugin.

### Load the classifier and evaluate it
1. Drag `bonus_2_ilastik.cppipe` into the pipeline panel.
1. Drag the `images_Illum-corrected` subfolder from the main exercise into the Images panel.
1. Open the RunIlastik module, set the path to your project file (`NucleoliDetection.ilp`) and then also:
  - ilastik-installed (recommended): set the path to your local installation of ilastik.
  - Docker-installed: change the top setting from Local to Docker.

3. Put CellProfiler into TestMode <img src="./TutorialImages/startTestMode.png" width="120"/>, open the eye icons <img src="./TutorialImages/EyeOpen.png" width="50"/> next to Runilastik and OverlayOutlines, and then hit <img src="./TutorialImages/Run.png" width="120"/>. You can check the settings in the OverlayOutlines module to see which outline color corresponds to which segmentation in the output.
  - You may wish to put a pause <img src="./TutorialImages/Pause.png" width="50"/> next to SaveImages, or uncheck it <img src="./TutorialImages/InactivatedModule.png" width="50"/>, to keep it from saving images, but that's up to you.

```{note}
If using Docker, the very first time you execute the Runilastik module, it will need to download a ~5GB file, which may be slow depending on your internet connection. You only need to do this step once, however!
```

4. Evaluate your prediction in Runilastik across a few image sets - how well does it perform? Does it perform worse on images it wasn't trained on?

```{figure} ./TutorialImages/RunIlastik.png
:width: 700
:align: center

Screenshot of the Runilastik module 
```

5. Evaluate your segmentations across a few image sets using OverlayOutlines and/or the WorkspaceViewer - are there cases where you think the ilastik model-based segmentation performs better? The filtering-and-masking segmentation?

```{figure} ./TutorialImages/WorkspaceViewerilastik.png
:width: 700
:align: center

Evaluating segmentations in the Workspace Viewer
```


### Bonus-to-the-Bonus - train your own ilastik model

Based on your evaluations above, can you identify some places where additional training might help fix some issues in the ilastik model? 

1. Open `NucleoliDetection.ilp` in ilastik.
1. Navigate to the `Training` tab. 
1. Turn `LiveUpdate` on.
1. Pick an image you think needed some help and add (a very small number of single-pixel) annotations. Did things get better or worse? 
1. Add some very large annotations (a long, squiggly line, for example) to one image, then switch images in order to prove to yourself large annotations can actually harm in some cases rather than help (if you want to save your classifier, go back and use the eraser tool to delete these!).
1. If you think you've sufficiently improved the prediction, save this model and return to CellProfiler. Did it help in the cases where you thought it would?

## **Exercise 3: Running Cellpose from a Docker container**

RunCellpose is by far our most popular plugin, simply because a) Cellpose is awesome! and b) `conda` installing software when you aren't very computationally comfortable isn't. You can use the plugin in either of two modes - using a local `conda` or `python` installation that contains both CellProfiler and Cellpose, OR using Docker. The run time with Docker is substantially slower (about a minute more per image, in our testing), but if installation would take you a long time and be frustrating, in this sense you can "trade" your personal hands-on frustration time for time where CellProfiler is running on your computer (but you aren't there). For many people, this is a good trade!

### Start Docker Desktop
1. If you have not already installed Docker Desktop from the link above, please do so! This may involve rebooting your computer.
1. Start Docker Desktop.
1. Optional but strongly recommended - once Docker Desktop opens, use the search functionality to search `Cellpose` and look for the `cellprofiler/runcellpose_with_pretrained` model and pull it. If for whatever reason this isn't working, move on, but it will save you some time later. 

### Grab the RunCellpose plugin
1. Download [the plugin](https://github.com/CellProfiler/CellProfiler-plugins/blob/11b46ee7f6eb78f97f784a731c5a1931b66c90d4/active_plugins/runcellpose.py) into a folder on your local computer. As stated above, we strongly suggest a folder that contains ONLY plugins.
1. In CellProfiler's File -> Preferences menu, set the `CellProfiler plugins directory` to the folder containing the plugin.
1. Close and reopen CellProfiler to load the plugin.

### Load the pipeline and evaluate segmentation
1. Drag `bonus_3_cellpose.cppipe` into the pipeline panel.
1. Drag the `images_Illum-corrected` subfolder from the main exercise into the Images module
1. Put CellProfiler into TestMode <img src="./TutorialImages/startTestMode.png" width="120"/>, open the eye icons <img src="./TutorialImages/EyeOpen.png" width="50"/> next to RunCellpose and OverlayOutlines, and then hit <img src="./TutorialImages/Run.png" width="120"/>
  - You may wish to put a pause next to SaveImages, or uncheck it, to keep it from saving images, but that's up to you

```{note}
If you didn't already pull the container in the Docker Desktop section above, the very first time you hit the RunCellpose module, it will need to download a ~13GB file, which may be slow depending on your connection. You only need to do this step once however!
```

```{figure} ./TutorialImages/RunCellpose.png
:width: 700
:align: center

The output of the RunCellpose module
```

4. As before, using OverlayOutlines and/or the WorkspaceViewer, evaluate segmentation on a few images. Where is CellProfiler doing better, and where is Cellpose doing better?
5. Use the <img src="./TutorialImages/Info.png" width="35"> button to learn more about the different parameters you can pass to Cellpose (we don't offer all of them, but many!) - how does tweaking these affect your output? How about changing the model you're using, and/or the image you're segmenting?

## What next? Want to know more about CellProfliler plugins and modules?
1. Read the [CellProfiler-plugins paper](https://pubmed.ncbi.nlm.nih.gov/37690102/)
2. Watch this [video](https://www.youtube.com/watch?v=fgF_YueM1b8) to learn how to write a module
