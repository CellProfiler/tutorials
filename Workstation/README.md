Download the images from https://data.broadinstitute.org/bbbc/BBBC018/

```bash
curl -O "https://data.broadinstitute.org/bbbc/BBBC018/BBBC018_v1_images.zip"
unzip BBBC018_v1_images.zip
```

Download this pipeline.
A key module that should belong in every pipeline that will be used for command line computing is the “CreateBatchFiles” module. If you have an existing pipeline you’d like to try instead, make sure it has the “CreateBatchFiles” module.
Answer these questions and assign their values to variables:
Where are my images located?
Assign this value to “FILEPATH”.
Where will the CellProfiler output be located?
Assign this value to “OUTPUT”
Where is my CellProfiler pipeline located?
Assign this value to “PIPELINE”
Create a filelist that will informs CellProfiler about the pool of images that will be processed.
```mkdir -p "${OUTPUT}"


FILELIST="${OUTPUT}/filelist.txt"


find "${FILEPATH}" -type f | tee "${FILELIST}" > /dev/null
```
Create a groupslist file that divides the image set into groups that will processed in parallel. The groups are defined within the pipeline by the metadata for each file. Here is a script that will create the groups file.
```GROUPSFILE="${OUTPUT}/groups.txt"


python cp_group_option_metadata_maker.py ${FILELIST} ${GROUPSFILE} ${PIPELINE}
```
Use parallel to run CellProfiler in parallel.
`parallel -j 26 cellprofiler -c -r -g {} -o "${OUTPUT}" -p "${PIPELINE}" --file-list="${FILELIST}" :::: "${GROUPSFILE}"`
