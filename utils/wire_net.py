# Copyright 2018 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse

import libvirtwrap
import ovsdb


def parse_args():
    parser = argparse.ArgumentParser()

    return parser.parse_args()


def main():
    args = parse_args()
    domains = libvirtwrap.get_domains()
    try:
        idl = ovsdb.get_idl_singleton()
    except Exception:
        ovsdb.enable_connection_uri()
        idl = ovsdb.get_idl_singleton()


if __name__ == "__main__":
    main()

