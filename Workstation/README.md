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

python cp_group_option_metadata_maker.py ${FILELIST} ${OUTPUT} ${PIPELINE}
```

Create the batch file.
```bash
cellprofiler -c -r -o "${OUTPUT}" -p "${PIPELINE}" --file-list="${FILELIST}"

BATCHFILE="${OUTPUT}/Batch_data.h5"
```

Use parallel to run CellProfiler in parallel.

```bash
PROCESS_NUMBER=2

parallel -j ${PROCESS_NUMBER} cellprofiler -c -r -g {} -o "${OUTPUT}" -p "${BATCHFILE}" :::: "${GROUPSFILE}"
```
