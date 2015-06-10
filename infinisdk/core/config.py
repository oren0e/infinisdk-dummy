###!
### Infinidat Ltd.  -  Proprietary and Confidential Material
###
### Copyright (C) 2014, 2015, Infinidat Ltd. - All Rights Reserved
###
### NOTICE: All information contained herein is, and remains the property of Infinidat Ltd.
### All information contained herein is protected by trade secret or copyright law.
### The intellectual and technical concepts contained herein are proprietary to Infinidat Ltd.,
### and may be protected by U.S. and Foreign Patents, or patents in progress.
###
### Redistribution and use in source or binary forms, with or without modification,
### are strictly forbidden unless prior written permission is obtained from Infinidat Ltd.
###!
import os

from .._compat import ConfigParser

import confetti
from packaging.specifiers import SpecifierSet

config = confetti.Config(dict(

    check_version_compatibility=True,

    ini_file_path="~/.infinidat/infinisdk.ini",

    defaults=dict(
        system_api_port=80,
        retry_sleep_seconds=5,
    ),
    izbox=dict(
        defaults=dict(
            system_api=dict(
                timeout_seconds=180,
            ),
            events=dict(
                page_size=1000,
                max_events=10 ** 6,
                max_page_size=1000),
        ),
        approval_required_codes=tuple((
            "DANGEROUS_OPERATION",
        )),
    ),
    infinibox=dict(

        compatible_versions = [
            SpecifierSet(">=1.5"),
        ],

        defaults=dict(
            system_api=dict(
                timeout_seconds=30,
            ),
            enlosure_drives=dict(
                total_count=dict(mock=0, simulator=480),
            ),
        ),
        approval_required_codes=tuple((
            "APPROVAL_REQUIRED",
            "APPROVAL_REQUIRED_VOLUME_HAS_CHILDREN",
        )),
    ),
))

_cached_ini_parser = None

def get_ini_option(section, option, default=None):
    global _cached_ini_parser
    if _cached_ini_parser is None:
        _cached_ini_parser = ConfigParser()
        _cached_ini_parser.read(os.path.expanduser((config.root.ini_file_path)))

    if _cached_ini_parser.has_option(section, option):
        return _cached_ini_parser.get(section, option)
    return default
