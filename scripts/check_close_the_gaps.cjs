#!/usr/bin/env node
/*
 * Checks the Close the Gaps data against the real test and lesson pages.
 *
 *   node scripts/check_close_the_gaps.cjs [output-folder]
 *
 * For every pretest and mastery test it confirms that:
 *   - the page loads js/close-the-gaps.js and calls CloseTheGaps.show with its own id
 *   - every answer key on the page maps to at least one lesson
 *   - multi-phonogram tiles (soundToPhonogram) match the mapping data
 * It also confirms every linked lesson and test page exists with a matching
 * title. With an output folder, it writes a sample curriculum file for each
 * test where every item was missed.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.join(__dirname, '..');
// Load the browser script the same way a page does, without a bundler.
const sandbox = { console };
sandbox.globalThis = sandbox;
vm.runInNewContext(fs.readFileSync(path.join(root, 'js', 'close-the-gaps.js'), 'utf8'), sandbox);
const ctg = sandbox.CloseTheGaps;
const outDir = process.argv[2];
let failures = 0;
const fail = (msg) => { failures++; console.error('FAIL: ' + msg); };

function grab(src, name) {
    const m = src.match(new RegExp('const ' + name + '\\s*=\\s*([\\[{][\\s\\S]*?[\\]}]);'));
    // eslint-disable-next-line no-eval
    return m ? eval('(' + m[1] + ')') : null;
}

function pageTitle(slug) {
    const file = path.join(root, slug + '.html');
    if (!fs.existsSync(file)) return null;
    const m = fs.readFileSync(file, 'utf8').match(/<title>([^<|]*)/);
    return m ? m[1].trim() : '';
}

// Lesson titles in the data match the lesson pages.
for (const [n, title] of Object.entries(ctg.data.LESSONS)) {
    const actual = pageTitle('lesson-' + n);
    if (actual === null) fail('missing lesson-' + n + '.html');
    else if (actual !== 'Lesson ' + n + ': ' + title) fail(`lesson-${n} title "${actual}" does not match "${title}"`);
}
for (const p of Object.keys(ctg.data.PHONOGRAM_LESSONS)) {
    const n = ctg.data.PHONOGRAM_LESSONS[p];
    if (!ctg.data.LESSONS[n]) fail(`phonogram ${p} points to lesson ${n} with no title`);
}

if (outDir) fs.mkdirSync(outDir, { recursive: true });

let checked = 0;
for (const kind of ['pretest', 'test']) {
    for (let n = 1; n <= 10; n++) {
        const id = `${kind}-${n}`;
        const src = fs.readFileSync(path.join(root, id + '.html'), 'utf8');
        if (!src.includes('/js/close-the-gaps.js')) fail(id + ' does not load close-the-gaps.js');
        if (!src.includes(`CloseTheGaps.show('${id}'`)) fail(id + ' does not call CloseTheGaps.show with its id');

        let keys;
        if (n === 8) {
            keys = grab(src, 'syllableTypes');
            const words = grab(src, 'words');
            words.forEach((w) => w.types.forEach((t) => {
                if (!keys.includes(t)) fail(`${id} word ${w.word} uses unknown type ${t}`);
            }));
        } else {
            keys = grab(src, 'allSounds');
        }
        if (!keys || !keys.length) { fail(id + ' has no answer keys'); continue; }

        const s2p = grab(src, 'soundToPhonogram');
        for (const key of keys) {
            const lessons = ctg.lessonsForItem(n, key);
            if (!lessons.length) fail(`${id} answer "${key}" maps to no lesson`);
            if (s2p && s2p[key]) {
                const tile = s2p[key].split('/').sort().join(',');
                const plan = ctg.buildPlan(id, [key]);
                const mapped = [];
                plan.lessons.forEach((l) => {
                    const m = l.description.match(/Practice: (.*)\.$/);
                    m[1].split(', ').forEach((p) => mapped.push(p));
                });
                if (mapped.sort().join(',') !== tile) fail(`${id} answer "${key}" tile ${s2p[key]} maps to ${mapped.join('/')}`);
            }
        }

        const plan = ctg.buildPlan(id, keys);
        if (plan.unmapped.length) fail(`${id} unmapped: ${plan.unmapped.join(', ')}`);
        for (const item of plan.items) {
            const t = pageTitle(item.slug);
            if (t === null) fail(`${id} links to missing page ${item.slug}`);
        }
        const nextTitle = plan.next.map((s) => s.slug).join(' + ');
        console.log(`ok ${id}: ${keys.length} answers -> ${plan.lessons.length} lessons, then ${nextTitle}`);
        if (outDir) fs.writeFileSync(path.join(outDir, plan.fileName), ctg.toCsv(plan));
        checked++;
    }
}

console.log(`\n${checked} test pages checked, ${failures} problem(s).`);
process.exit(failures ? 1 : 0);
