# Interfacing CellProfiler with other software tools via files and plugins

Beth Cimini 
<br>
Broad Institute of MIT and Harvard, Cambridge, MA.

## **Background information**

### General background information

This exercise is meant to extend and build upon the Beginner Segmentation exercise available from tutorials.cellprofiler.org . Please consult that tutorial for general information on how to configure CellProfiler as well as information about the images. It will be generally assumed you understand the modules covered in that tutorial, including input, object creation, overlays, and saving. 

### What is this exercise?

There are a number of great software tools available to a biologist wishing to analyze images these days - forum.image.sc has more than 60 open-source tools alone. Sometimes, though, it helps to have a multi-tool workflow - do one step in ToolA, and then another in ToolB (and then possibly C, D, etc, but hopefully not!). In this tutorial, you'll try 3 different ways of accessing work you did in other tools. 

1. Loading masks created by other segmentation tools (in this case, [Cellpose](https://www.cellpose.org/), but many tools use this format)
1. Accessing [ilastik](https://www.ilastik.org/) to use a trained pixel classification model via CellProfiler's plugins system
1. Running Cellpose in CellProfiler via CellProfiler's plugins system and a Docker container

### Plugins

While CellProfiler doesn't have as many plugins as, say, Fiji, it does have many for you to try! You can visit plugins.cellprofiler.org to learn more. To quote from that site:

>Plugins advance the capabilities of CellProfiler but are not officially supported in the same way as modules. A module may be in CellProfiler-plugins instead of CellProfiler itself because:
>- it is under active development
>- it has a niche audience
>- it is not documented to CellProfiler’s standards
>- it only works with certain version of CellProfiler
>- it requires extra libraries or other dependencies we are unable or unwilling to require for CellProfiler
>- it has been contributed by a community member

````{tip}
While that documentation has instructions on [installing plugins](https://plugins.cellprofiler.org/using_plugins.html#installing-plugins-without-dependencies), in step 2 it suggests downloading all of the CellProfiler plugins; this isn't a bad thing to do, but you can download individual plugins from GitHub with the website button below as well or instead. We strongly recommend making a dedicated folder for CellProfiler plugins, as loading can be slow if there are a lot of other miscellaneous files around.

```{figure} ./TutorialImages/GitHubDownloadButton.png
:width: 400
:align: center

GitHub's "Download Raw Files" button
```
````

### Docker Desktop

In Exercise 3 (and for Windows users, optionally Excercise 2 as well), we want to access software that we either don't want to install locally because it's painful if you're not pretty comfortable in Python (Cellpose) or that we CAN install locally but may not play nicely with other tools' multiprocessing setup (ilastik). 

Computer scientists will often use software containers to ship tools or data that are hard to install - [here](https://journals.sagepub.com/doi/10.1177/25152459211017853) is a good introduction and overview for non-computer scientists. You can think of them as "a pre-configured operating system in a box". Because they come to you pre-configured, installation of any software happens once-and-only-once (by the creator of the container, not by you), and should stay working for long after ie the latest Mac upgrade breaks a certain older software installation. Groups like [biocontainers](https://biocontainers.pro/) have already containerized many of the tools you know and love. There are a number of types of software containers, but one of the most common is called a Docker container. 

Most biologists aren't aware of or don't use containers, especially because typical usage involves accessing them via your terminal. But Docker doesn't have to mean terminal! There are [containers that spit out interactive websites for you to use](https://github.com/COBA-NIH/docker_gradio_demo), and CellProfiler has plugins that are specifically set up to call other tools that live inside Docker containers. 

To do this, CellProfiler needs to have the infrastructure for Docker containers up and running, which you can give it by installing a free program called [Docker Desktop](https://www.docker.com/products/docker-desktop/). You need not make an account (but you probably will need to reboot your computer). You then simply must make sure the program is open and running when you try to use a Docker-calling plugin in CellProfiler - CellProfiler will take care of everything else!

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

### FYI only - how did we make these?
Cellpose was installed in a conda environment according to the [official instructions](https://github.com/MouseLand/cellpose?tab=readme-ov-file#installation) for installation with the GUI.

Nuclear masks were made by starting cellpose in that conda environment with the command `cellpose`, and then dragging each nuclear image into the GUI, selecting the nuclei model, and then saving to PNG with *Cmd+N* (Mac) *Ctl+N* (Windows). Since there were only 10 and the hotkeys were available, this was not too painful.

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

### Loading these masks into CellProfiler

1. Open up a clean copy of CellProfiler (or run File -> New Project) and drag `bonus_1_import_masks.cppipe` into the pipeline panel.
1. Drag the `images_Illum-corrected` subfolder from the main exercise and the `cellpose_masks_cells` subfolder from this exercise. *Do not drag in the `cellpose_masks_nuclei` folder.*
1. Put CellProfiler into TestMode <img src="./TutorialImages/startTestMode.png" width="120"/>, open the eye next to OverlayOutlines, and then hit <img src="./TutorialImages/Step.png" width="120"/> 3 times to create a classical segmentation and compare it with the Cellpose-generated version.
1. Optionally, open the Workspace Viewer to create easily on-the-fly customizable overlays
1. Hit <img src="./TutorialImages/NextImageSet.png" width="120"/> and repeat a couple of times to examine a couple more images

```{admonition} Question for you
Are there cases where you think classical typically performs better? Where Cellpose performs better?
```

```{figure} ./TutorialImages/WorkspaceViewerImportedMasks.png
:width: 700
:align: center

Visualization of images and objects in the Workspace Viewer
```
### Reverse engineer how this worked
1. Open the NamesAndTypes module 
1. Find the entry in NamesAndTypes that adds the masks - is there any setting you notice about it that is different than the other channels?
1. Find the entry in NamesAndTypes that has 2 rules the image has to pass, not just one - do you understand why that is?

### Bonus-to-the-Bonus - add the provided nuclear segmentations as well

1. Add the `cellpose_masks_nuclei` folder in the Images module
1. Go to the NamesAndTypes module and configure it so both kinds of masks can be loaded (hint: there's a duplicate button!)
  - You'll probably have to modify the existing settings for loading the cell masks by changing its rule or adding a second rule. Do you understand how/why?

## **Exercise 2: Running ilastik locally or from a Docker container**

```{figure} ./TutorialImages/IlastikLiveUpdate.png
:width: 700
:align: center

 Figure x: .
```

```{figure} ./TutorialImages/RunIlastik.png
:width: 700
:align: center

 Figure x: .
```


```{figure} ./TutorialImages/WorkspaceViewerilastik.png
:width: 700
:align: center

 Figure x: .
```

### Bonus-to-the-Bonus - train your own ilastik model

```{figure} ./TutorialImages/IlastikBatchMode.png
:width: 700
:align: center

 Figure x: .
```

https://github.com/CellProfiler/CellProfiler-plugins/blob/master/active_plugins/runilastik.py

## **Exercise 3: Running Cellpose from a Docker container**



https://github.com/CellProfiler/CellProfiler-plugins/blob/11b46ee7f6eb78f97f784a731c5a1931b66c90d4/active_plugins/runcellpose.py

```{figure} ./TutorialImages/RunCellpose.png
:width: 700
:align: center

 Figure x: .
```