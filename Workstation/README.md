# Workstation tutorial
## Download BBBC018 images and pipeline
Download the images from https://data.broadinstitute.org/bbbc/BBBC018/

```bash
FILEPATH="/your/path/to/images"

curl -O "https://data.broadinstitute.org/bbbc/BBBC018/BBBC018_v1_images.zip"

unzip BBBC018_v1_images.zip -d "${FILEPATH}"
```

Download the tutorial pipeline.

```bash
curl -O "https://raw.githubusercontent.com/CellProfiler/tutorials/master/Workstation/bbbc018_batch.cppipe"
```

Answer these questions and assign their values to variables:
1. Where are my images located? `FILEPATH`
1. Where will the CellProfiler output be located? `OUTPUT`
1. Where is my CellProfiler pipeline located? `PIPELINE`

```bash
OUTPUT="/your/path/to/output"

PIPELINE="bbbc018_batch.cppipe"
```

Create a filelist that will informs CellProfiler about the pool of images that will be processed.

```bash
mkdir -p "${OUTPUT}"

FILELIST="${OUTPUT}/filelist.txt"

find "${FILEPATH}" -type f | tee "${FILELIST}" > /dev/null
```

Create a groups file that divides the image set into groups that will processed in parallel. The groups are defined within the pipeline by the metadata for each file. Here is a script that will create the groups file.

Download the script that finds groups from the pipeline file.

```bash
curl -O "https://raw.githubusercontent.com/CellProfiler/tutorials/master/Workstation/cp_group_option_metadata_maker.py"
```

```bash
GROUPSMETADATA="${OUTPUT}/groups_metadata.txt"

GROUPSOUTPUT="${OUTPUT}/groups_output.txt"

python cp_group_option_metadata_maker.py ${FILELIST} ${OUTPUT} ${PIPELINE}
```

## Running CellProfiler
Create the batch file.

```bash
cellprofiler -c -r -o "${OUTPUT}" -p "${PIPELINE}" --file-list="${FILELIST}"

BATCHFILE="${OUTPUT}/Batch_data.h5"
```

Use parallel to run CellProfiler in parallel.

```bash
paste -d '\t' "${GROUPSMETADATA}" "${GROUPSOUTPUT}" > cp_parallel.txt

PROCESS_NUMBER=2

parallel -j ${PROCESS_NUMBER} --colsep "\t" cellprofiler -c -r -g {1} -o "${OUTPUT}/"{2} -p "${BATCHFILE}" :::: cp_parallel.txt

#parallel -j ${PROCESS_NUMBER} cellprofiler -c -r -g {1} -o "${OUTPUT}/"{2} -p "${BATCHFILE}" :::: "${GROUPSMETADATA}" ::::+ "${GROUPSOUTPUT}"
```
### Running CellProfiler without using a batch file
A pipeline can also be run without using a batch file or the *CreateBatchFiles* module.

```bash
curl -O "https://raw.githubusercontent.com/CellProfiler/tutorials/master/Workstation/bbbc018.cppipe"
```

```bash
PROCESS_NUMBER=2

parallel -j ${PROCESS_NUMBER} --colsep "\t" cellprofiler -c -r -g {1} -o "${OUTPUT}/"{2} -p "${PIPELINE}"  --file-list="${FILELIST}" :::: cp_parallel.txt
```

## Consolidating distributed output
For each group of images processed by CellProfiler a set of output CSV files is created. To access all the CellProfiler output data at once the CSV files will be combined into a sqlite database file with cytominer-database.

Create the **ingest_config.ini** file.

```bash
nano ingest_config.ini
```

```
[filenames]
image = bbbc018_Image.csv
experiment = bbbc018_Experiment.csv
```
Run cytominer-database

```bash
cytominer-database ingest "${OUTPUT}" sqlite:///bbbc018.sqlite -c ingest_config.ini --no-munge
```
