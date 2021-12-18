import matplotlib.pyplot as plt
import numpy as np
from constants import *
from helper import *
import wfdb
import h5py

"""
@author: Timo Grautstück
"""


def get_channel_names(path_to_record):
    """ Returns a list containing all channel names

    :param path_to_record: str (Path to the record)
    :return: list (all channel names)
    """
    return wfdb.rdheader(path_to_record).sig_name


def plot_histogram(record):
    """ Plot a histogram for all given channels in the record

    :param record: str (path to record)
    :return:
    """
    fig, ax = plt.subplots(3, 5, figsize=(15, 6))
    fig.suptitle("Distribution of the signal values (" + wfdb.rdrecord(record).record_name + ")", size=20)
    fig.subplots_adjust(hspace=.4, wspace=.5)
    ax = ax.ravel()
    for i, value in enumerate(get_channel_names(record)):
        signal = wfdb.rdrecord(record, channels=[i]).p_signal
        signal = signal.reshape(signal.shape[0])
        ax[i].hist(signal, 20, density=True, color="c", edgecolor='black')
        ax[i].set_title(value, size=12)
    for i in range(len(get_channel_names(record)), len(ax)):
        fig.delaxes(ax[i])
    plt.show()


def plot_channel_distribution(channel_names, record_list):
    """ TODO: DOC
    """
    ret = np.zeros([len(channel_names)])
    for record in record_list:
        if get_channel_names(TRAIN_PATH + record) == channel_names:
            ret += np.ones(len(channel_names))
    return ret


def get_converted_sleep_stages(record_arousal, modified=False):
    """ get a numerical array containing sleep stages of
    the transmission file

    0 = UNDEFINED, 1 = N3 , 2 = N2,
    3 = N1       , 4 = REM, 5 = WAKE

    :param modified: TODO write doc
    :param record_arousal: str (.mat file)
    :return: np.array (containing sleep stages)
    """
    file = h5py.File(record_arousal)
    sleep_stages = file["data"]["sleep_stages"]
    # Get the samples to reshape
    shape = sleep_stages[STAGES[0]].shape[1]
    ret = np.zeros(shape).reshape(1, shape)
    if modified is False:
        for k in STAGES.keys():
            tmp = np.array(sleep_stages[STAGES[k]][:])
            tmp[tmp == 1] = k
            ret += tmp
    else:
        for k in STAGES.keys():
            tmp = np.array(sleep_stages[STAGES[k]][:])
            tmp[tmp == 1] = MODIFIED_STAGES[k]
            ret += tmp
    return ret.reshape(shape), extract_record_name(file), shape


def plot_sleep_stages(record_arousal, modified=False):
    """ Creates a plot to visualize sleep stages.

    :param modified: TODO write doc
    :param record_arousal: array (sleep stages)
    """

    stages, name, _ = get_converted_sleep_stages(record_arousal, modified)

    plt.figure(figsize=(12, 3))
    # Remove 0 (undefined) from the array
    if not modified:
        stages = np.delete(stages, np.argwhere(stages == 0))
        plt.yticks(
            list(TICK_LABELS.keys()),
            list(TICK_LABELS.values()),
            size=12
        )
    else:
        plt.yticks(
            list(MODIFIED_TICK_LABELS.keys()),
            list(MODIFIED_TICK_LABELS.values()),
            size=12
        )
    plt.xlabel("time in h", size=12)
    plt.xticks(size=12)
    plt.title(name)
    plt.grid()
    plt.plot(stages)


# not used, but maybe useful
def get_raw_sleep_stages(record_arousal):
    """ returns "raw" sleep stages as a matrix containing:
     1 = True and 0 = False

    [0] = N1        , [1] = N2,
    [2] = N3        , [3] = REM,
    [4] = undefined , [5] = wake

    :param record_arousal: str (.mat file)
    :return: np.array (matrix containing sleep stages)
    """
    sleep_stages = h5py.File(record_arousal)["data"]["sleep_stages"]
    samples = sleep_stages[STAGES[0]].shape[1]
    ret = []
    for v in STAGES.values():
        ret.append(sleep_stages[v][:])
    return np.array(ret).reshape(6, samples)


def distribution_sleep_stages(record_list):
    ret = np.zeros([6])
    for record in record_list:
        stages, _, samples = get_converted_sleep_stages(TRAIN_PATH + record + "-arousal.mat")
        for i in range(0, samples, 200 * 30):
            ret[int(stages[i])] += 1
    return ret
