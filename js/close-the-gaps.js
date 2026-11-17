/*
 * Close the Gaps
 *
 * Builds a custom Story Hour Academy curriculum file from the items a
 * student missed on a pretest or mastery test. The file uses the Lesson
 * Hollow curriculum format (a comma-separated values file) so a family can
 * import it at https://lessonhollow.com.
 *
 * Everything runs in the browser. Nothing about the student is stored or sent.
 *
 * How it works:
 *   1. Each test page calls CloseTheGaps.show(testId, missedKeys) when the
 *      results appear. missedKeys are the answer keys the page already uses
 *      (for example "b", "longa", "erirur"), or syllable type names on the
 *      syllable types test.
 *   2. TEST_ITEM_PHONOGRAMS turns each key into the phonograms shown on the
 *      correct answer tile for that test (for example "longa" is ai, ay, eigh).
 *   3. PHONOGRAM_LESSONS turns each phonogram into the lesson that teaches it.
 *   4. Lessons are listed once each, in lesson number order, followed by the
 *      next segment's pretest from NEXT_STEPS.
 */
(function (root) {
    'use strict';

    var SITE = 'https://www.storyhouracademy.org';

    // Lesson titles, matching each lesson page title.
    var LESSONS = {
        3: 'Letter B', 4: 'Letter D', 5: 'Letter F', 6: 'Letter H', 7: 'Letter J',
        8: 'Letter K', 9: 'Letter L', 10: 'Letter M', 11: 'Letter N', 12: 'Letter P',
        13: 'Phonogram QU', 14: 'Letter R', 15: 'Letter T', 16: 'Letter V',
        17: 'Letter W', 18: 'Letter Z',
        23: 'Phonogram CK', 24: 'Phonogram CH', 25: 'Phonogram NG', 26: 'Phonogram SH',
        27: 'Phonogram TH', 28: 'Phonogram WH',
        33: 'Vowel Phonogram AI', 34: 'Vowel Phonogram AY', 35: 'Vowel Phonogram EIGH',
        36: 'Vowel Phonogram EE', 37: 'Vowel Phonogram IGH', 38: 'Vowel Phonogram OA',
        39: 'Vowel Phonogram AU', 40: 'Vowel Phonogram AW', 41: 'Vowel Phonogram OI',
        42: 'Vowel Phonogram OY', 43: 'Vowel Phonogram UI', 44: 'Vowel Phonogram ER',
        45: 'Vowel Phonogram IR', 46: 'Vowel Phonogram UR', 47: 'Vowel Phonogram AR',
        48: 'Vowel Phonograms OR and WOR', 49: 'Vowel Phonogram EAR', 50: 'Vowel Phonogram OUR',
        55: 'Letter A', 56: 'Letter E', 57: 'Letter I', 58: 'Letter O', 59: 'Letter U',
        60: 'Letter Y',
        65: 'Letter C', 66: 'Letter G', 67: 'Letter S', 68: 'Letter X',
        73: 'Closed Syllables', 74: 'Open Syllables', 75: 'Consonant-LE Syllables',
        76: 'R-Controlled Syllables', 77: 'Vowel-Consonant-E Syllables', 78: 'Vowel Team Syllables',
        81: 'The Schwa Sound',
        84: 'Phonogram TCH', 85: 'Phonogram PH', 86: 'Phonogram RH', 87: 'Phonogram GH',
        88: 'Phonogram GN', 89: 'Phonogram KN', 90: 'Phonogram WR', 91: 'Phonogram DG',
        92: 'Phonogram AIGH',
        97: 'Phonogram GU', 98: 'Phonogram OE', 99: 'Phonogram OU', 100: 'Phonogram OW',
        101: 'Phonogram OO', 102: 'Phonogram EW', 103: 'Phonograms EU and EUR',
        104: 'Phonogram EA', 105: 'Phonogram EAU', 106: 'Phonogram EI', 107: 'Phonogram EY',
        108: 'Phonogram IE', 109: 'Phonogram AUGH', 110: 'Phonogram OUGH'
    };

    // The lesson that teaches each phonogram or syllable type.
    var PHONOGRAM_LESSONS = {
        b: 3, d: 4, f: 5, h: 6, j: 7, k: 8, l: 9, m: 10, n: 11, p: 12, qu: 13,
        r: 14, t: 15, v: 16, w: 17, z: 18,
        ck: 23, ch: 24, ng: 25, sh: 26, th: 27, wh: 28,
        ai: 33, ay: 34, eigh: 35, ee: 36, igh: 37, oa: 38, au: 39, aw: 40,
        oi: 41, oy: 42, ui: 43, er: 44, ir: 45, ur: 46, ar: 47, or: 48, wor: 48,
        ear: 49, our: 50,
        a: 55, e: 56, i: 57, o: 58, u: 59, y: 60,
        c: 65, g: 66, s: 67, x: 68,
        'closed': 73, 'open': 74, 'consonant-le': 75, 'r-controlled': 76,
        'vowel-consonant-e': 77, 'vowel-team': 78,
        tch: 84, ph: 85, rh: 86, gh: 87, gn: 88, kn: 89, wr: 90, dg: 91, aigh: 92,
        gu: 97, oe: 98, ou: 99, ow: 100, oo: 101, ew: 102, eu: 103, eur: 103,
        ea: 104, eau: 105, ei: 106, ey: 107, ie: 108, augh: 109, ough: 110
    };

    // Friendly names for syllable types, used in task descriptions.
    var SKILL_LABELS = {
        'closed': 'closed syllables', 'open': 'open syllables',
        'consonant-le': 'consonant-le syllables', 'r-controlled': 'r-controlled syllables',
        'vowel-consonant-e': 'vowel-consonant-e syllables', 'vowel-team': 'vowel team syllables'
    };

    // Answer keys whose correct tile shows more than one phonogram.
    // These match the soundToPhonogram tables and tiles on each test page.
    var VOWEL_TEAM_KEYS = {
        longa: ['ai', 'ay', 'eigh'], broada: ['au', 'aw'], ear3: ['ear'], longe: ['ee'],
        erirur: ['er', 'ir', 'ur'], longi: ['igh'], longo: ['oa'], oioy: ['oi', 'oy'],
        our2: ['our'], longoo: ['ui']
    };
    var TEST_ITEM_PHONOGRAMS = {
        // Tests 1, 2, 6, 8: every key is its own phonogram or syllable type.
        3: { k: ['k', 'ck'] }, // the /k/ tile shows ck and k
        4: VOWEL_TEAM_KEYS,
        5: VOWEL_TEAM_KEYS,
        7: merge(VOWEL_TEAM_KEYS, { ck: ['ck', 'k'] }),
        9: merge(VOWEL_TEAM_KEYS, {
            longa: ['ai', 'ay', 'eigh', 'aigh'], ck: ['ck', 'k'], f: ['f', 'ph'],
            j: ['j', 'dg'], n: ['n', 'gn', 'kn'], r: ['r', 'wr', 'rh']
        }),
        10: merge(VOWEL_TEAM_KEYS, {
            longa: ['ai', 'ay', 'eigh', 'aigh'], ck: ['ck', 'k'], f: ['f', 'ph'],
            j: ['j', 'dg'], n: ['n', 'gn', 'kn'], r: ['r', 'wr', 'rh'],
            ew: ['ew', 'eu'], eur: ['eur']
        })
    };

    // Test names, matching tests.html.
    var TEST_NAMES = {
        1: 'Single-Sound Consonants (lowercase)',
        2: 'Single-Sound Consonants (uppercase)',
        3: 'Single-Sound Consonants and Consonant Digraphs',
        4: 'Multi-Letter Vowel Phonograms',
        5: '25 Vowel Phonograms',
        6: 'Alphabet Letters and their Associated Sounds',
        7: '51 Phonograms',
        8: 'Syllable Types',
        9: '60 Phonograms',
        10: '75 Phonograms'
    };

    function pretestStep(n) {
        return { kind: 'test', slug: 'pretest-' + n, title: 'Pretest of ' + TEST_NAMES[n],
            description: 'Take this pretest to see what to learn next. Show your teacher the results.' };
    }

    // What comes after each test, following the lesson order on the site.
    // Lesson 1 gives pretests 1 and 2, lesson 21 gives pretest 3, lesson 31
    // gives pretest 4, lesson 53 gives pretest 5, lesson 63 gives pretests 6
    // and 7, lesson 71 gives pretest 8, lesson 82 gives pretest 9, and lesson
    // 95 gives pretest 10. Lesson 81 (The Schwa Sound) has no test, so it
    // comes before pretest 9. Test 10 is the last test in the course, so its
    // plan ends with the 75 Phonograms Mastery Test as a final check.
    var NEXT_STEPS = {
        1: [pretestStep(3)],
        2: [pretestStep(3)],
        3: [pretestStep(4)],
        4: [pretestStep(5)],
        5: [pretestStep(6), pretestStep(7)],
        6: [pretestStep(8)],
        7: [pretestStep(8)],
        8: [{ kind: 'lesson', slug: 'lesson-81', title: 'Lesson 81: The Schwa Sound',
              description: 'Work through each activity in this lesson.' }, pretestStep(9)],
        9: [pretestStep(10)],
        10: [{ kind: 'test', slug: 'test-10', title: 'Mastery Test of 75 Phonograms',
               description: 'Take the mastery test again to check that the gaps are closed. Show your teacher the results.' }]
    };

    function merge(a, b) {
        var out = {}, k;
        for (k in a) { if (Object.prototype.hasOwnProperty.call(a, k)) out[k] = a[k]; }
        for (k in b) { if (Object.prototype.hasOwnProperty.call(b, k)) out[k] = b[k]; }
        return out;
    }

    function parseTestId(testId) {
        var m = /^(pretest|test)-(\d+)$/.exec(testId || '');
        if (!m || !TEST_NAMES[m[2]]) return null;
        var num = Number(m[2]);
        var kind = m[1] === 'pretest' ? 'Pretest' : 'Mastery Test';
        return { id: testId, num: num, kind: kind, name: TEST_NAMES[num],
                 label: TEST_NAMES[num] + ' ' + kind,
                 pageTitle: kind + ' of ' + TEST_NAMES[num] };
    }

    function phonogramsFor(testNum, key) {
        var table = TEST_ITEM_PHONOGRAMS[testNum] || {};
        if (Object.prototype.hasOwnProperty.call(table, key)) return table[key];
        return [key];
    }

    // Returns the lesson numbers for one missed answer key on one test.
    function lessonsForItem(testNum, key) {
        var normalized = String(key).toLowerCase();
        return phonogramsFor(testNum, normalized)
            .map(function (p) { return PHONOGRAM_LESSONS[p]; })
            .filter(function (n) { return typeof n === 'number'; });
    }

    function stepUrl(slug) { return SITE + '/' + slug; }

    // Builds the plan for a test and a list of missed answer keys.
    function buildPlan(testId, missedKeys) {
        var test = parseTestId(testId);
        if (!test) throw new Error('Unknown test: ' + testId);

        var focus = {}; // lesson number -> list of phonograms or skills
        var unmapped = [];
        (missedKeys || []).forEach(function (key) {
            var normalized = String(key).toLowerCase();
            var phonograms = phonogramsFor(test.num, normalized);
            var found = false;
            phonograms.forEach(function (p) {
                var lesson = PHONOGRAM_LESSONS[p];
                if (typeof lesson !== 'number') return;
                found = true;
                focus[lesson] = focus[lesson] || [];
                var label = SKILL_LABELS[p] || p;
                if (focus[lesson].indexOf(label) === -1) focus[lesson].push(label);
            });
            if (!found) unmapped.push(key);
        });

        var lessonNumbers = Object.keys(focus).map(Number).sort(function (a, b) { return a - b; });
        var lessons = lessonNumbers.map(function (n) {
            return {
                kind: 'lesson',
                slug: 'lesson-' + n,
                url: stepUrl('lesson-' + n),
                title: 'Lesson ' + n + ': ' + LESSONS[n],
                description: 'Work through each activity in this lesson. Practice: ' + focus[n].join(', ') + '.'
            };
        });
        var next = NEXT_STEPS[test.num].map(function (step) {
            return { kind: step.kind, slug: step.slug, url: stepUrl(step.slug),
                     title: step.title, description: step.description };
        });
        var lastStep = next[next.length - 1];

        return {
            test: test,
            allCorrect: lessons.length === 0,
            lessons: lessons,
            next: next,
            items: lessons.length ? lessons.concat(next) : [],
            unmapped: unmapped,
            name: 'Story Hour Academy: Closing the Gaps after the ' + test.label,
            description: 'Story Hour Academy lessons for the sounds and skills missed on the ' +
                test.label + ', followed by the ' + lastStep.title + '. Free and public domain at storyhouracademy.org.',
            fileName: 'story-hour-academy-closing-the-gaps-' + test.id + '.csv'
        };
    }

    function csvField(value) {
        var s = String(value == null ? '' : value).replace(/[\r\n]+/g, ' ');
        if (/[",]/.test(s) || /^\s|\s$/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
        return s;
    }

    function csvRow(fields) { return fields.map(csvField).join(','); }

    // Lesson Hollow curriculum file: five detail rows, a blank row,
    // the task header, then one row per task.
    function toCsv(plan) {
        var rows = [
            csvRow(['Name', plan.name]),
            csvRow(['Description', plan.description]),
            csvRow(['Publisher', 'Story Hour Academy']),
            csvRow(['Grade Level', 'Any']),
            csvRow(['Link', stepUrl(plan.test.id)]),
            '',
            csvRow(['Title', 'Description', 'Action', 'URL'])
        ];
        plan.items.forEach(function (item) {
            rows.push(csvRow([item.title, item.description, 'Do', item.url]));
        });
        return rows.join('\r\n') + '\r\n';
    }

    // ---------- Browser section ----------

    function escapeHtml(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    function stepLink(item) {
        return '<a href="/' + escapeHtml(item.slug) + '">' + escapeHtml(item.title) + '</a>';
    }

    function renderHtml(plan) {
        var html = '<h2 class="close-gaps-title" id="closeGapsTitle">Close the Gaps</h2>';

        if (plan.allCorrect) {
            if (plan.test.num === 10) {
                html += '<p>Every answer was right. Your student knows all 75 phonograms, ' +
                    'which is everything Story Hour Academy tests. Wonderful work!</p>';
                return html;
            }
            html += '<p>Every answer was right, so there are no gaps to close. ' +
                'Your student is ready for what comes next:</p>' +
                '<ul class="close-gaps-next">' + plan.next.map(function (item) {
                    return '<li>' + stepLink(item) + '</li>';
                }).join('') + '</ul>';
            return html;
        }

        var count = plan.lessons.length;
        var ending = plan.test.num === 10
            ? 'the ' + plan.next[0].title + ' as a final check.'
            : plan.next.map(function (item) { return item.title; }).join(' and ') + '.';
        html += '<p>Here is a plan made from this test. It goes back to just the ' +
            (count === 1 ? 'lesson' : count + ' lessons') +
            ' your student still needs, then ends with ' + escapeHtml(ending) + '</p>' +
            '<ol class="close-gaps-list">' + plan.items.map(function (item) {
                return '<li class="close-gaps-item close-gaps-' + item.kind + '">' + stepLink(item) + '</li>';
            }).join('') + '</ol>' +
            '<div class="close-gaps-actions"><button type="button" class="primary-button close-gaps-download">' +
            '<i class="fas fa-download"></i> Download the Plan</button></div>' +
            '<h3 class="close-gaps-subtitle">Use it free in Lesson Hollow</h3>' +
            '<p><a href="https://lessonhollow.com" target="_blank" rel="noopener">Lesson Hollow</a> ' +
            'turns this plan into a daily checklist for your child.</p>' +
            '<ol class="close-gaps-steps">' +
            '<li>Download the plan. It is a small spreadsheet file, called a comma-separated values (CSV) file.</li>' +
            '<li>Sign up free at <a href="https://lessonhollow.com" target="_blank" rel="noopener">lessonhollow.com</a>. ' +
            'No credit card needed.</li>' +
            '<li>Switch to your child\'s Player View, open Curriculums, click New Curriculum, choose the CSV Upload tab, and add the file.</li>' +
            '<li>Enroll your child. Their first curriculum is free.</li>' +
            '</ol>' +
            '<p class="close-gaps-note">This plan is made right here in your browser. ' +
            'Nothing about your student is saved or sent anywhere.</p>';
        return html;
    }

    function download(plan) {
        var blob = new Blob([toCsv(plan)], { type: 'text/csv;charset=utf-8' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = plan.fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    }

    function getContainer() {
        var section = document.getElementById('closeTheGaps');
        if (section) return section;
        section = document.createElement('section');
        section.id = 'closeTheGaps';
        section.className = 'close-gaps';
        section.setAttribute('aria-labelledby', 'closeGapsTitle');
        var screen = document.getElementById('resultsScreen');
        (screen || document.querySelector('main') || document.body).appendChild(section);
        return section;
    }

    function show(testId, missedKeys) {
        try {
            var plan = buildPlan(testId, missedKeys);
            var section = getContainer();
            section.innerHTML = renderHtml(plan);
            var button = section.querySelector('.close-gaps-download');
            if (button) button.addEventListener('click', function () { download(plan); });
            return plan;
        } catch (err) {
            if (root.console) root.console.error('Close the Gaps:', err);
            return null;
        }
    }

    var api = {
        show: show,
        buildPlan: buildPlan,
        toCsv: toCsv,
        lessonsForItem: lessonsForItem,
        renderHtml: renderHtml,
        data: {
            LESSONS: LESSONS, PHONOGRAM_LESSONS: PHONOGRAM_LESSONS,
            TEST_ITEM_PHONOGRAMS: TEST_ITEM_PHONOGRAMS, TEST_NAMES: TEST_NAMES, NEXT_STEPS: NEXT_STEPS
        }
    };

    if (typeof module !== 'undefined' && module.exports) module.exports = api;
    root.CloseTheGaps = api;
})(typeof window !== 'undefined' ? window : globalThis);
