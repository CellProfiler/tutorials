# NEW BUILD INSTRUCTIONS BASED ON [THIS ISSUE](https://github.com/CellProfiler/tutorials/issues/53)

## **To update these documents:** 
- Modify the tutorial Markdown documents (.md files) within `[YourTutorialsRepo]/internal_use/docs/source/[AnyTutorial]`. 
    - The accompanying images for the tutorial should live within the 'images' folder (sometimes called 'TutorialImages' or 'media', depending on the tutorial).
- If you're adding a tutorial or want to change their name you can do so by going to `[YourTutorialsRepo]/internal_use/docs/source/toc_en/` and editing the `index.rst` file. An example of the index structure:
<pre>
    Translocation <../Translocation/Translocation>     
    
    OR
    
    [Name to be displayed in the html index] <[Path to the .md file]> 
</pre>       

- *Don't forget to commit your changes to Github!!*

## **To build the html from the updated document**

- (Install sphynx)
- Make sure you've properly updated your index if necessary (see above)
- In your terminal `cd` into `[YourTutorialsRepo]/internal_use/docs/source/`
- Run `sphinx-build -b html -D root_doc=toc_en/index . ../build/html` to build html files in English
- Run `sphinx-build -b html -D language=es -D root_doc=toc_es/index . ../build/html_es` to build in Spanish  
- The html files will populate the `[YourTutorialsRepo]/internal_use/docs/build` folder
- Once you have an HTML version, use your browser's **"Print to PDF"** function to create an updated PDF file for the main tutorial folder.
- *Don't forget to commit your changes to Github!!*

## **To build/update the .toc files for the translation in transifex**

- (Install sphynx)
- Make sure you've properly updated your index if necessary (see above)
- In your terminal `cd` into `[YourTutorialsRepo]/internal_use/docs/source/`
- Run `sphinx-build -b gettext -D root_doc=toc_en/index . ../_build/gettext/` to build/update the English .toc files
- the .toc files will live within `[YourTutorialsRepo]/internal_use/docs/_build/gettext/`
- *Don't forget to commit your changes to Github!!*



================================================================================================================

# OLD INSTRUCTIONS:

### *(THESE INSTRUCTIONS MAY SOON BE DEPRECATED, BUT WILL ALWAYS STILL CONTINUE TO WORK)*

To update these documents, install pandoc, then type `pandoc FILENAME.rst -o FILENAME.html`.

Once you have an HTML version, use your browser's **"Print to PDF"** function to create
an updated PDF for the main tutorial folder.

