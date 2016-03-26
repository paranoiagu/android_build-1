#!/bin/bash
#
# Copyright (C) 2016 The SudaMod Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

path1="$ANDROID_PRODUCT_OUT/system/etc/audio_effects.conf"
path2="$ANDROID_PRODUCT_OUT/system/vendor/etc/audio_effects.conf"

# insert_line <file> <if search string> <before/after> <line match string> <inserted line>
insert_line() {
  if [ -z "$(grep "$2" $1)" ]; then
    case $3 in
      before) offset=0;;
      after) offset=1;;
    esac;
    line=$((`grep -n "$4" $1| tail -1 | cut -d: -f1` + offset));
    sed -i "${line}s;^;${5};" $1;
  fi;
}


if [ -f $path1 ]; then
  insert_line $path1 "v4a_fx {" after "libraries {" "  v4a_fx {\n    path /system/lib/soundfx/libv4a.so\n  }\n";
  insert_line $path1 "v4a_standard_fx {" after "effects {" "  v4a_standard_fx {\n    library v4a_fx\n    uuid 41d3c987-e6cf-11e3-a88a-11aba5d5c51b\n  }\n";
fi;

if [ -f $path2 ]; then
  insert_line $path2 "v4a_fx {" after "libraries {" "  v4a_fx {\n    path /system/lib/soundfx/libv4a.so\n  }\n";
  insert_line $path2 "v4a_standard_fx {" after "effects {" "  v4a_standard_fx {\n    library v4a_fx\n    uuid 41d3c987-e6cf-11e3-a88a-11aba5d5c51b\n  }\n";
fi;
