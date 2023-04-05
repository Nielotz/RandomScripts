SERIES_FOLDER_PATH = r"D:\Futurama"  # Path to folder with seasons folder.
SERIES_NAME = "FUTURAMA"  # Used to createname filenames.

import shutil
import os
from collections import namedtuple
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

if not os.path.exists(SERIES_FOLDER_PATH):
    raise NotADirectoryError(f"Invalid SERIES_FOLDER_PATH = {SERIES_FOLDER_PATH} - thing not exists")

# Match episode id with other data.
# end_id - relates only when multiple episodes are concatenated, if not apply, set equal id_ - episode_data key
EpisodeData = namedtuple('EpisodeData', ['end_id', 'season', 'season_episode_id', 'title'])
episode_data = {
    1: EpisodeData(1, 1, 1, "Space Pilot 3000"),
    2: EpisodeData(2, 1, 2, "The Series Has Landed"),
    3: EpisodeData(3, 1, 3, "I, Roommate"),
    4: EpisodeData(4, 1, 4, "Love's Labours Lost in Space"),
    5: EpisodeData(5, 1, 5, "Fear of a Bot Planet"),
    6: EpisodeData(6, 1, 6, "A Fishful of Dollars"),
    7: EpisodeData(7, 1, 7, "My Three Suns"),
    8: EpisodeData(8, 1, 8, "A Big Piece of Garbage"),
    9: EpisodeData(9, 1, 9, "Hell Is Other Robots"),
    10: EpisodeData(10, 1, 10, "A Flight to Remember"),
    11: EpisodeData(11, 1, 11, "Mars University"),
    12: EpisodeData(12, 1, 12, "When Aliens Attack"),
    13: EpisodeData(13, 1, 13, "Fry and the Slurm Factory"),
    14: EpisodeData(14, 2, 1, "I Second That Emotion"),
    15: EpisodeData(15, 2, 2, "Brannigan, Begin Again"),
    16: EpisodeData(16, 2, 3, "A Head in the Polls"),
    17: EpisodeData(17, 2, 4, "Xmas Story"),
    18: EpisodeData(18, 2, 5, "Why Must I Be a Crustacean in Love?"),
    19: EpisodeData(19, 2, 6, "The Lesser of Two Evils"),
    20: EpisodeData(20, 2, 7, "Put Your Head on My Shoulders"),
    21: EpisodeData(21, 2, 8, "Raging Bender"),
    22: EpisodeData(22, 2, 9, "A Bicyclops Built for Two"),
    23: EpisodeData(23, 2, 10, "A Clone of My Own"),
    24: EpisodeData(24, 2, 11, "How Hermes Requisitioned His Groove Back"),
    25: EpisodeData(25, 2, 12, "The Deep South"),
    26: EpisodeData(26, 2, 13, "Bender Gets Made"),
    27: EpisodeData(27, 2, 14, "Mother's Day"),
    28: EpisodeData(28, 2, 15, "The Problem with Popplers"),
    29: EpisodeData(29, 2, 16, "Anthology of Interest I"),
    30: EpisodeData(30, 2, 17, "War Is the H-Word"),
    31: EpisodeData(31, 2, 18, "The Honking"),
    32: EpisodeData(32, 2, 19, "The Cryonic Woman"),
    33: EpisodeData(33, 3, 1, "Amazon Women in the Mood"),
    34: EpisodeData(34, 3, 2, "Parasites Lost"),
    35: EpisodeData(35, 3, 3, "A Tale of Two Santas"),
    36: EpisodeData(36, 3, 4, "The Luck of the Fryrish"),
    37: EpisodeData(37, 3, 5, "The Birdbot of Ice-Catraz"),
    38: EpisodeData(38, 3, 6, "Bendless Love"),
    39: EpisodeData(39, 3, 7, "The Day the Earth Stood Stupid"),
    40: EpisodeData(40, 3, 8, "That's Lobstertainment!"),
    41: EpisodeData(41, 3, 9, "The Cyber House Rules"),
    42: EpisodeData(42, 3, 10, "Where the Buggalo Roam"),
    43: EpisodeData(43, 3, 11, "Insane in the Mainframe"),
    44: EpisodeData(44, 3, 12, "The Route of All Evil"),
    45: EpisodeData(45, 3, 13, "Bendin' in the Wind"),
    46: EpisodeData(46, 3, 14, "Time Keeps On Slippin'"),
    47: EpisodeData(47, 3, 15, "I Dated a Robot"),
    48: EpisodeData(48, 3, 16, "A Leela of Her Own"),
    49: EpisodeData(49, 3, 17, "A Pharaoh to Remember"),
    50: EpisodeData(50, 3, 18, "Anthology of Interest II"),
    51: EpisodeData(51, 3, 19, "Roswell That Ends Well"),
    52: EpisodeData(52, 3, 20, "Godfellas"),
    53: EpisodeData(53, 3, 21, "Future Stock"),
    54: EpisodeData(54, 3, 22, "The 30% Iron Chef"),
    55: EpisodeData(55, 4, 1, "Kif Gets Knocked Up a Notch"),
    56: EpisodeData(56, 4, 2, "Leela's Homeworld"),
    57: EpisodeData(57, 4, 3, "Love and Rocket"),
    58: EpisodeData(58, 4, 4, "Less Than Hero"),
    59: EpisodeData(59, 4, 5, "A Taste of Freedom"),
    60: EpisodeData(60, 4, 6, "Bender Should Not Be Allowed on TV"),
    61: EpisodeData(61, 4, 7, "Jurassic Bark"),
    62: EpisodeData(62, 4, 8, "Crimes of the Hot"),
    63: EpisodeData(63, 4, 9, "Teenage Mutant Leela's Hurdles"),
    64: EpisodeData(64, 4, 10, "The Why of Fry"),
    65: EpisodeData(65, 4, 11, "Where No Fan Has Gone Before"),
    66: EpisodeData(66, 4, 12, "The Sting"),
    67: EpisodeData(67, 4, 13, "Bend Her"),
    68: EpisodeData(68, 4, 14, "Obsoletely Fabulous"),
    69: EpisodeData(69, 4, 15, "The Farnsworth Parabox"),
    70: EpisodeData(70, 4, 16, "Three Hundred Big Boys"),
    71: EpisodeData(71, 4, 17, "Spanish Fry"),
    72: EpisodeData(72, 4, 18, "The Devil's Hands Are Idle Playthings"),
    73: EpisodeData(76, 5, 1, "Bender's Big Score"),
    77: EpisodeData(80, 5, 2, "The Beast with a Billion Backs"),
    81: EpisodeData(84, 5, 3, "Bender 's Game,"),
    85: EpisodeData(88, 5, 4, "Into the Wild Green Yonder"),
    89: EpisodeData(89, 6, 1, "Rebirth"),
    90: EpisodeData(90, 6, 2, "In-A-Gadda-Da-Leela"),
    91: EpisodeData(91, 6, 3, "Attack of the Killer App"),
    92: EpisodeData(92, 6, 4, "Proposition Infinity"),
    93: EpisodeData(93, 6, 5, "The Duh-Vinci Code"),
    94: EpisodeData(94, 6, 6, "Lethal Inspection"),
    95: EpisodeData(95, 6, 7, "The Late Philip J. Fry"),
    96: EpisodeData(96, 6, 8, "That Darn Katz!"),
    97: EpisodeData(97, 6, 9, "A Clockwork Origin"),
    98: EpisodeData(98, 6, 10, "The Prisoner of Benda"),
    99: EpisodeData(99, 6, 11, "Lrrreconcilable Ndndifferences"),
    100: EpisodeData(100, 6, 12, "The Mutants Are Revolting"),
    101: EpisodeData(101, 6, 13, "The Futurama Holiday Spectacular"),
    102: EpisodeData(102, 6, 14, "The Silence of the Clamps"),
    103: EpisodeData(103, 6, 15, "Möbius Dick"),
    104: EpisodeData(104, 6, 16, "Law and Oracle"),
    105: EpisodeData(105, 6, 17, "Benderama"),
    106: EpisodeData(106, 6, 18, "The Tip of the Zoidberg"),
    107: EpisodeData(107, 6, 19, "Ghost in the Machines"),
    108: EpisodeData(108, 6, 20, "Neutopia"),
    109: EpisodeData(109, 6, 21, "Yo Leela Leela"),
    110: EpisodeData(110, 6, 22, "Fry Am the Egg Man"),
    111: EpisodeData(111, 6, 23, "All the Presidents' Heads"),
    112: EpisodeData(112, 6, 24, "Cold Warriors"),
    113: EpisodeData(113, 6, 25, "Overclockwise"),
    114: EpisodeData(114, 6, 26, "Reincarnation"),
    115: EpisodeData(115, 7, 1, "The Bots and the Bees"),
    116: EpisodeData(116, 7, 2, "A Farewell to Arms"),
    117: EpisodeData(117, 7, 3, "Decision 3012"),
    118: EpisodeData(118, 7, 4, "The Thief of Baghead"),
    119: EpisodeData(119, 7, 5, "Zapp Dingbat"),
    120: EpisodeData(120, 7, 6, "The Butterjunk Effect"),
    121: EpisodeData(121, 7, 7, "The Six Million Dollar Mon"),
    122: EpisodeData(122, 7, 8, "Fun on a Bun"),
    123: EpisodeData(123, 7, 9, "Free Will Hunting"),
    124: EpisodeData(124, 7, 10, "Near-Death Wish"),
    125: EpisodeData(125, 7, 11, "31st Century Fox"),
    126: EpisodeData(126, 7, 12, "Viva Mars Vegas"),
    127: EpisodeData(127, 7, 13, "Naturama"),
    128: EpisodeData(128, 7, 14, "Forty Percent Leadbelly"),
    129: EpisodeData(129, 7, 15, "2-D Blacktop"),
    130: EpisodeData(130, 7, 16, "T.: The Terrestrial"),
    131: EpisodeData(131, 7, 17, "Fry and Leela's Big Fling"),
    132: EpisodeData(132, 7, 18, "The Inhuman Torch"),
    133: EpisodeData(133, 7, 19, "Saturday Morning Fun Pit"),
    134: EpisodeData(134, 7, 20, "Calculon 2.0"),
    135: EpisodeData(135, 7, 21, "Assie Come Home"),
    136: EpisodeData(136, 7, 22, "Leela and the Genestalk"),
    137: EpisodeData(137, 7, 23, "Game of Tones"),
    138: EpisodeData(138, 7, 24, "Murder on the Planet Express"),
    139: EpisodeData(139, 7, 25, "Stench and Stenchibility"),
    140: EpisodeData(140, 7, 26, "Meanwhile"),
}

# File title: actual episode number.
episodes_data_from_explorer = {
    'Futurama.S01E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 1,
    'Futurama.S01E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 2,
    'Futurama.S01E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 3,
    'Futurama.S01E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 4,
    'Futurama.S01E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 5,
    'Futurama.S01E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 6,
    'Futurama.S01E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 7,
    'Futurama.S01E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 8,
    'Futurama.S01E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 9,
    'Futurama.S02E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 10,
    'Futurama.S02E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 11,
    'Futurama.S02E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 12,
    'Futurama.S02E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 13,
    'Futurama.S02E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 14,
    'Futurama.S02E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 15,
    'Futurama.S02E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 16,
    'Futurama.S02E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 17,
    'Futurama.S02E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 18,
    'Futurama.S02E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 19,
    'Futurama.S02E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 20,
    'Futurama.S02E12.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 21,
    'Futurama.S02E13.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 22,
    'Futurama.S02E15.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 23,
    'Futurama.S02E14.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 24,
    'Futurama.S02E16.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 25,
    'Futurama.S02E17.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 26,
    'Futurama.S02E19.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 27,
    'Futurama.S02E18.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 28,
    'Futurama.S02E20.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 29,
    'Futurama.S03E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 30,
    'Futurama.S03E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 31,
    'Futurama.S03E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 32,
    'Futurama.S03E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 33,
    'Futurama.S03E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 34,
    'Futurama.S04E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 35,
    'Futurama.S03E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 36,
    'Futurama.S03E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 37,
    'Futurama.S03E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 38,
    'Futurama.S03E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 39,
    'Futurama.S03E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 40,
    'Futurama.S03E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 41,
    'Futurama.S04E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 42,
    'Futurama.S03E12.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 43,
    'Futurama.S05E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 44,
    'Futurama.S03E13.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 45,
    'Futurama.S03E14.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 46,
    'Futurama.S03E15.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 47,
    'Futurama.S04E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 48,
    'Futurama.S04E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 49,
    'Futurama.S04E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 50,
    'Futurama.S04E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 51,
    'Futurama.S04E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 52,
    'Futurama.S04E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 53,
    'Futurama.S04E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 54,
    'Futurama.S05E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 55,
    'Futurama.S04E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 56,
    'Futurama.S04E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 57,
    'Futurama.S05E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 58,
    'Futurama.S05E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 59,
    'Futurama.S05E15.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 60,
    'Futurama.S05E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 61,
    'Futurama.S05E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 62,
    'Futurama.S05E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 63,
    'Futurama.S05E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 64,
    'Futurama.S04E12.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 65,
    'Futurama.S05E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 66,
    'Futurama.S05E13.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 67,
    'Futurama.S05E14.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 68,
    'Futurama.S05E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 69,
    'Futurama.S05E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 70,
    'Futurama.S05E12.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 71,
    'Futurama.S05E16.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 72,
    'Futurama.S06E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1-002.mkv': 73,
    'Futurama.S06E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1-004.mkv': 77,
    'Futurama.S06E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1-001.mkv': 81,
    'Futurama.S06E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1-003.mkv': 85,
    'Futurama.S07E01.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 89,
    'Futurama.S07E02.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 90,
    'Futurama.S07E03.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 91,
    'Futurama.S07E04.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 92,
    'Futurama.S07E05.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 93,
    'Futurama.S07E06.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 94,
    'Futurama.S07E07.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 95,
    'Futurama.S07E08.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 96,
    'Futurama.S07E09.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 97,
    'Futurama.S07E10.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 98,
    'Futurama.S07E11.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 99,
    'Futurama.S07E12.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 100,
    'Futurama.S07E13.1080p.AMZN.WEB-DL.DDP2.0.H.264-Yatogam1.mkv': 101,
    'Futurama.S08E05.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 102,
    'Futurama.S08E08.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 103,
    'Futurama.S08E04.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 104,
    'Futurama.S08E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 105,
    'Futurama.S08E10.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 106,
    'Futurama.S08E03.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 107,
    'Futurama.S08E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 108,
    'Futurama.S08E06.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 109,
    'Futurama.S08E09.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 110,
    'Futurama.S08E07.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 111,
    'Futurama.S08E11.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 112,
    'Futurama.S08E12.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 113,
    'Futurama.S08E13.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 114,
    'Futurama.S09E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 115,
    'Futurama.S09E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 116,
    'Futurama.S09E03.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 117,
    'Futurama.S09E04.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 118,
    'Futurama.S09E05.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 119,
    'Futurama.S09E06.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 120,
    'Futurama.S09E07.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 121,
    'Futurama.S09E08.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 122,
    'Futurama.S09E09.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 123,
    'Futurama.S09E10.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 124,
    'Futurama.S09E11.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 125,
    'Futurama.S09E12.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 126,
    'Futurama.S09E13.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 127,
    'Futurama.S10E01.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 128,
    'Futurama.S10E02.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 129,
    'Futurama.S10E03.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 130,
    'Futurama.S10E04.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 131,
    'Futurama.S10E05.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 132,
    'Futurama.S10E06.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 133,
    'Futurama.S10E07.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 134,
    'Futurama.S10E08.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 135,
    'Futurama.S10E09.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 136,
    'Futurama.S10E10.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 137,
    'Futurama.S10E11.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 138,
    'Futurama.S10E12.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 139,
    'Futurama.S10E13.1080p.AMZN.WEB-DL.DDP5.1.H.264-Yatogam1.mkv': 140
}

old_dir_abs_paths: {str, } = set()
for old_episode_filename, absolute_episode_id in episodes_data_from_explorer.items():
    season_padded: str = old_episode_filename.split(".")[1].split("E")[0].upper()

    if not os.path.isfile(full_path := os.path.join(SERIES_FOLDER_PATH, season_padded, old_episode_filename)):
        logging.warning(f"Not found {full_path}")
        continue

    absolute_path_to_season_folder = os.path.join(SERIES_FOLDER_PATH, season_padded)
    old_dir_abs_paths.add(absolute_path_to_season_folder)

    path_to_episode = os.path.join(absolute_path_to_season_folder, old_episode_filename)

    episode: EpisodeData = episode_data[absolute_episode_id]
    season_episode_id: str = episode.season_episode_id

    if absolute_episode_id != episode.end_id:
        absolute_episode_id: str = f"{absolute_episode_id}_{absolute_episode_id + episode.end_id - absolute_episode_id}"

    episode_padded_number: str = str(season_episode_id).zfill(2)
    sanitized_title = ''.join(filter(lambda char: char not in r'\/:*?"<>|', list(episode.title)))

    target_filename = f"{SERIES_NAME}.S{episode.season}E{episode_padded_number}.#{absolute_episode_id}.{sanitized_title}.mkv"
    sanitized_target_filename = ''.join(filter(lambda char: char not in r'\/:*?"<>|', list(target_filename)))

    new_season_padded = f"S{episode.season}"
    new_episode_local_path = os.path.join(new_season_padded, sanitized_target_filename)
    new_episode_path = os.path.join(SERIES_FOLDER_PATH, new_episode_local_path)

    if not os.path.isdir(season_dir_path := os.path.join(SERIES_FOLDER_PATH, new_season_padded)):
        logging.info(f"Creating {season_dir_path}...")
        os.mkdir(season_dir_path)

    old_episode_local_path = os.path.join(season_padded, old_episode_filename)
    old_episode_path = os.path.join(SERIES_FOLDER_PATH, old_episode_local_path)

    logging.info(f"Moving {old_episode_local_path} to {new_episode_local_path}...")
    shutil.move(old_episode_path, new_episode_path)

# Delete empty old dirs.
for dir_path in old_dir_abs_paths:
    try:
        os.rmdir(dir_path)
        logging.info(f"Deleted empty folder {dir_path}.")
    except (FileNotFoundError, OSError):
        pass
