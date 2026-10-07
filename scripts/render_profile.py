"""Render self-contained, theme-aware profile banners using only Python's stdlib."""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'light': {'ink': '#1f2328', 'accent': '#59636e',
              'rule': '#d1d9e0', 'detail': '#59636e', 'frame': '#d1d9e0'},
    'dark': {'ink': '#f0f6fc', 'accent': '#9198a1',
             'rule': '#3d444d', 'detail': '#9198a1', 'frame': '#3d444d'},
}

def text(x, y, value, size, color, *, family='Arial, Helvetica, sans-serif', weight='400', spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing is not None else ''
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}"{extra}>{html.escape(value)}</text>')

def medal(x, y, color):
    return (f'<g transform="translate({x} {y})" fill="none" stroke="{color}" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="11" cy="8" r="6"/><path d="M7 13L5 24l6-4 6 4-2-11"/></g>')

def image_uri(path):
    content = path.read_bytes()
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        mime = 'image/png'
    elif content.startswith(b'\xff\xd8\xff'):
        mime = 'image/jpeg'
    elif content.startswith(b'RIFF') and content[8:12] == b'WEBP':
        mime = 'image/webp'
    else:
        raise ValueError('The portrait must contain a PNG, JPEG, or WebP image.')
    return f'data:{mime};base64,{base64.b64encode(content).decode("ascii")}'

def render(profile, palette, portrait, mobile):
    p = palette
    width, height = (560, 556) if mobile else (1000, 410)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
             f'<title id="title">{html.escape(profile["name"])} — AI Systems</title>',
             '<desc id="description">Portrait with Dean’s List and Departmental Honors Scholarship honors for Spring 2026.</desc>']
    if mobile:
        px, py, pw, ph, name_x = 34, 34, 136, 181.333, 197
        honors_x, honors_y, award_y, rule_y, second_y = 36, 273, 310, 389, 417
        heading_size, detail_size = 23, 19
        eyebrow_size, title_size = 15, 55
    else:
        px, py, pw, ph, name_x = 38, 59, 222, 296, 302
        honors_x, honors_y, award_y, rule_y, second_y = name_x, 190, 221, 282, 304
        heading_size, detail_size = 20, 16
        eyebrow_size, title_size = 13, 67
    parts.extend([
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="{p["frame"]}"/>',
        f'<image x="{px+8}" y="{py+8}" width="{pw-16}" height="{ph-16}" preserveAspectRatio="xMidYMid slice" href="{portrait}"/>',
        text(name_x, 74 if mobile else 70, profile['eyebrow'], eyebrow_size, p['accent'], family='Consolas, monospace', spacing='1.8'),
    ])
    if mobile:
        pieces = profile['name'].rsplit(' ', 1)
        for index, piece in enumerate(pieces):
            parts.append(text(name_x, 137+index*62, piece, title_size, p['ink'], family='Georgia, Times New Roman, serif'))
    else:
        parts.append(text(name_x, 145, profile['name'], title_size, p['ink'], family='Georgia, Times New Roman, serif'))
    parts.append(text(honors_x, honors_y, profile['honors_term'], 14 if mobile else 12, p['accent'], family='Consolas, monospace', spacing='1.5'))
    for index, award in enumerate(profile['awards']):
        y = award_y if index == 0 else second_y
        parts.append(medal(honors_x, y-2, p['accent']))
        tx = honors_x + 36
        title_lines = ['Departmental Honors', 'Scholarship - 2026 Spring'] if mobile and award['name'] == 'Departmental Honors Scholarship - 2026 Spring' else [award['name']]
        for offset, line in enumerate(title_lines):
            parts.append(text(tx, y+16+offset*28, line, heading_size, p['ink'], weight='600'))
        if award.get('detail'):
            parts.append(text(tx, y+43+(len(title_lines)-1)*28, award['detail'], detail_size, p['detail']))
        if index == 0:
            parts.append(f'<path d="M{honors_x} {rule_y}H{width-36}" stroke="{p["rule"]}"/>')
    parts.append('</svg>')
    output = '\n'.join(parts) + '\n'
    ET.fromstring(output)
    return output

def main():
    profile = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
    photo_path = (ROOT / profile['photo']).resolve()
    if not photo_path.is_relative_to(ROOT):
        raise ValueError('Portrait must be inside this repository.')
    if len(profile['awards']) != 2:
        raise ValueError('This layout expects exactly two awards.')
    portrait = image_uri(photo_path)
    for theme, palette in PALETTES.items():
        for mobile in (False, True):
            suffix = '-mobile' if mobile else ''
            target = ROOT / 'assets' / f'header-honors-{theme}{suffix}.svg'
            target.write_text(render(profile, palette, portrait, mobile), encoding='utf-8')
            print(target.relative_to(ROOT))

if __name__ == '__main__':
    main()
