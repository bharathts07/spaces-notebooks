#!/usr/bin/env python3
import os
import re
import sys
import tomllib


def kebab_case(string):
    # Naive implementation of kebab case to find icon names from lesson areas
    return re.sub(r'[^a-zA-Z0-9]+', '-', string.strip()).lower()


def error(msg):
    print('ERROR:', msg, file=sys.stderr)
    sys.exit(1)


for f in sys.argv[1:]:

    with open(f, 'r') as infile:
        info = tomllib.loads(infile.read())

    if 'meta' not in info:
        error(f'No `meta` section in `{f}`')

    # The meta section requires, title, description, and icon
    meta = info['meta']

    if 'title' not in meta:
        error(f'No `title` in `meta` section of {f}')

    if 'description' not in meta:
        error(f'No `description` in `meta` section of {f}')

    # Authors must be a non-empty list
    if (
        'authors' not in meta
        or not isinstance(meta['authors'], list)
        or not meta['authors']
    ):
        error(f'No `authors` in `meta` section of {f}')

    if 'icon' not in meta:
        error(f'No `icon` in `meta` section of {f}')

    if 'minimum_tier' not in meta:
        error(
            f'No `minimum_tier` in `meta` section of {f}; '
            f'it must be set to "free-shared" or "standard"',
        )

    if meta['minimum_tier'] not in ['free-shared', 'standard']:
        error(
            f'`minimum_tier` in `meta` section of {f} '
            f'must be set to "free-shared" or "standard"',
        )

    if 'lesson_areas' not in meta:
        error(
            f'No `lesson_areas` in `meta` section of {f}; '
            f'it must be an array of strings (can be empty)',
        )

    if not isinstance(meta['lesson_areas'], list):
        error(
            f'`lesson_areas` in `meta` section of {f} must be a list',
        )

    # Tags must be all lower-case, ascii letters
    tags = meta.get('tags', [])

    if [x.lower() for x in tags] != tags:
        error(f'Tags must be in all lower-case ({tags}) in {f}')

    if [re.sub(r'[^a-z0-9]', r'', x) for x in tags] != tags:
        error(f'Tags can only contain letters and numbers ({tags}) in {f}')

    if len(tags) != len(set(tags)):
        error(f'Duplicate tag found ({tags}) in {f}')

    # Currently only "spaces" is allowed in destinations
    destinations = meta.get('destinations', [])

    if destinations and [x for x in destinations if x != 'spaces']:
        error(f'Only "spaces" is allowed in `destinations` in {f}')

    card_icons = os.listdir('common/images/card-header-icons')
    preview_icons = os.listdir('common/images/preview-header-icons')

    for lesson_area in meta['lesson_areas']:
        expected_icon_name = f'{kebab_case(lesson_area)}.png'
        if expected_icon_name not in card_icons:
            error(f'Lesson area {lesson_area} not found in card icons')
        if expected_icon_name not in preview_icons:
            error(f'Lesson area {lesson_area} not found in preview icons')

    # Authors must have a corresponding author entry
    author_meta_files = os.listdir('authors')
    for author in meta['authors']:
        author_filename = f'{author}.toml'
        if author_filename not in author_meta_files:
            error(f'Author {author} does not have a corresponding author entry in {f}')
