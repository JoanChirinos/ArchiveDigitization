#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ArchiveDigitization/ArchiveDigitization/")
sys.path.insert(1,"/var/www/ArchiveDigitization/")

from ArchiveDigitization import app as application
