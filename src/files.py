#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Python standard library
from __future__ import print_function
import os, sys, re

# Local imports
from utils import (
    Colors,
    err,
    fatal
)


def clean(s, remove=['"', "'"]):
    """Cleans a string to remove any defined leading or trailing characters.
    @param s <str>:
        String to clean.
    @param remove list[<str>]:
        List of characters to remove from beginning or end of string 's'.
    @return s <str>:
        Cleaned string
    """
    for c in remove:
        s = s.strip(c)
    return s


def index(file, delim='\t', required = ['sample', 'group']):
    """Return the index of expected columns in provided file. A groups 
    file is expected to have the following required. 
    @Required columns:
        - sample, group
    @param file <str>:
        Path to groups TSV file.
    @return tuple(indices <dict[int/None]>, hasHeader <boolean>):
        [0] Dictionary containing information the index of each required/optional column
        [1] Boolean to indicate whether file has a header
    """
    c = Colors()
    indices = {}
    has_header = True  
    
    # Check to see if the file is empty
    fh = open(file, 'r')
    try:
        header = [clean(col.lower().strip()) for col in next(fh).strip().split(delim)]
    except StopIteration:
        err('{0}{1}Error: groups file, {2}, is empty!{3}'.format(c.bg_red, c.white, file, c.end))
        fatal('{0}{1}Please add sample and group information to the file and try again.{2}'.format(c.bg_red, c.white, c.end))
    finally:
        fh.close()
    
    # Parse the header to get the index of required fields
    try:
        # Get index of sample, group
        # columns for parsing the file
        for col in required:
            col = col.lower()
            indices[col] = header.index(col)
    except ValueError:
        # Missing column names or header in peakcall file
        # This can also occur if the file is not actually 
        # a tab delimited file.
        # TODO: Add a check to see if the file is actually
        # a tab delimited file, i.e. a TSV file.
        has_header = False
        err(
            '{0}{1}Warning: {2} is missing at least one of the following column names: Sample, Group {3}'.format(
                c.bg_yellow,
                c.black,
                file,
                c.end
            )
        )
        err('{0}{1}\t  └── Making assumptions about columns in the peakcall file... 1=Sample, 2=Group {2}'.format(
            c.bg_yellow,
            c.black,
            c.end)
        )
        # Setting column indexes to the following defaults (zero-based):
        # 0 = Sample column
        # 1 = Group information column
        for i in range(len(required)):
            indices[required[i]] = i
        
    return indices, has_header


def groups(file, delim='\t'):
    """Reads and parses a sample sheet, groups.tsv, into a dictionary. 
    This file acts as a sample sheet to gather sample metadata and define 
    relationship betweeen groups of samples. This file is used to pair a
    sample with its group. This tab delimited file contains two columns.
    One column for the basename of the sample and one column for the 
    sample's group. It is worth noting that a sample can belong to more
    than one group. A 1:M sample to group relationship can be denoted by
    seperating muliptle groups with commas (i.e. ','). This group information
    is used downstream in the pipeline for differential-like analyses. 
    Comparisons between groups can be made with a constrast.tsv file.
    This function returns a dictionary containing group to sample lists.
    @Example: groups.tsv
        Sample          Group
        Sample_A_rep1	GrpA,GrpAB
        Sample_A_rep2	GrpA,GrpAB
        Sample_B_rep1	GrpB,GrpAB
        Sample_B_rep2	GrpB,GrpAB
        Sample_C_rep1	GrpC,GrpCD
        Sample_C_rep2	GrpC,GrpCD
        Sample_D_rep1	GrpD,GrpCD
        Sample_D_rep2	GrpD,GrpCD
    
    >> groups = groups('peakcall.tsv')
    {
        'GrpA': ['Sample_A_rep1', 'Sample_A_rep2'],
        'GrpB': ['Sample_B_rep1', 'Sample_B_rep2'],
        'GrpC': ['Sample_C_rep1', 'Sample_C_rep2'],
        'GrpD': ['Sample_D_rep1', 'Sample_D_rep2'],
        'GrpAB': ['Sample_A_rep1', 'Sample_A_rep2', 'Sample_B_rep1', 'Sample_B_rep2'],
        'GrpCD': ['Sample_C_rep1', 'Sample_C_rep2', 'Sample_D_rep1', 'Sample_D_rep2']
    }
    @param file <str>:
        Path to peakcall TSV file.
    @return groups <dict[str]>:
        Dictionary containing group to samples, where each key is group 
        and its value is a list of samples belonging to that group
    """
    # Get index of each required and 
    # optional column and determine if
    # the file has a header
    c = Colors()
    indices, header = index(file)
    s_index = indices['sample']
    g_index = indices['group']
    # Parse the samples and
    # grab group information 
    groups = {}
    # Keep track of line number
    # to report where errors or
    # warnings are coming from
    lineno = 0
    with open(file, 'r') as fh:
        if header:
            # Skip over header and
            # start parsing the file
            lineno += 1
            _ = next(fh)
        for line in fh:
            lineno += 1
            linelist = [l.strip() for l in line.split(delim)]
            try:
                sample = clean(linelist[s_index])
                group = linelist[g_index]
            except IndexError:
                # Can occur due to empty lines or
                # if a user only has 1 column of
                # information, this checks if the
                # line is blank to silently continue
                filtered = [item for item in linelist if item]
                if filtered:
                    err(
                        '{0}{1}Warning: Sample or Group column is missing for line {2}: {3}, skipping line...{4}'.format(
                            c.bg_yellow,
                            c.black,
                            lineno,
                            linelist,
                            c.end
                        )      
                    )
                continue
            
            if not sample or not group: 
                err(
                    '{0}{1}Warning: Sample or Group information is missing for line {2}: {3}, skipping line...{4}'.format(
                        c.bg_yellow,
                        c.black,
                        lineno,
                        linelist,
                        c.end
                    )
                )
                continue # skip over empty string
            
            # Check for multiple groups,
            # split on comma or semicolon
            multiple_groups = re.split(';|,',group)
            multiple_groups = [clean(g.strip()) for g in multiple_groups]
            for g in multiple_groups:
                if g not in groups:
                    groups[g] = []
                if sample not in groups[g]:
                    groups[g].append(sample)

    return groups


def contrasts(file, groups, delim='\t'):
    """Reads and parses the group comparison file, contrasts.tsv, into a 
    dictionary. This file acts as a config file to setup contrasts between
    two groups, where groups of samples are defined in the peakcalls.tsv file.
    This information is used in differential analysis, like differential binding
    analysis or differential gene expression, etc. 
    @Example: contrasts.tsv
        G2  G1
        G4  G3
        G5  G1
    >> contrasts = contrasts('contrasts.tsv', groups = ['G1', 'G2', 'G3', 'G4', 'G5'])
    >> contrasts
    [
        ["G2",  "G1"],
        ["G4",  "G3"],
        ["G5",  "G1"]
    ]
    @param file <str>:
        Path to contrasts TSV file.
    @param groups list[<str>]:
        List of groups defined in the peakcall file, enforces groups exist.
    @return comparisons <list[list[str, str]]>:
        Nested list contain comparsions of interest.  
    """

    c = Colors()
    errors = []
    comparsions = []
    line_number = 0
    with open(file) as fh:
        for line in fh:
            line_number += 1
            linelist = [clean(l.strip()) for l in line.split(delim)]
            try:
                g1 = linelist[0]
                g2 = linelist[1]
                if not g1 or not g2: continue # skip over empty lines
            except IndexError:
                # Missing a group, need two groups to tango
                # This can happen if the file is NOT a TSV file,
                # and it is seperated by white spaces, :(  
                err(
                '{}{}Warning: {} is missing at least one group on line {}: {}{}'.format(
                    c.bg_yellow,
                    c.black,
                    file,
                    line_number,
                    line.strip(),
                    c.end
                    )
                )
                err('{}{}\t  └── Skipping over line, check if line is tab seperated... {}'.format(
                    c.bg_yellow,
                    c.black,
                    c.end)
                )
                continue
            # Check to see if groups where defined already,
            # avoids user errors and spelling errors
            for g in [g1, g2]:
                if g not in groups:
                    # Collect all error and report them at end
                    errors.append(g)
            
            # Add comparsion to list of comparisons
            if [g1, g2] not in comparsions:
                comparsions.append([g1, g2])

    if errors:    
        # One of the groups is not defined in peakcalls
        err('{}{}Error: the following group(s) in "{}" are not defined in peakcall file! {}'.format(
            c.bg_red, 
            c.white,
            file,
            c.end)
        )
        fatal('{}{}\t  └── {} {}'.format(
            c.bg_red,
            c.white,
            ','.join(errors),
            c.end)
        )
    
    return comparsions


if __name__ == '__main__':
    # Testing groups file parser
    print('Parsing groups file...')
    group2samples = groups(sys.argv[1])
    print(group2samples)
    # Testing contrasts file parser
    # print('Parsing contrasts file...')
    # comparsions = contrasts(sys.argv[2], groups=groups.keys())
    # print(comparsions)