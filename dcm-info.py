#!/usr/bin/env python


import dicom
import os
import sys

from argparse import ArgumentParser



def get_dicom_metadata(file,input_args):
    """
    Returns a dictionary of metadata extracted from DICOM file. 
    Returns an empty dictionary if no metadata could be found.
    """

    d = {}    
    plan = dicom.read_file(file, stop_before_pixels=True)
    
    # The following could be done without global flags, but we'd have
    # to pass values from parse_input() all the way to this (sub-)sub-function
    tags = []
    
    if input_args.sequence:
        tags.append('SeriesDescription')
    if input_args.name:
        tags.append('PatientName')
    if input_args.time:
        tags.append('AcquisitionTime')
    if input_args.date:
        tags.append('AcquisitionDate')        

    for t in tags:
        #print "plan.dir('{0}') = {1}".format(t,plan.dir(t))
        if plan.dir(t):
            d[t] = plan.data_element(t).value
        else:
            d[t] = '[error: not found in DICOM header]'

    return d



def find_dicom_files(dir, input_args):
    """
    Searches folder dir for DICOM files
    
    The form of the returned metadata is a list of dictionaries. 
    
    Returns an empty list if no DICOM files are found in dirpath
    Returns a single element list if if metadata is found and find_all is False    
    """

    metadata_list = []

    # Verify that dir argument actually points to a folder
    if not os.path.isdir(dir):
        print 'Error: {0} is not a directory'.format(dir)
        return []
        
    listing = [os.path.join(dir,f) for f in os.listdir(dir)]
    
    for f in listing:
        if not os.path.isfile(f):
            continue
        
        if f[f.rfind('.'):].lower() == '.dcm':
            md = get_dicom_metadata(f,input_args)
            if md:
                if not input_args.find_all_uniques:
                    return [md]
                if input_args.find_all_uniques and md not in metadata_list:                    
                    metadata_list.append(md)
            else:
                return [] # if no metadata was found, nothing to return
                    
    return metadata_list
                    


def parse_input():
    """
    Parses input
    
    Raises a usage error if there is a problem with the user's input
    """
   
    parser = ArgumentParser(description='Search folders for DICOM files and print metadata')

    
    parser.add_argument('-v', '--verbose', action='store_true', 
                        dest='verbose', default=False,
                        help='print additional output')
    parser.add_argument('folder', nargs='?', default=os.getcwd(),
                        help='the folder to search for DICOM files')
    
    parser.add_argument('--no-sequence', action='store_false', 
                        dest='sequence', default=True,
                        help='do not print SeriesDescription metadata')    
    parser.add_argument('-n', '--name', action='store_true', 
                        dest='name', default=False,
                        help='print PatientName metadata')    
    parser.add_argument('-t', '--time', action='store_true', 
                        dest='time', default=False,
                        help='print AcquisitionTime metadata')
    parser.add_argument('-d', '--date', action='store_true', 
                        dest='date', default=False,
                        help='print AcquisitionDate metadata')
                      
    parser.add_argument('-u', '--find-all-uniques', action='store_true', 
                        dest='find_all_uniques', default=False,
                        help='print all unique metadata found in each folder (takes longer)')
    
    input_args = parser.parse_args()
    
        
    """
    if #(disagreeable condition):
        parser.error('You must enter ________')
    """ 

    return input_args



def main():
    """
    Parses input 
    Searches for DICOM files in the user-provided folder (and subfolders)
    Prints the requested metadata if it can be found in those files
    """
    
    # parse arguments
    input_args = parse_input()
    
    # Populate a list of all the directories we want to check (the given folder,
    # its subfolders, and so on)
    dirs = [input_args.folder]
    for dirname, dirnames, _ in os.walk(input_args.folder):
        for subdirname in dirnames:
            dirs.append(os.path.join(dirname, subdirname))
    
    dirs.sort()
           
    for dir in dirs:
        metadata_list = find_dicom_files(dir, input_args)
        
        if len(metadata_list) == 0:
            continue
        
        print '{0}:'.format(dir)
        for i,md in enumerate(metadata_list, start=1):
            for tag in md:
                print '  {0:20s} {1}'.format(tag+':',md[tag])
            if input_args.verbose and len(metadata_list)>1 and i<len(metadata_list):
                print ' and' # separator between unique sets of metadata
        
        if input_args.verbose:
            print '\n', # blank line between folders

    return 0


    


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    sys.exit(main())




