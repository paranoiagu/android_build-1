#!/usr/bin/env python
import tempfile
import os
import shutil
import sys

LIB = ('  v4a_fx {\n'
       '    path /system/lib/soundfx/libv4a.so\n'
       '  }\n')
EFFECT = ('  v4a_standard_fx {\n'
          '    library v4a_fx\n'
          '    uuid 41d3c987-e6cf-11e3-a88a-11aba5d5c51b\n'
          '  }\n')
VAR = 'ANDROID_PRODUCT_OUT'
PATHS = ['system/etc/audio_effects.conf',
         'system/vendor/etc/audio_effects.conf']

def parse_file(filename, header, sub, addition):
    start = ''
    content = ''
    end = ''
    count = 0
    f = open(filename, 'r')

    while True:
        line = f.readline()
        check = line.lstrip(' ')
        if header in check and not check.startswith('#'):
            count += 1
            start += line
            break
        elif not check:
            break
        else:
            start += line

    if count == 0:
        raise ValueError('No "{0}" declaration found'.format(header))

    while count > 0:
        line = f.readline()
        check = line.lstrip(' ')
        if sub in check and not check.startswith('#'):
            return
        elif '{' in check and not check.startswith('#'):
            count += 1
            content += line
        elif '}' in check and not check.startswith('#'):
            count -= 1
            if count == 0:
                end += line
            else:
                content += line
        elif not check:
            break
        else:
            content += line

    end += f.read()
    if count != 0:
        raise ValueError('Malformed config file')
    else:
        content += addition

    output = tempfile.NamedTemporaryFile(delete = False, mode = 'w')
    output.write(start + content + end)
    output.close()
    f.close()

    return output.name

def main():

    # Determine output directory
    base = os.getenv(VAR)
    if not base:
        raise ValueError('Cannot determine output directory')

    for i in PATHS:
        # Form output path
        filename = os.path.join(base, i)

        # Skip if file does not exist
        if not os.path.isfile(filename):
            continue

        # Start parsing and add lines
        tmp = parse_file(filename, 'libraries {', 'v4a_fx', LIB)
        if tmp:
            final = parse_file(tmp, 'effects {', 'v4a_standard_fx', EFFECT)
        else:
            continue
        # Copy to output destination
        shutil.copy(final, filename)

        # Clean up
        os.remove(tmp)
        os.remove(final)
main()
