""" Provide some helper functions.
@author: Timo Grautstück
"""


def extract_record_name(h5py_object):
    _, record_name, _ = str(h5py_object).split('"')
    return record_name.replace("-arousal.mat", "")


def get_all_records(path_to_record, text_file):
    file = open(path_to_record + text_file)
    ret = []
    # loop through all records
    for line in file:
        record = line.strip() + line.strip().replace("/", "")
        ret.append(record)
    file.close()
    return ret

