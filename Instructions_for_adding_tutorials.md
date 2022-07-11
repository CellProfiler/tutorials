# How to add a new tutorial to the repo

1. Gather all the necessary files in a folder. Give the folder a descriptive name with no spaces. Note that files > 25 MB (and especially >100 MB) may not be uploadable to GitHub. If your tutorial requires large files, please do the following: 
    1. Add the files to a folder with a descriptive name (no spaces)
    2. Zip the folder (on mac, right click > Compress...)
    3. Add the .zip file to google drive in the `Outreach` > `Workshops_Webinars_Tutorials` folder on the shared g drive
    4. Create a short link to these materials using https://broad.io/admin/golinks/add and include in the tutorial instructions that the images are available at that link. 

2. Make a PR adding the folder of materials to the tutorial repo. In addition to the materials, please also 
    1) write a short description of the tutorial to add to the readme and
    2) create a gif (tips on making one [here](https://docs.google.com/document/d/1G5odCSbX1fW8vReKH5ubgvWc1sIGquLisUe7t5pR7d8/edit#heading=h.kjidkmwv6jq3)) and add that gif to to the `assets` > `img` folder. 

3. Update the readme with the description and gif. If there is an associated blogpost or video, please link that using the appropriate badge. If the tutorial is particularly geared toward beginners, add the beginner badge. If the tutorial is advanced such that a user should definitely do a beginner tutorial first, use the advanced badge. 

## Here's an example of what the markdown looks like for the Translocation tutorial: 
```
## Translocation

<img class="imggif" src="assets/img/translocation.gif" alt="example segmentation" align="right" width="150">

A tutorial showing how to segment cells in CellProfiler and then classify them by phenotype in CellProfiler Analyst. This is our standard tutorial for those new to image analysis in general or CellProfiler in particular. <br>

<img src="assets/img/beginner-badge.png" alt="beginner" width="140px"> <a href="https://www.youtube.com/watch?v=LOD2yqBLXXk&t=4s"><img src="assets/img/video-badge.png" alt="video link" width="140px"> </a> <a href="https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/CellProfiler/tutorials/tree/master/Translocation" target="_blank"><img src="assets/img/download-button.png" alt="Download button" width="140px"> </a> 
```
Copy and adjust as needed. Here's a breakdown of what each line is and what you change: 
1. The title of the tutorial is after `##`
2. The gif. Change the name to whatever you saved the gif as in the assets/img folder
3. The description of the tutorial (just paste in your description here instead) No special formatting
4. Badges and buttons separated by spaces. For badges, you can copy and paste from a previous tutorial, but they're just a piece of HTML pointing to an image and sometimes a link. For instance, here is the badge for a video link: 

   `<a href="https://www.youtube.com/watch?v=LOD2yqBLXXk&t=4s"><img src="assets/img/video-badge.png" alt="video link" width="140px"> </a>`
  
   To use this, just change the youtube link after `href="` and paste the whole thing into the readme. 
  
   The badge for beginner tutorials is here: 
   `<img src="assets/img/beginner-badge.png" alt="beginner" width="140px">`
   Since this is just an image, you can just copy and paste that HTML into the readme.

   For the download link, use [DownGit](https://downgit.github.io/#/home) or just alter the download link in the translocation example:

   `<a href="https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/CellProfiler/tutorials/tree/master/Translocation" target="_blank"><img src="assets/img/download-button.png" alt="Download button" width="140px"> </a> `
  
   To change the download link, just sub in your folder name instead of `Translocation`.
   
   Here's a table of all the badges and buttons we currently have: 
   
| Badge/Button    | Description                                                            | Image / Example                                                                                                                                                                                                                    | Example HTML                                                                                                                                                                                                                         |
|-----------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Download button | Every tutorial should have a button to download all relevant materials | <a href="https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/CellProfiler/tutorials/tree/master/Translocation" target="_blank"><img src="assets/img/download-button.png" alt="Download button" width="140px"> </a> | `<a href="https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/CellProfiler/tutorials/tree/master/Translocation" target="_blank"><img src="assets/img/download-button.png" alt="Download button" width="140px"> </a>` |
| Video link      | Link to video of the tutorial (like a recorded workshop)               | <a href="https://www.youtube.com/watch?v=LOD2yqBLXXk&t=4s"><img src="assets/img/video-badge.png" alt="video link" width="140px"> </a>                                                                                              | `<a href="https://www.youtube.com/watch?v=LOD2yqBLXXk&t=4s"><img src="assets/img/video-badge.png" alt="video link" width="140px"> </a>`                                                                                              |
| Blogpost link   | Link to blogpost describing the tutorial                               | <a href="https://carpenter-singh-lab.broadinstitute.org/blog/annotating-images-with-cellprofiler-and-gimp"><img src="assets/img/blog-badge.png" alt="blog link" width=140px> </a>                                                  | `<a href="https://carpenter-singh-lab.broadinstitute.org/blog/annotating-images-with-cellprofiler-and-gimp"><img src="assets/img/blog-badge.png" alt="blog link" width=140px> </a>`                                                  |
| Advanced badge  | Tutorial for advanced CellProfiler users                               | <img src="assets/img/advanced-badge.png" alt="advanced" width="140px">                                                                                                                                                             | `<img src="assets/img/advanced-badge.png" alt="advanced" width="140px">`                                                                                                                                                             |
| Beginner badge  | Good tutorial for beginners to CellProfiler                            | <img src="assets/img/beginner-badge.png" alt="beginner" width="140px">                                                                                                                                                             | `<img src="assets/img/beginner-badge.png" alt="beginner" width="140px">`                                                                                                                                                             |

That's it. GitHub pages will take care of updating the website with these changes!
