#!/usr/bin/env python3
"""
rebuild.py — Unified Excel-to-JSON rebuild script for Quiz Generator

Features:
  • Pandas column-name-based reading (robust to column reordering)
  • Corrections loaded from corrections.json (no hardcoded fixes in code)
  • Data validation: duplicate numbers, missing options, invalid answers

Usage:
  python rebuild.py          # rebuild all questions
  python rebuild.py --check  # validation only (no output)
"""

import pandas as pd
import os
import re
import json
import sys

# Fix Windows console encoding for Unicode/emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# CONFIGURATION
# ============================================================
BASE = os.path.dirname(os.path.abspath(__file__))

# Column names used in Excel files
COL_NUM   = 'Số TT'
COL_TEXT  = 'Nội dung câu hỏi (*)'
COL_ANS   = 'Đáp án (*)'

OPTION_COLS = [
    ('P/A lựa chọn 1', 'A'),
    ('P/A lựa chọn 2', 'B'),
    ('P/A lựa chọn 3', 'C'),
    ('P/A lựa chọn 4', 'D'),
]

# Files to process (source Excel, sheet label, mode)
# Order matters — questions appended in this order.
FILES = [
    # --- VHF (xls, multi-sheet) ---
    {
        'file': 'NHCH LÝ THUYẾT NĂNG LỰC VHF.xls',
        'mode': 'vhf',
        'label_mode': True,       # use sheet name as label
        'fallback_cols': {       # positional fallback (openpyxl 1-indexed)
            'num': 6, 'text': 7, 'ans': 8, 'opts': [9, 10, 11, 12]
        },
    },
    # --- Radar (xlsx, single active sheet) ---
    {
        'file': 'NH Câu hỏi, ĐA Lý thuyết_Nguyên lý PSR _16.5.2026.xlsx',
        'label': 'PSR (Sơ cấp)',
        'mode': 'radar',
        'fallback_cols': {
            'num': 1, 'text': 2, 'ans': 3, 'opts': [4, 5, 6, 7]
        },
    },
    {
        'file': 'NH Câu hỏi, ĐA Lý thuyết_Nguyên lý SSR _5.2026.xlsx',
        'label': 'SSR (Thứ cấp)',
        'mode': 'radar',
        'fallback_cols': {
            'num': 1, 'text': 2, 'ans': 3, 'opts': [4, 5, 6, 7]
        },
    },
    {
        'file': 'NH Câu hỏi, ĐA Lý thuyết_Radar_Indra_PSR_SSR INDRA_5.2026.xlsx',
        'label': 'Indra PSR SSR',
        'mode': 'radar',
        'fallback_cols': {
            'num': 1, 'text': 2, 'ans': 3, 'opts': [4, 5, 6, 7]
        },
    },
    # --- Kíp Trưởng (xlsx, single active sheet) ---
    {
        'file': '06. LT KT Radar Son Tra_Long.xlsx',
        'label': 'Radar Sơn Trà',
        'mode': 'kip_truong',
        'fallback_cols': {
            'num': 6, 'text': 7, 'ans': 8, 'opts': [9, 10, 11, 12]
        },
    },
]

# ============================================================
# CORRECTIONS
# ============================================================
CORRECTIONS_FILE = os.path.join(BASE, 'corrections.json')


def load_corrections():
    """Load regex-based corrections from corrections.json."""
    if not os.path.exists(CORRECTIONS_FILE):
        print(f'[WARN] corrections.json not found at {CORRECTIONS_FILE}, skipping corrections.')
        return []
    with open(CORRECTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('fixes', [])


# ============================================================
# COLUMN NAME NORMALISATION
# ============================================================
# Reverse alias map: normalised column name → canonical name.
# Covers newlines, accent variations, extra symbols, etc.
_COL_ALIASES = {
    # Number columns
    'số tt':       'SỐ TT',
    'số\n tt':     'SỐ TT',
    'số  tt':      'SỐ TT',
    'sốtt':        'SỐ TT',
    'so tt':       'SỐ TT',
    'so\n tt':     'SỐ TT',
    # Text columns
    'nội dung câu hỏi (*)': 'NỘI DUNG CÂU HỎI (*)',
    'noi dung cau hoi (*)': 'NỘI DUNG CÂU HỎI (*)',
    'nội dung câu hỏi':     'NỘI DUNG CÂU HỎI (*)',
    'noi dung cau hoi':     'NỘI DUNG CÂU HỎI (*)',
    # Answer columns
    'đáp án':        'ĐÁP ÁN',
    'dáp án':        'ĐÁP ÁN',
    'đáp án (*)':    'ĐÁP ÁN',
    'dáp án (*)':    'ĐÁP ÁN',
    'đáp án\n(*)':   'ĐÁP ÁN',
    'đáp án\n':      'ĐÁP ÁN',
    'đáp án ':       'ĐÁP ÁN',
    'dap án':        'ĐÁP ÁN',
    'dap án (*)':    'ĐÁP ÁN',
    'dáp án\n':      'ĐÁP ÁN',
    # Option columns
    'p/a lựa chọn 1':  'P/A LỰA CHỌN 1',
    'p/a lua chon 1':  'P/A LỰA CHỌN 1',
    'p/a lựa chọn 2':  'P/A LỰA CHỌN 2',
    'p/a lua chon 2':  'P/A LỰA CHỌN 2',
    'p/a lựa chọn 3':  'P/A LỰA CHỌN 3',
    'p/a lua chon 3':  'P/A LỰA CHỌN 3',
    'p/a lựa chọn 4':  'P/A LỰA CHỌN 4',
    'p/a lua chon 4':  'P/A LỰA CHỌN 4',
    'p/a lựa chọn 5':  'P/A LỰA CHỌN 5',
}

# Canonical column definitions
COL_NUM    = 'SỐ TT'
COL_TEXT   = 'NỘI DUNG CÂU HỎI (*)'
COL_ANS    = 'ĐÁP ÁN'

OPTION_MAP = [
    ('P/A LỰA CHỌN 1', 'A'), ('P/A LỰA CHỌN 2', 'B'),
    ('P/A LỰA CHỌN 3', 'C'), ('P/A LỰA CHỌN 4', 'D'),
]


def _normalise(name):
    """Strip whitespace (including newlines) and lowercase for matching."""
    return name.strip().lower().replace('\n', '').replace('\r', '')


def get_col(df, canonical_name):
    """
    Find a column in the DataFrame, with alias fallback.
    1) Direct case-insensitive match
    2) Alias match from _COL_ALIASES
    3) None
    """
    canon_norm = _normalise(canonical_name)

    # 1) Direct match
    for col in df.columns:
        if _normalise(col) == canon_norm:
            return col

    # 2) Alias match
    for col in df.columns:
        col_norm = _normalise(col)
        if col_norm in _COL_ALIASES:
            alias_target = _COL_ALIASES[col_norm]
            if _normalise(alias_target) == canon_norm:
                return col

    return None


# ============================================================
# HELPERS
# ============================================================
def clean(v):
    """Strip NaN, whitespace, and normalise."""
    if pd.isna(v):
        return ""
    return str(v).strip()


def map_answer(val):
    """Map raw answer value to A/B/C/D."""
    if not val:
        return None
    s = str(val).strip().upper()
    # Handle Excel numeric answers (1.0 → '1')
    if s.endswith('.0'):
        s = s[:-2]
    numeric_map = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'}
    if s in numeric_map:
        return numeric_map[s]
    if s in ('A', 'B', 'C', 'D'):
        return s
    return None


# ============================================================
# PROCESS A SINGLE DATAFRAME
# ============================================================
def process_df(df, mode, sheet_label, questions, fallback_cols=None):
    """
    Process one Excel sheet DataFrame into question dicts.

    Uses pandas column-name-based reading when possible,
    falls back to positional columns for legacy formats.
    """
    # Find columns by normalised name
    col_num  = get_col(df, COL_NUM)
    col_text = get_col(df, COL_TEXT)
    col_ans  = get_col(df, COL_ANS)
    use_names = col_text is not None and col_ans is not None

    for _, row in df.iterrows():
        try:
            if use_names:
                # --- Pandas column-name-based reading ---
                num       = int(row[col_num]) if pd.notna(row[col_num]) else len(questions) + 1
                text      = clean(row[col_text]).replace('\n', ' ').replace('\t', ' ')
                ans       = map_answer(row[col_ans])

                if not text or not ans:
                    continue

                opts = {}
                for opt_col, key in OPTION_MAP:
                    actual_opt_col = get_col(df, opt_col)
                    if actual_opt_col and pd.notna(row[actual_opt_col]):
                        v = re.sub(r'^[A-D][.\s]+', '', clean(row[actual_opt_col]))
                        if v:
                            opts[key] = v

            else:
                # --- Positional fallback (legacy) ---
                fb = fallback_cols or {}
                num       = int(row.iloc[fb['num'] - 1]) if pd.notna(row.iloc[fb['num'] - 1]) else len(questions) + 1
                text      = clean(row.iloc[fb['text'] - 1]).replace('\n', ' ').replace('\t', ' ')
                ans       = map_answer(row.iloc[fb['ans'] - 1])

                if not text or not ans:
                    continue

                opts = {}
                for i, key in zip(fb.get('opts', []), ['A', 'B', 'C', 'D']):
                    if i - 1 < len(row) and pd.notna(row.iloc[i - 1]):
                        v = re.sub(r'^[A-D][.\s]+', '', clean(row.iloc[i - 1]))
                        if v:
                            opts[key] = v

            # Only include if we have at least one option
            if text and ans and opts:
                # Skip meta-questions
                if text.strip().lower() == 'câu hỏi chung':
                    continue
                questions.append({
                    'number': num,
                    'text': text,
                    'correct': ans,
                    'sheet': sheet_label,
                    'mode': mode,
                    'options': opts,
                })

        except Exception:
            continue  # skip malformed rows


# ============================================================
# CLEANING PASS (removes stray quotes/newlines from output)
# ============================================================
def clean_questions(questions):
    """Final sanitisation: remove stray quotes, extra whitespace."""
    for q in questions:
        q['text'] = re.sub(r'["\']', '', q['text']).replace('\n', ' ').replace('\t', ' ')
        for k in q['options']:
            q['options'][k] = (
                re.sub(r'["\']', '', str(q['options'][k]))
                .replace('\n', ' ')
                .replace('\t', ' ')
            )


# ============================================================
# CORRECTIONS
# ============================================================
def apply_corrections(questions, corrections):
    """Apply regex-based answer corrections."""
    applied = 0
    for q in questions:
        text = q.get('text', '')
        for fix in corrections:
            if re.search(fix['pattern'], text, re.IGNORECASE):
                old = q['correct']
                q['correct'] = fix['new_correct']
                applied += 1
                mode_icon = {'vhf': '📡', 'radar': '📟', 'kip_truong': '🎖️'}
                icon = mode_icon.get(q['mode'], '?')
                print(f'  ✓ {icon} {q["mode"]} #{q["number"]} [{q["sheet"]}] '
                      f'{old} → {fix["new_correct"]}')
                break  # only first matching correction per question
    return applied


# ============================================================
# VALIDATION
# ============================================================
def validate(questions, corrections):
    """Run validation checks and report issues."""
    errors = []
    warnings = []

    # --- Duplicate question numbers per (mode, sheet) ---
    seen = {}
    for q in questions:
        key = (q['mode'], q['sheet'], q['number'])
        if key in seen:
            errors.append(f'Duplicate question: {key}')
        seen[key] = q

    # --- Missing options ---
    for q in questions:
        missing = [opt for opt in 'ABCD' if opt not in q.get('options', {})]
        if missing:
            warnings.append(
                f'Missing options {missing} — {q["mode"]} #{q["number"]} [{q["sheet"]}]')

    # --- Invalid answer ---
    for q in questions:
        if q.get('correct') not in ('A', 'B', 'C', 'D'):
            errors.append(f'Invalid answer "{q["correct"]}" — {q["mode"]} #{q["number"]}')

    # --- Empty text ---
    for q in questions:
        if not q.get('text', '').strip():
            errors.append(f'Empty text — {q["mode"]} #{q["number"]}')

    # --- Report ---
    print()
    print('─── VALIDATION ───')
    if errors:
        print(f'  ❌ {len(errors)} error(s):')
        for e in errors[:20]:
            print(f'     • {e}')
        if len(errors) > 20:
            print(f'     ... and {len(errors) - 20} more')
    if warnings:
        print(f'  ⚠️  {len(warnings)} warning(s):')
        for w in warnings[:10]:
            print(f'     • {w}')
        if len(warnings) > 10:
            print(f'     ... and {len(warnings) - 10} more')
    if not errors and not warnings:
        print('  ✅ All checks passed!')

    return errors, warnings


# ============================================================
# MAIN
# ============================================================
def run(verify_only=False):
    all_questions = []

    for item in FILES:
        fpath = os.path.join(BASE, item['file'])
        if not os.path.exists(fpath):
            print(f'[SKIP] File not found: {item["file"]}')
            continue

        mode_icon = {'vhf': '📡', 'radar': '📟', 'kip_truong': '🎖️'}
        icon = mode_icon.get(item['mode'], '?')
        print(f'\n[{icon}] Processing: {item["file"]} (mode={item["mode"]})')

        try:
            if fpath.endswith('.xls'):
                # VHF: multi-sheet, each sheet is a separate group
                wb = pd.ExcelFile(fpath, engine='xlrd')
                for sname in wb.sheet_names:
                    df = pd.read_excel(fpath, engine='xlrd', sheet_name=sname)
                    label = sname
                    process_df(df, item['mode'], label, all_questions,
                               fallback_cols=item.get('fallback_cols'))
                print(f'  → {len([q for q in all_questions if q["mode"] == item["mode"]])} total so far')

            else:
                # xlsx: read active sheet only (matches original rebuild2 behavior)
                df = pd.read_excel(fpath, engine='openpyxl')
                label = item.get('label', 'Sheet1')
                process_df(df, item['mode'], label, all_questions,
                           fallback_cols=item.get('fallback_cols'))
                print(f'  → {item.get("label", label)}: {len([q for q in all_questions if q["mode"] == item["mode"] and q["sheet"] == label])} questions')

        except Exception as e:
            print(f'  ❌ Error: {e}')

    # --- Final cleaning ---
    clean_questions(all_questions)

    # --- Load & apply corrections ---
    corrections = load_corrections()
    if corrections:
        applied = apply_corrections(all_questions, corrections)
        print(f'  Applied {applied} correction(s) from corrections.json')

    # --- Validation ---
    errors, warnings = validate(all_questions, corrections)

    if errors:
        print(f'\n❌ {len(errors)} error(s) found. Check output above.')

    # --- Output summary ---
    print()
    print('─── SUMMARY ───')
    print(f'  Total questions: {len(all_questions)}')
    from collections import Counter
    modes = Counter(q['mode'] for q in all_questions)
    for m, count in sorted(modes.items()):
        icon = {'vhf': '📡', 'radar': '📟', 'kip_truong': '🎖️'}.get(m, '?')
        print(f'  {icon} {m}: {count}')

    sheets = Counter(q['sheet'] for q in all_questions)
    for s, count in sheets.most_common():
        print(f'    [{s}] {count}')

    # --- Write JSON ---
    out = os.path.join(BASE, 'all_questions.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print(f'\n✅ Saved: {out}')

    # --- Return status ---
    return len(errors) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        run(verify_only=True)
    else:
        success = run()
        sys.exit(0 if success else 1)
