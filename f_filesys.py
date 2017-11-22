# -*- coding: utf-8 -*-
import logging
import shutil
import os
import time
import codecs

# create logger
module_logger = logging.getLogger('harvest.filesys')


def dir_exists(p_dir):
    # Check if directory exists.
    # p_dir = dir path

    pass

    return os.path.exists(p_dir)


def fs_copy(p_src, p_dest):
    # Copies filesystem object.
    # p_src = source path
    # p_dest = destination path

    shutil.copy(p_src, p_dest)

    return


def fs_ls_list(p_dir):
    # Returns list of dirs in dir.
    # p_dir = dir path

    dir_list = []
    for dname in os.listdir(p_dir):
        dir_list.append(p_dir + '/' + dname)

    return dir_list


def fs_move(p_src, p_dest):
    # Moves directory. (May overwrite.)
    # p_src = source path
    # p_dest = destination path

    shutil.move(p_src, p_dest)

    return


def fso_older_than(p_fso, p_time):
    # Checks if filesystem object is older than given time (in ptime).
    # p_fso = path
    # p_time = time to compare with, given as yyyy-mm-ddTHH:MM:SS.

    result = 0
    if time.localtime(os.path.getctime(p_fso)) > p_time:
        result = 1

    return result


def is_dir(p_dir):
    # Checks if p_dir is directory
    # p_dir = dir path

    result = False
    if os.path.exists(p_dir):
        if os.path.isdir(p_dir):
            result = True

    return result


def ready_dir(p_dir):
    # If dir doesn't exit, create it.
    # If p_dir doesn't exit, create it (also creates intermediate-level dirs if needed).

    if not os.path.exists(p_dir):
        os.makedirs(p_dir)
    return


def ready_empty_dir(p_dir):
    # If dir exists, delete it. Then recreate dir (also creates intermediate-level dirs if needed).
    # p_dir = dir path

    if os.path.exists(p_dir):
        os.system("rm -rf '" + p_dir + "'")

    ready_dir(p_dir)

    return


def rec_file_list(p_dir):

    fileList = []

    for root, subFolders, files in os.walk(p_dir):
        for file in files:
            f = os.path.join(root,file)
            fileList.append(f)

    return fileList


def read_file(p_path):
    # Returns contents of a file as string
    # p_path = file to read

    str = ""

    if (os.path.exists(p_path)):
        sfile = open(p_path, 'r')
        str = sfile.read()
        sfile.close()

    return str


def run_cmd(p_cmd):
    # Run shell command.
    # p_cmd = command to run

    os.system(p_cmd)

    return


def versioner(p_path):
    # If path exists, returns a pathname for next version. This is to avoid overwriting.
    # !!! Needs to be worked out better, but currently sufficient.
    # Directories: /a -> /a_2 -> /a_3 -> ...
    # Files: a.ext -> a_2.ext -> a_3.ext -> ...
    # p_path = dir/file path

    result = p_path
    if (os.path.exists(p_path)):

        use_file_method = False
        part_1 = None
        extension = None
        c = 2

        if ('.' in p_path):
            part_1, extension = p_path.rsplit('.', 1)
            if (len(extension) <= 3):
                use_file_method = True

        if (use_file_method):
            result = part_1  + '_' + str(c) + '.' + extension

            while (os.path.exists(result)):
                c = c + 1
                result = part_1  + '_' + str(c) + '.' + extension

        else:
            result = p_path  + '_' + str(c)

            while (os.path.exists(result)):
                c = c + 1
                result = p_path  + '_' + str(c)

    return result


def write_file(p_contents, p_filename):
    # Write string to file. (May overwrite previous.)
    # p_contents = string to write
    # p_filename = file path

    if (p_filename):
        dest = p_filename
        sfile = open(dest, 'w')
        #p_contents = p_contents.encode('utf-8')
        sfile.write(p_contents)
        sfile.close()

    return

#--

def delete_dir(p_dir):
    # p_dir = dir path

    os.system("rm -rf '" + p_dir + "'")

    return



def delete_incomplete(p_dir):
    # Delete previously unfinished items in directory.
    # p_dir = dir path

    item_dirs = fs_ls_list(p_dir)
    for item_dir in item_dirs:
        if (os.path.basename(item_dir).count('_INCOMPLETE_') > 0):
            os.system("rm -rf '" + p_dir + '/' + os.path.basename(item_dir) + "'")

    return

	
	






