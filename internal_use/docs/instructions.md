NEW BUILD INSTRUCTIONS BASED ON [THIS ISSUSE](https://github.com/CellProfiler/tutorials/issues/53)

**To update these documents:** 
- Modify the tutorial MarkDown documents (.dm files) within `[YourTutorialsRepo]/internal_use/docs/source/[AnyTutorial`. The accompanying images for the tutorial live within the 'images' (sometimes also 'TutorialImages' or 'media', depending on the tutorial) folder.
- *Don't gorget to commit your changes to github!!*

**To update the Tutorial Index**
- Go to `[YourTutorialsRepo]/internal_use/docs/source/toc_en/index.rst` and change the location of the source .md file and/or the name to be displayed in the index for the toturial (default is the primary title of the document)
- Go to `[YourTutorialsRepo]/internal_use/docs/source/toc_es/index.rst` to do the same for the Spanish versions

Index looks like this:

   Beginner Segmentation <../BeginnerSegmentation/CPbeginner_Segmentation>
        ^                                        ^
Assigned name to the tutorial             Location of the .md file

**To build the html from the updated document**

- Install sphynx
- In your terminal `cd` into `[YourTutorialsRepo]/internal_use/docs/source`
- Run `sphinx-build -b html -D root_doc=toc_en/index . ../build/html` to build in English
- Run `sphinx-build -b html -D language=es -D root_doc=toc_es/index . ../build/html_es` to build in Spanish  



================================================================================================================
OLD INSTRUCTIONS:

(THESE INSTRUCTIONS MAY SOON BE DEPRECATED, BUT WILL ALWAYS STILL CONTINUE TO WORK)

To update these documents, install pandoc, then type pandoc FILENAME.rst -o FILENAME.html.

Once you have an HTML version, use your browser's "Print to PDF" function to create
an updated PDF for the main tutorial folder.

