"""
Find the groups options to run CellProfiler in batch from the command line.
"""

import os
import re
import sys

import click
import numpy
import pandas

@click.command()
@click.argument("filelist", type=click.File(mode="r"))
@click.argument("outpath", type=click.Path(exists=True))
@click.argument("pipeline", type=click.File(mode="r"))
def command(filelist, outpath, pipeline):
    """A program that creates a text file for batching processing images with CellProfiler by parsing a `*.cppipe` file. The output text file is saved in the same directory as the pipeline file.
    
    * filelist: The path to a text file. Each line of the text file is the full path to an image.
    * outpath: The path where the CellProfiler group information will be output.
    * pipeline: The path to a `*.cppipe` file.
    """
    groups_filename = os.path.join(outpath,"groups_metadata.txt")
    try:
        with open(groups_filename, "w") as f:
            f.write("groups_metadata.txt file access test.")
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print("cannot create output file {}".format(groups_filename))
        raise

    image_list = [line.rstrip('\n') for line in filelist]

    pipeline_list = [line.rstrip('\n') for line in pipeline]

    cp_group_option_metadata_maker(image_list, pipeline_list, groups_filename)

    click.echo(groups_filename)


def find_group_order(pipeline):
    """
    The metadata that is being used to group data is returned as a list.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """
    number_of_grouping_metadata = 0

    for ind, line in enumerate(pipeline):
        if re.match(r"^\s*Do you want to group your images\?:Yes$", line) is not None:
            re_out = re.search(r":(\d+)", pipeline[ind + 1])
            
            number_of_grouping_metadata = int(re_out.group(1))
                        
            ind_start = numpy.add(ind, 2)
            
            ind_end = numpy.sum([ind, 2, number_of_grouping_metadata])
            
            grouping_range = range(ind_start, ind_end)
            
            break
    
    pipeline_groups = [pipeline[ind] for ind in grouping_range]
    
    group_order_list = [None]*number_of_grouping_metadata
    
    for ind, text in enumerate(pipeline_groups):
        re_out = re.match(r"^\s*Metadata category:(\w+)$", text)
        
        group_order_list[ind] = re_out.group(1)
            
    return group_order_list


def is_image_set_grouped(pipeline):
    """
    Report if the pipeline will group image sets. Returns **True** if image sets will be grouped.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """
    is_grouped_bool = False
    
    for line in pipeline:
        if re.match(r"^\s*Do you want to group your images\?:Yes$", line) is not None:
            is_grouped_bool = True
            
            break
            
    return is_grouped_bool


def count_grouping_metadata(pipeline):
    """
    Returns the number of metadata extraction methods in a CellProfiler pipeline. If the pipeline is not setup to extract metadata then the number of methods is zero.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """
    number_of_grouping_metadata = 0

    for ind, line in enumerate(pipeline):
        if re.match(r"^\s*Do you want to group your images\?:Yes$", line) is not None:
            re_out = re.search(r":(\d+)", pipeline[ind + 1])
            
            number_of_grouping_metadata = re_out.group(1)
            
            break
                
    return number_of_grouping_metadata


def find_groups(metadata_df, group_order_list):
    """
    Find the group *keys* that define a collection of image sets. Groups are created from an ordered series of metadata variables that is defined in a CellProfiler pipeline.
    
    * group_order_list: The names of the metadata variables in a nested list, ordered in the way to group image sets.
    * metadata_df: a pandas dataframe where columns are metadata variables and rows are the metadata values for each image.
    """
    metadata_gb = metadata_df.groupby(by=group_order_list)
    
    groups_list = metadata_gb.indices.keys()
        
    groups_list.sort()

    if len(group_order_list) == 1:
        groups_list = [[metadata] for metadata in groups_list]

    return groups_list


def save_groups_options_for_command_line_batching(filename, groups_list, group_order_list):
    """
    Save a text file where each line contains an option value to process a group of image sets from the command line using the `-g` option. This text file can be used to batch process images from the command line with CellProfiler.
    
    * filename: the name of the output file.
    * groups_list: A list of tuples. Each tuple is a key to a group of image sets.
    * group_order_list: The names of the metadata variables in a list, ordered in the way to group image sets.
    """
    with open(filename, 'w') as f:
        for group in groups_list:
            group_order_pair = zip(group_order_list, group)
                        
            group_order_pair_list = ["Metadata_{}={}".format(pair[0], pair[1]) for pair in group_order_pair]
            
            group_option_string = ",".join(group_order_pair_list)
            
            f.write("{}\n".format(group_option_string))

    groups_text = read_text_file(filename)

    return groups_text


def cp_group_option_metadata_maker(file_list, pipeline, groups_filename):
    """Create a text file that contains CellProfiler metadata that groups image sets together.
    """
    assert is_extract_metadata(pipeline), "The pipeline is not configured to extract metadata. Please update the pipeline if this is incorrect."

    number_of_methods = count_extraction_methods(pipeline)

    assert number_of_methods > 0, "The pipeline is configured to extract metadata, but there are zero methods configured."

    filename_df = create_pandas_dataframe_with_filename_metadata(pipeline, file_list)

    metadata_df = filename_df

    assert is_image_set_grouped(pipeline), "The pipeline is not configured to group any image sets. Please update the pipeline if this is incorrect."

    group_order_list = find_group_order(pipeline)

    groups_list = find_groups(metadata_df, group_order_list)

    groups_text = save_groups_options_for_command_line_batching(groups_filename, groups_list, group_order_list)

    return groups_text


def decode_cellprofiler_pipeline_regular_expression_pattern_string(cp_re_string):
    """
    The regular expression pattern stored in a CellProfiler pipeline has the string escape character, a backslash, repeated several times. The pattern string must be decoded for use with the *re* module.
    
    * cp_re_string: the regular expression pattern found in the Metadata module of a CellProfiler pipeline `*.cppipe` file.
    """
    cp_re_string = cp_re_string.decode('string_escape').decode('string_escape')
    
    return cp_re_string


def get_filenames_from_list_of_paths(path_list):
    """
    Given a list of path strings, glob returns such a list, the path information is striped away and a list of only filenames is returned.
    
    * path_list: A list of paths. glob
    """
    filename_list = [os.path.split(item) for item in path_list]
    
    filename_list = map(list, zip(*filename_list))
    
    filename_list = filename_list[1]

    return filename_list


def parse_metadata_from_filenames(pipeline, metadata_filename_linenumber, filename_list):
    """
    Parse out the metadata for filenames as defined within a `*.cppipe` file by the Metadata module.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    * metadata_filename_linenumber: the line number that has the text `'    Metadata source:File name'` found in a pipeline file.
    * filename_list: a list of the names of images. They should be stripped of path information.
    """
    metadata_list_of_dict = [None]*len(filename_list)
    
    pipe_re_text = pipeline[metadata_filename_linenumber + 1]
    
    re_out_pattern_string = re.match(r"\s*Regular expression to extract from file name:(.*)", pipe_re_text)
    
    pipe_re_text = decode_cellprofiler_pipeline_regular_expression_pattern_string(re_out_pattern_string.group(1))
    
    for ind, filename in enumerate(filename_list):
        re_out_metadata = re.match(pipe_re_text, filename)
        
        if re_out_metadata:
            re_out_dict = re_out_metadata.groupdict()
            
            #re_out_dict = dict([(k,int(v)) if v.isdigit() else (k,v) for (k,v) in re_out_dict.items()])

            metadata_list_of_dict[ind] = re_out_dict
        else:
            metadata_list_of_dict[ind] = {"filename":filename}

    return metadata_list_of_dict


def create_pandas_dataframe_with_filename_metadata(pipeline, file_list):
    """
    Parse the pipeline and return a pandas dataframe with the metadata for each file in a list.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    * file_list: a list of the names of images. The list can have full path information or just filenames.
    """
    metadata_filename_ind_list = find_linenumbers_for_filename_metadata(pipeline)
    
    assert metadata_filename_ind_list, "There is no metadata for filenames."
    
    filename_list = get_filenames_from_list_of_paths(file_list)

    if len(metadata_filename_ind_list)==1:
        metadata_list_of_dict = parse_metadata_from_filenames(pipeline, metadata_filename_ind_list[0], filename_list)

        metadata_final_df = pandas.DataFrame.from_dict(metadata_list_of_dict)
        
        metadata_final_df = metadata_final_df.assign(filename=filename_list)
        
    else:
        list_of_all_metadata_from_filenames = []
    
        for ind in metadata_filename_ind_list:
            metadata_list_of_dict = parse_metadata_from_filenames(pipeline, ind, filename_list)

            metadata_df = pandas.DataFrame.from_dict(metadata_list_of_dict)
            
            metadata_df = metadata_df.assign(filename=filename_list)

            list_of_all_metadata_from_filenames.append(metadata_df)

        metadata_final_df = reduce(lambda left,right: pandas.merge(left,right,on='filename'), list_of_all_metadata_from_filenames)
    
    return metadata_final_df


def convert_column_names_to_cellprofiler_format(metadata_df):
    """
    Metadata in CellProfiler uses a specialized naming convention and this converts column names to the CellProfiler format.
    
    Note, each time this method is called the column names will be prefixed, so only call this method once for each dataframe.
    
    In general, metadata variable names must be prefixed with the string *Metadata_*.
    
    * metadata_df: a pandas dataframe where columns are metadata variables and rows are the metadata values for each image.
    """
    column_name_list = metadata_df.columns.values.tolist()
    
    new_column_name_list = ["Metadata_" + name for name in column_name_list]
    
    metadata_df.rename(columns = dict(zip(column_name_list, new_column_name_list)), inplace=True)
    
    return metadata_df


def read_text_file(path_to_file):
    """
    Read a text file and import each line as an item in a list.
    
    * path_to_file: the path to a text file.
    """
    with open(path_to_file) as f:
        lines = [line.rstrip('\n') for line in f]
        
    return lines


def find_linenumbers_for_filename_metadata(pipeline):
    """
    Find the linenumbers that contain the filename metadata info within the Metadata module in a CellProfiler pipeline.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """

    metadata_filename_linenumber_list = []

    for ind, line in enumerate(pipeline):
        if re.match(r'^\s*Metadata source:File name', line) is not None:
            metadata_filename_linenumber_list.append(ind)
            
    return metadata_filename_linenumber_list


def is_extract_metadata(pipeline):
    """
    Report if the pipeline will extract metadata. Returns **True** if metadata will be extracted.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """
    is_extract_metadata_bool = False
    
    for line in pipeline:
        if re.match(r"^\s*Extract metadata\?:Yes$", line) is not None:
            is_extract_metadata_bool = True
            
            break
            
    return is_extract_metadata_bool


def count_extraction_methods(pipeline):
    """
    Returns the number of metadata extraction methods in a CellProfiler pipeline. If the pipeline is not setup to extract metadata then the number of methods is zero.
    
    * pipeline: a list where each item is a line from a CellProfiler `*.cppipe` file.
    """
    number_of_methods = 0
    
    for ind, line in enumerate(pipeline):
        if re.match(r"^\s*Extract metadata\?:Yes$", line) is not None:
            re_out = re.search(r":(\d+)", pipeline[ind + 3])

            number_of_methods = re_out.group(1)
            
            break
            
    return number_of_methods


if __name__ == "__main__":
    command(sys.argv[1:])
