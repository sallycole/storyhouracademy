#!/usr/bin/env python3
"""
Fix remaining meta tag issues: duplicate video titles/descriptions and short descriptions.
"""

import os
import re
from pathlib import Path

SITE_URL = "https://www.storyhouracademy.org"
SITE_NAME = "Story Hour Academy"
OG_IMAGE = "https://www.storyhouracademy.org/assets/images/home/systematic-instruction-home.png"

VIDEO_SPECIFIC = {
    "2a": ("Single-Sound Consonants Overview Part 1", "Video introducing the first eight single-sound consonant letters: b, d, f, h, j, k, l, and m."),
    "2b": ("Single-Sound Consonants Overview Part 2", "Video introducing the second eight single-sound consonant letters: n, p, qu, r, t, v, w, and z."),
    "3": ("Letter B Video Lesson", "Video teaching the letter b, its sound, how to write it, and words that contain it."),
    "4": ("Letter D Video Lesson", "Video teaching the letter d, its sound, how to write it, and words that contain it."),
    "5": ("Letter F Video Lesson", "Video teaching the letter f, its sound, how to write it, and words that contain it."),
    "6": ("Letter H Video Lesson", "Video teaching the letter h, its sound, how to write it, and words that contain it."),
    "7": ("Letter J Video Lesson", "Video teaching the letter j, its sound, how to write it, and words that contain it."),
    "8": ("Letter K Video Lesson", "Video teaching the letter k, its sound, how to write it, and words that contain it."),
    "9": ("Letter L Video Lesson", "Video teaching the letter l, its sound, how to write it, and words that contain it."),
    "10": ("Letter M Video Lesson", "Video teaching the letter m, its sound, how to write it, and words that contain it."),
    "11": ("Letter N Video Lesson", "Video teaching the letter n, its sound, how to write it, and words that contain it."),
    "12": ("Letter P Video Lesson", "Video teaching the letter p, its sound, how to write it, and words that contain it."),
    "13": ("Phonogram QU Video Lesson", "Video teaching the phonogram qu, its sound, how to write it, and words that contain it."),
    "14": ("Letter R Video Lesson", "Video teaching the letter r, its sound, how to write it, and words that contain it."),
    "15": ("Letter T Video Lesson", "Video teaching the letter t, its sound, how to write it, and words that contain it."),
    "16": ("Letter V Video Lesson", "Video teaching the letter v, its sound, how to write it, and words that contain it."),
    "17": ("Letter W Video Lesson", "Video teaching the letter w, its sound, how to write it, and words that contain it."),
    "18": ("Letter Z Video Lesson", "Video teaching the letter z, its sound, how to write it, and words that contain it."),
    "19": ("Single-Sound Consonants Review Part 1", "Video reviewing the first eight single-sound consonant letters learned in Unit 1."),
    "20": ("Single-Sound Consonants Review Part 2", "Video reviewing the second eight single-sound consonant letters learned in Unit 1."),
    "21": ("Consonant Digraphs Introduction Part 1", "Video introducing the first three consonant digraphs: ck, ch, and ng."),
    "22": ("Consonant Digraphs Introduction Part 2", "Video introducing the remaining consonant digraphs: sh, th, and wh."),
    "23": ("Phonogram CK Video Lesson", "Video teaching the ck digraph, its sound, how to write it, and words that contain it."),
    "24": ("Phonogram CH Video Lesson", "Video teaching the ch digraph, its sound, how to write it, and words that contain it."),
    "25": ("Phonogram NG Video Lesson", "Video teaching the ng digraph, its sound, how to write it, and words that contain it."),
    "26": ("Phonogram SH Video Lesson", "Video teaching the sh digraph, its sound, how to write it, and words that contain it."),
    "27": ("Phonogram TH Video Lesson", "Video teaching the th digraph, its sound, how to write it, and words that contain it."),
    "28": ("Phonogram WH Video Lesson", "Video teaching the wh digraph, its sound, how to write it, and words that contain it."),
    "29": ("Consonant Digraphs Review Part 1", "Video reviewing the first three consonant digraphs: ck, ch, and ng."),
    "30": ("Consonant Digraphs Review Part 2", "Video reviewing the remaining consonant digraphs: sh, th, and wh."),
    "31": ("Multi-Letter Vowel Phonograms Introduction", "Video introducing 19 multi-letter vowel phonograms and the concept of blending sounds."),
    "32": ("Phonogram AI Video Lesson", "Video teaching the ai vowel phonogram, its sound, and words like rain, train, and mail."),
    "33": ("Phonogram AY Video Lesson", "Video teaching the ay vowel phonogram, its sound, and words like day, play, and say."),
    "34": ("Phonogram EIGH Video Lesson", "Video teaching the eigh vowel phonogram, its sound, and words like eight and weigh."),
    "35": ("Phonogram EE Video Lesson", "Video teaching the ee vowel phonogram, its sound, and words like see, tree, and feet."),
    "36": ("Phonogram IGH Video Lesson", "Video teaching the igh vowel phonogram, its sound, and words like night, light, and high."),
    "37": ("Phonogram OA Video Lesson", "Video teaching the oa vowel phonogram, its sound, and words like boat, coat, and road."),
    "38": ("Phonogram AU Video Lesson", "Video teaching the au vowel phonogram, its sound, and words like cause and pause."),
    "39": ("Phonogram AW Video Lesson", "Video teaching the aw vowel phonogram, its sound, and words like saw, draw, and law."),
    "40": ("Phonogram OI Video Lesson", "Video teaching the oi vowel phonogram, its sound, and words like oil, coin, and join."),
    "41": ("Phonogram OY Video Lesson", "Video teaching the oy vowel phonogram, its sound, and words like boy, toy, and joy."),
    "42": ("Phonogram UI Video Lesson", "Video teaching the ui vowel phonogram, its sound, and words like fruit and suit."),
    "43": ("Phonogram ER Video Lesson", "Video teaching the er vowel phonogram, its sound, and words like her, fern, and term."),
    "44": ("Phonogram IR Video Lesson", "Video teaching the ir vowel phonogram, its sound, and words like bird, girl, and first."),
    "45": ("Phonogram UR Video Lesson", "Video teaching the ur vowel phonogram, its sound, and words like fur, burn, and turn."),
    "46": ("Phonogram AR Video Lesson", "Video teaching the ar vowel phonogram, its sound, and words like car, star, and far."),
    "47": ("Phonograms OR and WOR Video", "Video teaching the or and wor vowel phonograms, their sounds, and example words."),
    "48": ("Phonogram EAR Video Lesson", "Video teaching the ear vowel phonogram, its sound, and words like ear, hear, and near."),
    "49": ("Phonogram OUR Video Lesson", "Video teaching the our vowel phonogram, its sound, and words like our, four, and pour."),
    "50": ("Multi-Letter Vowel Phonograms Review Part 1", "Video reviewing the first ten multi-letter vowel phonograms from Unit 3."),
    "51": ("Multi-Letter Vowel Phonograms Review Part 2", "Video reviewing the remaining multi-letter vowel phonograms from Unit 3."),
    "52": ("Vowel Phonograms Mastery Test Video", "Video introducing the mastery test for all 19 multi-letter vowel phonograms."),
    "53": ("Vowel Letters Introduction Video", "Video introducing the six vowel letters and the multiple sounds they represent."),
    "54": ("Letter A Vowel Sounds Video", "Video teaching letter a and all the sounds it can make in different words."),
    "55": ("Letter E Vowel Sounds Video", "Video teaching letter e and all the sounds it can make in different words."),
    "56": ("Letter I Vowel Sounds Video", "Video teaching letter i and all the sounds it can make in different words."),
    "57": ("Letter O Vowel Sounds Video", "Video teaching letter o and all the sounds it can make in different words."),
    "58": ("Letter U Vowel Sounds Video", "Video teaching letter u and all the sounds it can make in different words."),
    "59": ("Letter Y Vowel Sounds Video", "Video teaching letter y and all the sounds it can make in different words."),
    "60": ("Vowel Letters Review Part 1", "Video reviewing vowel letters a, e, and i and all the sounds they represent."),
    "61": ("Vowel Letters Review Part 2", "Video reviewing vowel letters o, u, and y and all the sounds they represent."),
    "61b": ("Vowel Letters Additional Practice", "Additional video practice for vowel letters and the sounds they represent."),
    "62": ("25 Vowel Phonograms Test Video", "Video introducing the mastery test for all 25 vowel phonograms."),
    "63": ("Multi-Sound Consonants Introduction", "Video introducing consonant letters c, g, s, and x that have multiple sounds."),
    "64": ("Letter C Two Sounds Video", "Video teaching the two sounds of letter c: hard c as in cat and soft c as in city."),
    "65": ("Letter G Two Sounds Video", "Video teaching the two sounds of letter g: hard g as in go and soft g as in gem."),
    "66": ("Letter S Two Sounds Video", "Video teaching the two sounds of letter s: s as in sun and z sound as in is."),
    "67": ("Letter X Sounds Video", "Video teaching the sounds of letter x in different word positions."),
    "68": ("Alphabet Letters Review Part 1", "Video reviewing all alphabet letters A through M and the sounds they make."),
    "69": ("Alphabet Letters Review Part 2", "Video reviewing all alphabet letters N through Z and the sounds they make."),
    "70": ("51 Phonograms Test Video", "Video introducing the mastery test for all 51 phonograms learned so far."),
    "71": ("Syllable Types Introduction Video", "Video introducing the six syllable types used in English words."),
    "72": ("Closed Syllables Video Lesson", "Video teaching closed syllables where a vowel is followed by a consonant."),
    "73": ("Open Syllables Video Lesson", "Video teaching open syllables where a vowel comes at the end."),
    "74": ("Consonant-LE Syllables Video", "Video teaching consonant-le syllables found at the end of words like table."),
    "75": ("R-Controlled Syllables Video", "Video teaching r-controlled syllables where a vowel is followed by r."),
    "76": ("Vowel-Consonant-E Syllables Video", "Video teaching VCE syllables with silent e that makes the vowel long."),
    "77": ("Vowel Team Syllables Video", "Video teaching vowel team syllables with two vowels making one sound."),
    "78": ("Syllable Types Review Part 1", "Video reviewing closed, open, and consonant-le syllable types."),
    "79": ("Syllable Types Review Part 2", "Video reviewing r-controlled, VCE, and vowel team syllable types."),
    "80": ("Syllable Types Mastery Test Video", "Video introducing the mastery test for identifying all six syllable types."),
    "81": ("Schwa Sound Video Lesson", "Video teaching the schwa sound, the most common vowel sound in English."),
    "82": ("More Phonograms Introduction Video", "Video introducing nine additional single-sound phonograms for advanced reading."),
    "83": ("Phonogram TCH Video Lesson", "Video teaching the tch phonogram, its sound, and words like watch and catch."),
    "84": ("Phonogram PH Video Lesson", "Video teaching the ph phonogram, its sound, and words like phone and graph."),
    "85": ("Phonogram RH Video Lesson", "Video teaching the rh phonogram, its sound, and words like rhyme and rhythm."),
    "86": ("Phonogram GH Video Lesson", "Video teaching the gh phonogram, its sounds, and example words."),
    "87": ("Phonogram GN Video Lesson", "Video teaching the gn phonogram, its sound, and words like gnat and sign."),
    "88": ("Phonogram KN Video Lesson", "Video teaching the kn phonogram, its sound, and words like knee and know."),
    "89": ("Phonogram WR Video Lesson", "Video teaching the wr phonogram, its sound, and words like write and wrong."),
    "90": ("Phonogram DG Video Lesson", "Video teaching the dg phonogram, its sound, and words like edge and badge."),
    "91": ("Phonogram AIGH Video Lesson", "Video teaching the aigh phonogram, its sound, and words like straight."),
    "92": ("60 Phonograms Review Part 1", "Video reviewing the first 30 phonograms from Units 1 through 8."),
    "93": ("60 Phonograms Review Part 2", "Video reviewing the remaining 30 phonograms from Units 1 through 8."),
    "94": ("60 Phonograms Mastery Test Video", "Video introducing the mastery test for all 60 phonograms learned."),
    "95": ("Final Phonograms Introduction Video", "Video introducing the final 15 multi-sound phonograms in the curriculum."),
    "96": ("Phonogram GU Video Lesson", "Video teaching the gu phonogram, its sounds, and words like guess and guard."),
    "97": ("Phonogram OE Video Lesson", "Video teaching the oe phonogram, its sounds, and words like toe and poem."),
    "98": ("Phonogram OU Video Lesson", "Video teaching the ou phonogram, its four sounds, and example words."),
    "99": ("Phonogram OW Video Lesson", "Video teaching the ow phonogram, its two sounds, and words like cow and snow."),
    "100": ("Phonogram OO Video Lesson", "Video teaching the oo phonogram, its two sounds, and words like moon and book."),
    "101": ("Phonogram EW Video Lesson", "Video teaching the ew phonogram, its sounds, and words like new and few."),
    "102": ("Phonograms EU and EUR Video", "Video teaching the eu and eur phonograms, their sounds, and example words."),
    "103": ("Phonogram EA Video Lesson", "Video teaching the ea phonogram, its three sounds, and words like eat and head."),
    "104": ("75 Phonograms Review Video", "Video reviewing all 75 phonograms from the complete Story Hour Academy curriculum."),
    "105": ("75 Phonograms Mastery Test Video", "Video introducing the final mastery test for all 75 phonograms in the curriculum."),
}

SHORT_DESC_FIXES = {
    "test-7.html": "Mastery test for all 51 phonograms including alphabet letters, consonant digraphs, and vowel phonograms.",
    "test-9.html": "Mastery test for 60 phonograms including tch, ph, gh, gn, kn, wr, rh, dg, and aigh phonograms.",
    "test-5.html": "Mastery test covering 25 vowel phonograms including single vowels and multi-letter vowel teams.",
    "test-4.html": "Mastery test for multi-letter vowel phonograms including ai, ay, ee, igh, oa, and r-controlled vowels.",
    "lesson-82.html": "Take the pretest for 60 phonograms to assess knowledge of all phonograms learned in Units 1 through 8.",
    "lesson-95.html": "Take the pretest for all 75 phonograms from the complete Story Hour Academy reading curriculum.",
    "lesson-93.html": "Review all 60 phonograms learned in Units 1 through 8 before taking the mastery test.",
    "lesson-94.html": "Take the mastery test to demonstrate knowledge of all 60 phonograms from the curriculum.",
    "lesson-80.html": "Take the mastery test to demonstrate your knowledge of the six syllable types.",
    "lesson-79.html": "Review all six syllable types before taking the Unit 6 mastery test.",
    "lesson-30.html": "Take the mastery test to demonstrate your knowledge of consonant digraphs.",
    "lesson-63.html": "Take pretests for multi-sound consonant letters c, g, s, and x to identify areas for study.",
    "quiz10.html": "Interactive quiz testing knowledge of all 75 phonograms from the complete curriculum.",
    "quiz7.html": "Interactive quiz testing knowledge of 51 phonograms including letters and digraphs.",
    "quiz9.html": "Interactive quiz testing knowledge of 60 phonograms including advanced phonograms.",
    "quiz8.html": "Interactive quiz testing the ability to identify the six syllable types in words.",
    "quiz5.html": "Interactive quiz testing knowledge of all 25 vowel phonograms learned in the curriculum.",
    "quiz6.html": "Interactive quiz testing all 26 alphabet letters and their associated sounds.",
    "thanks.html": "Thank you for contacting Story Hour Academy. We appreciate your feedback about our free reading curriculum.",
    "contact.html": "Contact Story Hour Academy to share your experience with our free reading curriculum or provide feedback.",
}

LESSON_DUPLICATE_FIXES = {
    "lesson1.html": ("Lesson 1: Unit 1 Pretest", "Take the Unit 1 pretest for single-sound consonants to identify which lessons to study."),
    "game-1.html": ("Letter B Sound Game Level 1", "Interactive game Level 1 to practice identifying the letter b and its sound."),
}


def update_html_file(filepath: str, new_title: str, new_desc: str) -> bool:
    """Update title and description in an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Update title
    content = re.sub(r'<title>[^<]*</title>', f'<title>{new_title} | Story Hour Academy</title>', content)
    
    # Update meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{new_desc}">',
        content
    )
    
    # Update OG tags
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{new_title} | Story Hour Academy">',
        content
    )
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{new_desc}">',
        content
    )
    
    # Update Twitter tags
    content = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{new_title} | Story Hour Academy">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{new_desc}">',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    """Fix remaining issues."""
    updated = 0
    
    # Fix video pages
    for video_num, (title, desc) in VIDEO_SPECIFIC.items():
        filepath = f"video-{video_num}.html"
        if os.path.exists(filepath):
            if update_html_file(filepath, title, desc):
                print(f"Updated: {filepath}")
                updated += 1
    
    # Fix short descriptions
    for filepath, desc in SHORT_DESC_FIXES.items():
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract current title
            title_match = re.search(r'<title>([^<]*)</title>', content)
            if title_match:
                current_title = title_match.group(1).replace(' | Story Hour Academy', '')
                
                # Update description only
                content = re.sub(
                    r'<meta name="description" content="[^"]*">',
                    f'<meta name="description" content="{desc}">',
                    content
                )
                content = re.sub(
                    r'<meta property="og:description" content="[^"]*">',
                    f'<meta property="og:description" content="{desc}">',
                    content
                )
                content = re.sub(
                    r'<meta name="twitter:description" content="[^"]*">',
                    f'<meta name="twitter:description" content="{desc}">',
                    content
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed short desc: {filepath}")
                updated += 1
    
    # Fix lesson1.html and game-1.html duplicates
    for filepath, (title, desc) in LESSON_DUPLICATE_FIXES.items():
        if os.path.exists(filepath):
            if update_html_file(filepath, title, desc):
                print(f"Fixed duplicate: {filepath}")
                updated += 1
    
    # Fix contact.html title
    if os.path.exists("contact.html"):
        with open("contact.html", 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(
            r'<title>[^<]*</title>',
            '<title>Contact Us | Story Hour Academy</title>',
            content
        )
        content = re.sub(
            r'<meta property="og:title" content="[^"]*">',
            '<meta property="og:title" content="Contact Us | Story Hour Academy">',
            content
        )
        content = re.sub(
            r'<meta name="twitter:title" content="[^"]*">',
            '<meta name="twitter:title" content="Contact Us | Story Hour Academy">',
            content
        )
        
        with open("contact.html", 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed: contact.html title")
        updated += 1
    
    print(f"\nTotal files updated: {updated}")


if __name__ == '__main__':
    main()
