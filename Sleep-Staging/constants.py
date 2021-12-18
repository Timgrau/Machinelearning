""" Provides some variables that can be easily changed
@author: Timo Grautstück
"""

""" Paths """
HARD_DRIVE = "/run/media/timo/AA32-EC21/"
DATA_PATH = "PhysioNet_Dataset/physionet.org/files/challenge-2018/1.0.0/"
TRAIN = "training/"
TRAIN_PATH = HARD_DRIVE + DATA_PATH + TRAIN

""" Variables """

STAGES = {
    3: "nonrem1",
    2: "nonrem2",
    1: "nonrem3",
    4: "rem",
    0: "undefined",
    5: "wake"
}
MODIFIED_STAGES = {
    3: 2,
    2: 2,
    1: 1,
    4: 3,
    0: 4,
    5: 4,
}
# Labels for plots
TICK_LABELS = {
    0: "UND",
    1: "N3",
    2: "N2",
    3: "N1",
    4: "REM",
    5: "WAKE"
}
MODIFIED_TICK_LABELS = {
    1: "deep sleep",
    2: "light sleep",
    3: "REM",
    4: "wake"
}
