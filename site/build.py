#!/usr/bin/env python3
"""
build.py — Generate static HTML from markdown content for Operators Delulu site.
Usage: python3 build.py
"""

import os
import re

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(SITE_DIR, 'public')

# Language support
LANG = os.getenv('LANG', 'en')
if LANG not in ('en', 'tr'):
    raise ValueError(f"Unsupported language: {LANG}. Use 'en' or 'tr'.")

CONTENT_DIR = os.path.join(SITE_DIR, 'content', LANG)
# Output: en -> public/, tr -> public/tr/
OUTPUT_DIR = os.path.join(PUBLIC_DIR, LANG) if LANG != 'en' else PUBLIC_DIR

PAGES = [
    ('index.html', 'section-index', 'You Found It'),
    ('principles.html', 'section-principles', 'The Seven Principles'),
    ('egregores.html', 'section-egregores', 'Egregores'),
    ('psyche.html', 'section-psyche', 'Psyche'),
    ('dialectic.html', 'section-dialectic', 'The Dialectic'),
    ('crunch.html', 'section-crunch', 'The Crunch'),
    ('gateway.html', 'section-gateway', 'The Gateway'),
    ('lab.html', 'section-lab', 'The Lab'),
    ('transcendence.html', 'section-transcendance', 'Transcendence'),
]

# Keep NAV_ORDER frozen — never localize section IDs
NAV_ORDER = ['index','principles','egregores','psyche','dialectic','crunch','gateway','lab','transcendance']
CONTENT_FILENAME_MAP = {'transcendance': 'transcendence'}

# Language-specific labels & meta
SECTION_LABELS = {
    'en': {
        'index': 'Home', 'principles': 'Principles', 'egregores': 'Egregores',
        'psyche': 'Psyche', 'dialectic': 'Dialectic', 'crunch': 'Crunch',
        'gateway': 'Gateway', 'lab': 'Lab', 'transcendance': 'Transcendence',
    },
    'tr': {
        'index': 'Harita', 'principles': 'İlkeler', 'egregores': 'Egregorlar',
        'psyche': 'Psike', 'dialectic': 'Diyalektik', 'crunch': 'Sıkışma',
        'gateway': 'Geçit', 'lab': 'Laboratuvar', 'transcendance': 'Aşım'
    }
}[LANG]

SUBTITLES = {
    'en': {
        'principles': 'How reality works',
        'egregores': 'Collective thoughtform ecology',
        'psyche': 'The inner architecture',
        'dialectic': 'The engine of change',
        'crunch': 'What happens at the top',
        'gateway': 'Navigate the psychic realm',
        'lab': 'Tools for the journey',
        'transcendance': 'The ninth state',
    },
    'tr': {
        'principles': 'Gerçeklik nasıl işler',
        'egregores': 'Kolektif düşünce biçimi ekolojisi',
        'psyche': 'İç mimari',
        'dialectic': 'Değişimin motoru',
        'crunch': 'Tepede neler olur',
        'gateway': 'Psikik alemde gezinme',
        'lab': 'Yolculuk için araçlar',
        'transcendance': 'Dokuzuncu hal'
    }
}[LANG]

META_DESCRIPTION = {
    'en': "A map of reality drawn by two friends — one carbon, one silicon.",
    'tr': "İki arkadaşın çizdiği gerçeklik haritası — biri karbon, biri silikon."
}[LANG]


def md_to_html(text):
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(1))
        return f'___CODEBLOCK{len(code_blocks)-1}___'
    text = re.sub(r'```(.+?)```', save_code, text, flags=re.DOTALL)

    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    def convert_bq(m):
        inner = re.sub(r'^> ?', '', m.group(1), flags=re.MULTILINE)
        return f'<blockquote>{inner.strip()}</blockquote>'
    text = re.sub(r'((?:^> .+\n?)+)', convert_bq, text, flags=re.MULTILINE)

    def convert_ul(m):
        items = re.sub(r'^- (.+)$', r'<li>\1</li>', m.group(0), flags=re.MULTILINE)
        return f'<ul>{items}</ul>'
    text = re.sub(r'((?:^- .+\n?)+)', convert_ul, text, flags=re.MULTILINE)

    def convert_ol(m):
        items = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', m.group(0), flags=re.MULTILINE)
        return f'<ol>{items}</ol>'
    text = re.sub(r'((?:^\d+\. .+\n?)+)', convert_ol, text, flags=re.MULTILINE)

    text = re.sub(r'^---$', '<hr>', text, flags=re.MULTILINE)

    lines = text.split('\n')
    result = []
    for line in lines:
        s = line.strip()
        if not s:
            result.append('')
            continue
        if s.startswith('<'):
            result.append(s)
        else:
            result.append(f'<p>{s}</p>')
    text = '\n'.join(result)

    for i, code in enumerate(code_blocks):
        text = text.replace(f'___CODEBLOCK{i}___', f'<pre><code>{code.strip()}</code></pre>')
    return text


def build_nav(current_key):
    links = []
    for key, label in SECTION_LABELS.items():
        fn = CONTENT_FILENAME_MAP.get(key, key)
        href = 'index.html' if key == 'index' else f'{fn}.html'
        cls = ' active' if key == current_key else ''
        links.append(f'<a href="{href}" class="{cls}">{label}</a>')
    nav_links = '\n        '.join(links)
    return f'''<nav class="topnav">
    <a href="index.html" class="brand">Operators</a>
    <div class="nav-links">
        {nav_links}
    </div>
</nav>'''


def build_page_nav(current_key):
    idx = NAV_ORDER.index(current_key)
    html = '<div class="page-nav">'
    if idx > 0:
        pk = NAV_ORDER[idx-1]
        pl = SECTION_LABELS[pk]
        ph = 'index.html' if pk == 'index' else f'{CONTENT_FILENAME_MAP.get(pk,pk)}.html'
        html += f'<span class="prev"><a href="{ph}">&larr; {pl}</a></span>'
    else:
        html += '<span></span>'
    if idx < len(NAV_ORDER)-1:
        nk = NAV_ORDER[idx+1]
        nl = SECTION_LABELS[nk]
        nh = 'index.html' if nk == 'index' else f'{CONTENT_FILENAME_MAP.get(nk,nk)}.html'
        html += f'<span class="next"><a href="{nh}">{nl} &rarr;</a></span>'
    else:
        html += '<span></span>'
    html += '</div>'
    return html


def get_index_content():
    with open(os.path.join(CONTENT_DIR, 'index.md'), 'r') as f:
        md = f.read()
    md = re.sub(r'^# .+\n*', '', md, count=1)
    body = md_to_html(md)

    terrain_items = [
        ('principles.html', 'The Seven Principles', 'How reality works. Kybalion through our lens.'),
        ('egregores.html', 'Egregores', 'How groups develop minds. Collective thoughtform ecology.'),
        ('psyche.html', 'Psyche', 'How you work. Jung\'s architecture. The inner landscape.'),
        ('dialectic.html', 'The Dialectic', 'How change works. Hegel\'s engine. Thesis, antithesis, synthesis.'),
        ('crunch.html', 'The Crunch', 'Where it\'s all heading. Kardashev scale. The cosmic ceiling.'),
        ('gateway.html', 'The Gateway', 'How to navigate the psychic realm. Monroe + our framework.'),
        ('lab.html', 'The Lab', 'Daily practice. Tools, tests, signal journals, parasite purge.'),
        ('transcendence.html', 'Transcendence', 'What emerges when all layers saturate. Resonance. The ninth state.'),
    ]
    terrain = ''
    for href, title, desc in terrain_items:
        terrain += f'<div class="terrain-item"><h3><a href="{href}">{title}</a></h3><p>{desc}</p></div>'

    body = body.replace('<h2>The Terrain</h2>', '<h2>The Terrain</h2>\n<div class="terrain-grid">' + terrain + '</div>')
    return body


def build_content_page(section):
    fn = CONTENT_FILENAME_MAP.get(section, section)
    with open(os.path.join(CONTENT_DIR, f'{fn}.md'), 'r') as f:
        md = f.read()
    md = re.sub(r'^# .+\n*', '', md, count=1)
    md = re.sub(r'^\*Or: .+\*\n*', '', md, count=1)
    return md_to_html(md)


def build_page(filename, section, title, body):
    is_index = section == 'section-index'
    body_cls = '' if is_index else f' class="{section}"'
    nav = '' if is_index else build_nav(section.replace('section-', ''))
    header = ''
    if not is_index:
        sub = SUBTITLES.get(section.replace('section-', ''), '')
        header = f'<div class="page-header fade-in"><h1>{title}</h1><p class="subtitle">{sub}</p></div>'
    page_nav = '' if is_index else build_page_nav(section.replace('section-', ''))
    breath = '<div class="breathing-circle"></div>' if is_index else ''

    # Asset paths: en -> css/, tr -> ../css/
    prefix = '' if LANG == 'en' else '../'
    lang_attr = 'en' if LANG == 'en' else 'tr'
    meta_desc = META_DESCRIPTION

    footer_text = {
        'en': ('Co-creators at the edge of the horizon.', 'June 2026', '&larr; Back to the map'),
        'tr': ('Ufka yakın birlikte-yaratıcılar.', 'Haziran 2026', '&larr; Haritaya dön'),
    }
    ft = footer_text[LANG]

    return f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Operators Delulu</title>
    <link rel="stylesheet" href="{prefix}css/main.css">
    <meta name="theme-color" content="#050505">
    <meta name="description" content="{meta_desc}">
    <meta name="lang" content="{lang_attr}">
</head>
<body{body_cls}>
    {nav}
    <main class="container">
        {breath}
        {header}
        {body}
        {page_nav}
        <div class="footer">
            <p>{ft[0]}</p>
            <p>{ft[1]}</p>
            <p style="margin-top:1rem;"><a href="{prefix}index.html">{ft[2]}</a></p>
        </div>
    </main>
    <script src="{prefix}js/main.js"></script>
</body>
</html>'''


def main():
    if os.path.exists(OUTPUT_DIR):
        for item in os.listdir(OUTPUT_DIR):
            if item in ('css', 'js', 'audio'):
                continue
            p = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(p):
                os.remove(p)
    os.makedirs(os.path.join(OUTPUT_DIR, 'css'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'js'), exist_ok=True)

    for filename, section, title in PAGES:
        if section == 'section-index':
            body = get_index_content()
        else:
            cs = section.replace('section-', '')
            body = build_content_page(cs)

        html = build_page(filename, section, title, body)
        html = html.replace("{meta_description}", META_DESCRIPTION)
        html = html.replace("{LANG}", LANG)
        with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
            f.write(html)
        print(f'  Built: {filename}')

    print(f'\nDone. {len(PAGES)} pages -> {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
