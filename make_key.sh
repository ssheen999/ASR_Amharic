#!usr/bin/env/bash

awk -F";" '{printf("%s\n", $2)}' mainkey.key | sed 's|./target//audio/||' > key

