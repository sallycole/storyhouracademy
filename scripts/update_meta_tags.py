#!/usr/bin/env python3
"""
Update meta tags for all HTML pages on Story Hour Academy.
Generates unique, accurate titles and descriptions based on page content.
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

SITE_URL = "https://www.storyhouracademy.org"
SITE_NAME = "Story Hour Academy"
OG_IMAGE = "https://www.storyhouracademy.org/assets/images/home/systematic-instruction-home.png"

UNIT_TOPICS = {
    "1": "Single-Sound Consonants",
    "2": "Consonant Digraphs", 
    "3": "Multi-Letter Vowel Phonograms",
    "4": "Vowel Letters and Their Sounds",
    "5": "Multi-Sound Consonant Letters",
    "6": "Syllable Types",
    "7": "The Schwa Sound",
    "8": "More Single-Sound Phonograms",
    "9": "More Multi-Sound Phonograms"
}

UNIT_DESCRIPTIONS = {
    "1": "Learn 16 single-sound consonant letters (b, d, f, h, j, k, l, m, n, p, qu, r, t, v, w, z) and their sounds in this free reading curriculum.",
    "2": "Learn six consonant digraphs (ck, ch, ng, sh, th, wh) that represent single sounds in this free reading curriculum.",
    "3": "Learn 19 multi-letter vowel phonograms and start blending sounds into words in this free reading curriculum.",
    "4": "Learn vowel letters a, e, i, o, u, y and the multiple sounds each can represent in this free reading curriculum.",
    "5": "Learn multi-sound consonant letters c, g, s, x and the sounds they make in different contexts.",
    "6": "Learn six syllable types: closed, open, consonant-le, r-controlled, vowel-consonant-e, and vowel team.",
    "7": "Learn about the schwa sound, the most common vowel sound in English, and identify it in words.",
    "8": "Learn nine more single-sound phonograms (tch, ph, rh, gh, gn, kn, wr, dg, aigh) for advanced reading.",
    "9": "Learn 15 more multi-sound phonograms to complete the Story Hour Academy reading curriculum."
}

LESSON_MAPPING = {
    1: ("Single-Sound Consonants Pretest", "1", "Take the pretest for single-sound consonants to identify which lessons to study."),
    2: ("Introduction to Single-Sound Consonants", "1", "Introduction to 16 single-sound consonant letters and their sounds."),
    3: ("Letter B", "1", "Learn about the letter b, its sound, and how to write it."),
    4: ("Letter D", "1", "Learn about the letter d, its sound, and how to write it."),
    5: ("Letter F", "1", "Learn about the letter f, its sound, and how to write it."),
    6: ("Letter H", "1", "Learn about the letter h, its sound, and how to write it."),
    7: ("Letter J", "1", "Learn about the letter j, its sound, and how to write it."),
    8: ("Letter K", "1", "Learn about the letter k, its sound, and how to write it."),
    9: ("Letter L", "1", "Learn about the letter l, its sound, and how to write it."),
    10: ("Letter M", "1", "Learn about the letter m, its sound, and how to write it."),
    11: ("Letter N", "1", "Learn about the letter n, its sound, and how to write it."),
    12: ("Letter P", "1", "Learn about the letter p, its sound, and how to write it."),
    13: ("Phonogram QU", "1", "Learn about the phonogram qu, its sound, and how to write it."),
    14: ("Letter R", "1", "Learn about the letter r, its sound, and how to write it."),
    15: ("Letter T", "1", "Learn about the letter t, its sound, and how to write it."),
    16: ("Letter V", "1", "Learn about the letter v, its sound, and how to write it."),
    17: ("Letter W", "1", "Learn about the letter w, its sound, and how to write it."),
    18: ("Letter Z", "1", "Learn about the letter z, its sound, and how to write it."),
    19: ("Review of Single-Sound Consonants", "1", "Review all 16 single-sound consonant letters from Unit 1."),
    20: ("Single-Sound Consonants Mastery Tests", "1", "Take mastery tests for single-sound consonants in lowercase and uppercase."),
    21: ("Consonant Digraphs Pretest", "2", "Take the pretest for consonant digraphs to identify which lessons to study."),
    22: ("Introduction to Consonant Digraphs", "2", "Introduction to six consonant digraph phonograms: ck, ch, ng, sh, th, wh."),
    23: ("Phonogram CK", "2", "Learn the digraph ck, the sound it makes, and how to write it."),
    24: ("Phonogram CH", "2", "Learn the digraph ch, the sound it makes, and how to write it."),
    25: ("Phonogram NG", "2", "Learn the digraph ng, the sound it makes, and how to write it."),
    26: ("Phonogram SH", "2", "Learn the digraph sh, the sound it makes, and how to write it."),
    27: ("Phonogram TH", "2", "Learn the digraph th, the sound it makes, and how to write it."),
    28: ("Phonogram WH", "2", "Learn the digraph wh, the sound it makes, and how to write it."),
    29: ("Review of Consonant Digraphs", "2", "Review all six consonant digraph phonograms from Unit 2."),
    30: ("Consonant Digraphs Mastery Test", "2", "Take the mastery test for consonant digraphs."),
    31: ("Multi-Letter Vowel Phonograms Pretest", "3", "Take the pretest for multi-letter vowel phonograms."),
    32: ("Introduction to Multi-Letter Vowel Phonograms", "3", "Introduction to 19 multi-letter vowel phonograms and blending."),
    33: ("Vowel Phonogram AI", "3", "Learn the vowel phonogram ai, its sound, and how to use it in words."),
    34: ("Vowel Phonogram AY", "3", "Learn the vowel phonogram ay, its sound, and how to use it in words."),
    35: ("Vowel Phonogram EIGH", "3", "Learn the vowel phonogram eigh, its sound, and how to use it in words."),
    36: ("Vowel Phonogram EE", "3", "Learn the vowel phonogram ee, its sound, and how to use it in words."),
    37: ("Vowel Phonogram IGH", "3", "Learn the vowel phonogram igh, its sound, and how to use it in words."),
    38: ("Vowel Phonogram OA", "3", "Learn the vowel phonogram oa, its sound, and how to use it in words."),
    39: ("Vowel Phonogram AU", "3", "Learn the vowel phonogram au, its sound, and how to use it in words."),
    40: ("Vowel Phonogram AW", "3", "Learn the vowel phonogram aw, its sound, and how to use it in words."),
    41: ("Vowel Phonogram OI", "3", "Learn the vowel phonogram oi, its sound, and how to use it in words."),
    42: ("Vowel Phonogram OY", "3", "Learn the vowel phonogram oy, its sound, and how to use it in words."),
    43: ("Vowel Phonogram UI", "3", "Learn the vowel phonogram ui, its sound, and how to use it in words."),
    44: ("Vowel Phonogram ER", "3", "Learn the vowel phonogram er, its sound, and how to use it in words."),
    45: ("Vowel Phonogram IR", "3", "Learn the vowel phonogram ir, its sound, and how to use it in words."),
    46: ("Vowel Phonogram UR", "3", "Learn the vowel phonogram ur, its sound, and how to use it in words."),
    47: ("Vowel Phonogram AR", "3", "Learn the vowel phonogram ar, its sound, and how to use it in words."),
    48: ("Vowel Phonograms OR and WOR", "3", "Learn the vowel phonograms or and wor, their sounds, and usage."),
    49: ("Vowel Phonogram EAR", "3", "Learn the vowel phonogram ear, its sound, and how to use it in words."),
    50: ("Vowel Phonogram OUR", "3", "Learn the vowel phonogram our, its sound, and how to use it in words."),
    51: ("Review of Multi-Letter Vowel Phonograms", "3", "Review all 19 multi-letter vowel phonograms from Unit 3."),
    52: ("Multi-Letter Vowel Phonograms Mastery Test", "3", "Take the mastery test for multi-letter vowel phonograms."),
    53: ("25 Vowel Phonograms Pretest", "4", "Take the pretest covering all 25 vowel phonograms."),
    54: ("Introduction to Vowel Letters", "4", "Learn about vowel letters and the multiple sounds they represent."),
    55: ("Letter A", "4", "Learn about the letter a and all the sounds it can represent in words."),
    56: ("Letter E", "4", "Learn about the letter e and all the sounds it can represent in words."),
    57: ("Letter I", "4", "Learn about the letter i and all the sounds it can represent in words."),
    58: ("Letter O", "4", "Learn about the letter o and all the sounds it can represent in words."),
    59: ("Letter U", "4", "Learn about the letter u and all the sounds it can represent in words."),
    60: ("Letter Y", "4", "Learn about the letter y and all the sounds it can represent in words."),
    61: ("Review of Vowel Letters", "4", "Review all vowel letters and the sounds they represent."),
    62: ("25 Vowel Phonograms Mastery Test", "4", "Take the mastery test for all 25 vowel phonograms."),
    63: ("Phonics Pretests", "5", "Take pretests for multi-sound consonant letters."),
    64: ("Introduction to Multi-Sound Consonants", "5", "Learn about consonant letters c, g, s, x and their multiple sounds."),
    65: ("Letter C", "5", "Learn the two sounds of letter c and when each sound is used."),
    66: ("Letter G", "5", "Learn the two sounds of letter g and when each sound is used."),
    67: ("Letter S", "5", "Learn the two sounds of letter s and when each sound is used."),
    68: ("Letter X", "5", "Learn the sounds of letter x and when each sound is used."),
    69: ("Review of Alphabet Letters", "5", "Review all alphabet letters and the sounds they make."),
    70: ("Phonics Mastery Tests", "5", "Take mastery tests for alphabet letters and 51 phonograms."),
    71: ("Syllable Types Pretest", "6", "Take the pretest to assess your knowledge of syllable types."),
    72: ("Introduction to Syllables", "6", "Learn about syllables and the six syllable types in English."),
    73: ("Closed Syllables", "6", "Learn about closed syllables and practice identifying them in words."),
    74: ("Open Syllables", "6", "Learn about open syllables and practice identifying them in words."),
    75: ("Consonant-LE Syllables", "6", "Learn about consonant-le syllables and practice identifying them."),
    76: ("R-Controlled Syllables", "6", "Learn about r-controlled syllables and practice identifying them."),
    77: ("Vowel-Consonant-E Syllables", "6", "Learn about vowel-consonant-e syllables and practice identifying them."),
    78: ("Vowel Team Syllables", "6", "Learn about vowel team syllables and practice identifying them."),
    79: ("Review of Syllables", "6", "Review all six syllable types from Unit 6."),
    80: ("Syllable Types Mastery Test", "6", "Take the mastery test for syllable types."),
    81: ("The Schwa Sound", "7", "Learn about the schwa sound and how to identify it in words."),
    82: ("60 Phonograms Pretest", "8", "Take the pretest for 60 phonograms."),
    83: ("Introduction to More Single-Sound Phonograms", "8", "Learn nine more single-sound phonograms for advanced reading."),
    84: ("Phonogram TCH", "8", "Learn the phonogram tch, its sound, and how to use it in words."),
    85: ("Phonogram PH", "8", "Learn the phonogram ph, its sound, and how to use it in words."),
    86: ("Phonogram RH", "8", "Learn the phonogram rh, its sound, and how to use it in words."),
    87: ("Phonogram GH", "8", "Learn the phonogram gh, its sound, and how to use it in words."),
    88: ("Phonogram GN", "8", "Learn the phonogram gn, its sound, and how to use it in words."),
    89: ("Phonogram KN", "8", "Learn the phonogram kn, its sound, and how to use it in words."),
    90: ("Phonogram WR", "8", "Learn the phonogram wr, its sound, and how to use it in words."),
    91: ("Phonogram DG", "8", "Learn the phonogram dg, its sound, and how to use it in words."),
    92: ("Phonogram AIGH", "8", "Learn the phonogram aigh, its sound, and how to use it in words."),
    93: ("Phonogram Review", "8", "Review all 60 phonograms learned so far."),
    94: ("60 Phonograms Mastery Test", "8", "Take the mastery test for 60 phonograms."),
    95: ("75 Phonograms Pretest", "9", "Take the pretest for all 75 phonograms."),
    96: ("Introduction to More Multi-Sound Phonograms", "9", "Learn 15 more multi-sound phonograms to complete the curriculum."),
    97: ("Phonogram GU", "9", "Learn the phonogram gu, its sounds, and how to use it in words."),
    98: ("Phonogram OE", "9", "Learn the phonogram oe, its sounds, and how to use it in words."),
    99: ("Phonogram OU", "9", "Learn the phonogram ou, its sounds, and how to use it in words."),
    100: ("Phonogram OW", "9", "Learn the phonogram ow, its sounds, and how to use it in words."),
    101: ("Phonogram OO", "9", "Learn the phonogram oo, its sounds, and how to use it in words."),
    102: ("Phonogram EW", "9", "Learn the phonogram ew, its sounds, and how to use it in words."),
    103: ("Phonograms EU and EUR", "9", "Learn the phonograms eu and eur, their sounds, and usage."),
    104: ("Phonogram EA", "9", "Learn the phonogram ea, its sounds, and how to use it in words."),
    105: ("Phonogram EAU", "9", "Learn the phonogram eau, its sounds, and how to use it in words."),
    106: ("Phonogram EI", "9", "Learn the phonogram ei, its sounds, and how to use it in words."),
    107: ("Phonogram EY", "9", "Learn the phonogram ey, its sounds, and how to use it in words."),
    108: ("Phonogram IE", "9", "Learn the phonogram ie, its sounds, and how to use it in words."),
    109: ("Phonogram AUGH", "9", "Learn the phonogram augh, its sounds, and how to use it in words."),
    110: ("Phonogram OUGH", "9", "Learn the phonogram ough, its many sounds, and how to use it."),
    111: ("Phonogram Review", "9", "Review all 75 phonograms from the complete curriculum."),
    112: ("75 Phonograms Mastery Test", "9", "Take the final mastery test for all 75 phonograms."),
}

PRETEST_DESCRIPTIONS = {
    1: ("Single-Sound Consonants (Lowercase)", "Pretest 16 single-sound consonant letters in lowercase: b, d, f, h, j, k, l, m, n, p, qu, r, t, v, w, z."),
    2: ("Single-Sound Consonants (Uppercase)", "Pretest 16 single-sound consonant letters in uppercase: B, D, F, H, J, K, L, M, N, P, Qu, R, T, V, W, Z."),
    3: ("Consonants and Consonant Digraphs", "Pretest 21 single-sound consonants and consonant digraphs including ch, ng, sh, th, wh."),
    4: ("Multi-Letter Vowel Phonograms", "Pretest multi-letter vowel phonograms: ai, ay, eigh, ar, au, aw, ear, ee, er, ir, ur, igh, oa, oi, oy, or, our, ui, wor."),
    5: ("25 Vowel Phonograms", "Pretest 25 vowel phonograms including single vowel letters and multi-letter vowel teams."),
    6: ("Alphabet Letters and Sounds", "Pretest all 26 alphabet letters (a through z) and their associated sounds."),
    7: ("51 Phonograms", "Pretest 51 phonograms: all alphabet letters plus consonant digraphs and vowel phonograms."),
    8: ("Syllable Types", "Pretest identifying the six syllable types across 36 words."),
    9: ("60 Phonograms", "Pretest 60 phonograms including tch, ph, gh, gn, kn, wr, rh, dg, aigh."),
    10: ("75 Phonograms", "Pretest all 75 phonograms from the complete Story Hour Academy curriculum."),
}

TEST_DESCRIPTIONS = {
    1: ("Single-Sound Consonants (Lowercase)", "Mastery test for 16 single-sound consonant letters in lowercase."),
    2: ("Single-Sound Consonants (Uppercase)", "Mastery test for 16 single-sound consonant letters in uppercase."),
    3: ("Consonants and Consonant Digraphs", "Mastery test for 21 single-sound consonants and consonant digraphs."),
    4: ("Multi-Letter Vowel Phonograms", "Mastery test for multi-letter vowel phonograms."),
    5: ("25 Vowel Phonograms", "Mastery test for 25 vowel phonograms."),
    6: ("Alphabet Letters and Sounds", "Mastery test for all 26 alphabet letters and their sounds."),
    7: ("51 Phonograms", "Mastery test for 51 phonograms."),
    8: ("Syllable Types", "Mastery test for identifying the six syllable types."),
    9: ("60 Phonograms", "Mastery test for 60 phonograms."),
    10: ("75 Phonograms", "Mastery test for all 75 phonograms from the complete curriculum."),
}

GAME_DESCRIPTIONS = {
    1: ("Letter B Sound Game", "Interactive game to practice identifying the letter b and its sound."),
    2: ("Letter D Sound Game", "Interactive game to practice identifying the letter d and its sound."),
    3: ("Letter F Sound Game", "Interactive game to practice identifying the letter f and its sound."),
    4: ("Letter H Sound Game", "Interactive game to practice identifying the letter h and its sound."),
    5: ("Letter J Sound Game", "Interactive game to practice identifying the letter j and its sound."),
    6: ("Letter K Sound Game", "Interactive game to practice identifying the letter k and its sound."),
    7: ("Letter L Sound Game", "Interactive game to practice identifying the letter l and its sound."),
    8: ("Letter M Sound Game", "Interactive game to practice identifying the letter m and its sound."),
    9: ("Letter N Sound Game", "Interactive game to practice identifying the letter n and its sound."),
    10: ("Letter P Sound Game", "Interactive game to practice identifying the letter p and its sound."),
    11: ("Phonogram QU Sound Game", "Interactive game to practice identifying the phonogram qu and its sound."),
    12: ("Letter R Sound Game", "Interactive game to practice identifying the letter r and its sound."),
    13: ("Letter T Sound Game", "Interactive game to practice identifying the letter t and its sound."),
    14: ("Letter V Sound Game", "Interactive game to practice identifying the letter v and its sound."),
    15: ("Letter W Sound Game", "Interactive game to practice identifying the letter w and its sound."),
    16: ("Letter Z Sound Game", "Interactive game to practice identifying the letter z and its sound."),
    17: ("Phonogram CK Sound Game", "Interactive game to practice identifying the ck digraph and its sound."),
    18: ("Phonogram CH Sound Game", "Interactive game to practice identifying the ch digraph and its sound."),
    19: ("Phonogram NG Sound Game", "Interactive game to practice identifying the ng digraph and its sound."),
    20: ("Phonogram SH Sound Game", "Interactive game to practice identifying the sh digraph and its sound."),
    21: ("Phonogram TH Sound Game", "Interactive game to practice identifying the th digraph and its sound."),
    22: ("Phonogram WH Sound Game", "Interactive game to practice identifying the wh digraph and its sound."),
    23: ("Phonogram AI Spelling", "Interactive spelling exercise for words with the ai phonogram."),
    24: ("Phonogram AY Spelling", "Interactive spelling exercise for words with the ay phonogram."),
    25: ("Phonogram EIGH Spelling", "Interactive spelling exercise for words with the eigh phonogram."),
    26: ("Phonogram EE Spelling", "Interactive spelling exercise for words with the ee phonogram."),
    27: ("Phonogram IGH Spelling", "Interactive spelling exercise for words with the igh phonogram."),
    28: ("Phonogram OA Spelling", "Interactive spelling exercise for words with the oa phonogram."),
    29: ("Phonogram AU Spelling", "Interactive spelling exercise for words with the au phonogram."),
    30: ("Phonogram AW Spelling", "Interactive spelling exercise for words with the aw phonogram."),
    31: ("Phonogram OI Spelling", "Interactive spelling exercise for words with the oi phonogram."),
    32: ("Phonogram OY Spelling", "Interactive spelling exercise for words with the oy phonogram."),
    33: ("Phonogram UI Spelling", "Interactive spelling exercise for words with the ui phonogram."),
    34: ("R-Controlled Vowel Spelling", "Interactive spelling exercise for words with er, ir, ur phonograms."),
    35: ("Phonogram AR Spelling", "Interactive spelling exercise for words with the ar phonogram."),
    36: ("Phonogram OR Spelling", "Interactive spelling exercise for words with the or and wor phonograms."),
    37: ("Phonogram EAR Spelling", "Interactive spelling exercise for words with the ear phonogram."),
    38: ("Phonogram OUR Spelling", "Interactive spelling exercise for words with the our phonogram."),
    39: ("Vowel Phonograms Review", "Interactive spelling review for all multi-letter vowel phonograms."),
}


def get_video_info(video_num: str) -> Tuple[str, str]:
    """Get title and description for video pages based on video number."""
    video_int = int(video_num.replace('a', '').replace('b', ''))
    
    if video_int <= 2 or video_num in ['2a', '2b']:
        return ("Introduction to Single-Sound Consonants", "Video lesson introducing single-sound consonant letters and their sounds.")
    elif video_int <= 18:
        letters = ['', '', '', 'b', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'qu', 'r', 't', 'v', 'w', 'z']
        if video_int < len(letters):
            letter = letters[video_int].upper()
            return (f"Letter {letter} Video Lesson", f"Video lesson teaching the letter {letter.lower()}, its sound, and how to write it.")
    elif video_int <= 20:
        return ("Single-Sound Consonants Review", "Video reviewing all 16 single-sound consonant letters.")
    elif video_int <= 30:
        digraphs = ['', 'ck', 'ch', 'ng', 'sh', 'th', 'wh']
        idx = video_int - 22
        if 0 < idx < len(digraphs):
            dg = digraphs[idx].upper()
            return (f"Phonogram {dg} Video Lesson", f"Video lesson teaching the {dg.lower()} digraph, its sound, and how to write it.")
        return ("Consonant Digraphs Video", "Video lesson about consonant digraph phonograms.")
    elif video_int <= 52:
        return ("Vowel Phonograms Video", "Video lesson teaching multi-letter vowel phonograms and blending.")
    elif video_int <= 62:
        return ("Vowel Letters Video", "Video lesson about vowel letters and the sounds they represent.")
    elif video_int <= 70:
        return ("Multi-Sound Consonants Video", "Video lesson about consonant letters with multiple sounds.")
    elif video_int <= 80:
        return ("Syllable Types Video", "Video lesson about the six syllable types in English.")
    elif video_int <= 94:
        return ("Advanced Phonograms Video", "Video lesson teaching additional single-sound phonograms.")
    else:
        return ("Multi-Sound Phonograms Video", "Video lesson teaching additional multi-sound phonograms.")


def get_canonical_url(filepath: str) -> str:
    """Get the canonical URL for a file."""
    filename = os.path.basename(filepath)
    if filename == 'index.html':
        return f"{SITE_URL}/"
    else:
        name = filename.replace('.html', '')
        return f"{SITE_URL}/{name}"


def generate_meta_tags(filepath: str) -> Dict[str, str]:
    """Generate appropriate meta tags for a given HTML file."""
    filename = os.path.basename(filepath)
    name = filename.replace('.html', '')
    canonical_url = get_canonical_url(filepath)
    
    title = ""
    description = ""
    noindex = False
    
    if filename == 'index.html':
        title = "Story Hour Academy | Free Online Reading Curriculum for Kids"
        description = "Free, comprehensive reading curriculum with 112 lessons. Includes pretests, interactive exercises, decodable reading, classic literature, and mastery tests."
    
    elif filename == 'tests.html':
        title = "Pretests and Mastery Tests | Story Hour Academy"
        description = "Diagnostic pretests and mastery tests for phonics and reading skills. Identify where students need help with consonants, vowels, phonograms, and syllable types."
    
    elif filename == 'about.html':
        title = "About Story Hour Academy | Our Story and Mission"
        description = "Learn how Story Hour Academy began as a solution for teaching children to read. Free curriculum created by a parent for parents and educators."
    
    elif filename == 'book-list.html':
        title = "Book List | Story Hour Academy"
        description = "Complete list of classic literature used in the Story Hour Academy reading curriculum, sortable by title, author, or publication date."
    
    elif filename == 'structure.html':
        title = "Curriculum Structure | Story Hour Academy"
        description = "Overview of Story Hour Academy's 9 units and 112 lessons covering phonograms, consonants, vowels, digraphs, syllable types, and more."
    
    elif filename == 'contact.html':
        title = "Contact Story Hour Academy"
        description = "Contact Story Hour Academy to share your experience with our free reading curriculum or provide feedback."
    
    elif filename == 'complete.html':
        title = "Curriculum Complete | Story Hour Academy"
        description = "Congratulations on completing the Story Hour Academy reading curriculum! Explore next steps for continued learning."
        noindex = True
    
    elif filename == 'thanks.html':
        title = "Thank You | Story Hour Academy"
        description = "Thank you for contacting Story Hour Academy."
        noindex = True
    
    elif filename == '404.html':
        title = "Page Not Found | Story Hour Academy"
        description = "The page you requested could not be found on Story Hour Academy."
        noindex = True
    
    elif filename == 'list.html':
        title = "Lesson List | Story Hour Academy"
        description = "Complete list of all 112 lessons in the Story Hour Academy free reading curriculum."
    
    elif filename == 'audio-1.html':
        title = "Audio Lesson: Consonant Sounds | Story Hour Academy"
        description = "Audio lesson for learning single-sound consonant letters and their pronunciation."
    
    elif name.startswith('unit-'):
        unit_num = name.replace('unit-', '')
        if unit_num in UNIT_TOPICS:
            topic = UNIT_TOPICS[unit_num]
            title = f"Unit {unit_num}: {topic} | Story Hour Academy"
            description = UNIT_DESCRIPTIONS.get(unit_num, f"Learn {topic.lower()} in this free reading curriculum unit.")
    
    elif name.startswith('lesson-'):
        lesson_num = int(name.replace('lesson-', ''))
        if lesson_num in LESSON_MAPPING:
            topic, unit, desc = LESSON_MAPPING[lesson_num]
            title = f"Lesson {lesson_num}: {topic} | Story Hour Academy"
            description = desc
    
    elif name == 'lesson1':
        title = "Lesson 1: Single-Sound Consonants Pretest | Story Hour Academy"
        description = "Take the pretest for single-sound consonants to identify which lessons to study."
    
    elif name.startswith('pretest-'):
        pretest_num = int(name.replace('pretest-', ''))
        if pretest_num in PRETEST_DESCRIPTIONS:
            topic, desc = PRETEST_DESCRIPTIONS[pretest_num]
            title = f"Pretest: {topic} | Story Hour Academy"
            description = desc
    
    elif name.startswith('test-'):
        test_num = int(name.replace('test-', ''))
        if test_num in TEST_DESCRIPTIONS:
            topic, desc = TEST_DESCRIPTIONS[test_num]
            title = f"Mastery Test: {topic} | Story Hour Academy"
            description = desc
    
    elif name.startswith('quiz'):
        quiz_num = int(name.replace('quiz', ''))
        if quiz_num in TEST_DESCRIPTIONS:
            topic, desc = TEST_DESCRIPTIONS[quiz_num]
            title = f"Quiz: {topic} | Story Hour Academy"
            description = f"Interactive quiz for {topic.lower()}."
    
    elif name.startswith('game-') or name.startswith('game'):
        game_num_str = name.replace('game-', '').replace('game', '')
        try:
            game_num = int(game_num_str)
            if game_num in GAME_DESCRIPTIONS:
                topic, desc = GAME_DESCRIPTIONS[game_num]
                title = f"{topic} | Story Hour Academy"
                description = desc
            else:
                title = f"Reading Game {game_num} | Story Hour Academy"
                description = f"Interactive phonics game to practice reading skills."
        except ValueError:
            title = f"Reading Game | Story Hour Academy"
            description = f"Interactive phonics game to practice reading skills."
    
    elif name.startswith('video-'):
        video_num = name.replace('video-', '')
        topic, desc = get_video_info(video_num)
        title = f"{topic} | Story Hour Academy"
        description = desc
    
    else:
        title = f"{name.replace('-', ' ').title()} | Story Hour Academy"
        description = f"Free reading lesson from Story Hour Academy's comprehensive curriculum."
    
    return {
        'title': title,
        'description': description,
        'canonical': canonical_url,
        'noindex': noindex,
        'og_title': title,
        'og_description': description,
        'og_url': canonical_url,
        'og_type': 'website',
        'og_site_name': SITE_NAME,
        'og_image': OG_IMAGE,
        'twitter_card': 'summary_large_image',
        'twitter_title': title,
        'twitter_description': description,
    }


def update_html_file(filepath: str) -> bool:
    """Update meta tags in an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    meta = generate_meta_tags(filepath)
    original_content = content
    
    # Skip template files
    if 'template' in filepath.lower():
        return False
    
    # Ensure html lang="en"
    content = re.sub(r'<html\s*>', '<html lang="en">', content)
    content = re.sub(r'<html\s+lang="[^"]*">', '<html lang="en">', content)
    
    # Update title
    if '<title>' in content:
        content = re.sub(r'<title>[^<]*</title>', f'<title>{meta["title"]}</title>', content)
    else:
        content = content.replace('</head>', f'    <title>{meta["title"]}</title>\n</head>')
    
    # Update or add meta description
    if 'name="description"' in content:
        content = re.sub(
            r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
            f'<meta name="description" content="{meta["description"]}">',
            content
        )
    else:
        # Add after viewport
        content = re.sub(
            r'(<meta\s+name="viewport"[^>]*>)',
            f'\\1\n    <meta name="description" content="{meta["description"]}">',
            content
        )
    
    # Remove any stray noindex tags from public pages (keep only for 404, complete, thanks)
    filename = os.path.basename(filepath)
    if not meta['noindex']:
        content = re.sub(r'\s*<meta\s+name="robots"\s+content="[^"]*noindex[^"]*"\s*/?>\s*', '\n', content)
    elif meta['noindex'] and 'name="robots"' not in content:
        content = re.sub(
            r'(<meta\s+name="description"[^>]*>)',
            f'\\1\n    <meta name="robots" content="noindex">',
            content
        )
    
    # Add/update Open Graph tags
    og_tags = f'''
    <!-- Open Graph -->
    <meta property="og:title" content="{meta['og_title']}">
    <meta property="og:description" content="{meta['og_description']}">
    <meta property="og:url" content="{meta['og_url']}">
    <meta property="og:type" content="{meta['og_type']}">
    <meta property="og:site_name" content="{meta['og_site_name']}">
    <meta property="og:image" content="{meta['og_image']}">'''
    
    twitter_tags = f'''
    <!-- Twitter Card -->
    <meta name="twitter:card" content="{meta['twitter_card']}">
    <meta name="twitter:title" content="{meta['twitter_title']}">
    <meta name="twitter:description" content="{meta['twitter_description']}">'''
    
    # Remove existing OG and Twitter tags
    content = re.sub(r'\s*<!-- Open Graph -->\s*', '\n', content)
    content = re.sub(r'\s*<meta\s+property="og:[^"]*"\s+content="[^"]*"\s*/?>\s*', '', content)
    content = re.sub(r'\s*<!-- Twitter Card -->\s*', '\n', content)
    content = re.sub(r'\s*<meta\s+name="twitter:[^"]*"\s+content="[^"]*"\s*/?>\s*', '', content)
    
    # Add OG and Twitter tags before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'{og_tags}\n{twitter_tags}\n</head>')
    
    # Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Main function to update all HTML files."""
    html_files = list(Path('.').glob('*.html'))
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        filename = str(filepath)
        if 'template' in filename.lower():
            skipped += 1
            continue
        
        if update_html_file(filename):
            print(f"Updated: {filename}")
            updated += 1
        else:
            print(f"No changes: {filename}")
    
    print(f"\nSummary: {updated} files updated, {skipped} templates skipped")


if __name__ == '__main__':
    main()
