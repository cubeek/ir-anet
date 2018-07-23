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

import functools

from ovs.db import idl
from ovsdbapp.backend.ovs_idl import connection
from ovsdbapp.backend.ovs_idl import idlutils
from ovsdbapp.schema.open_vswitch import helpers
from ovsdbapp.schema.open_vswitch import impl_idl

_idl = None
OVSDB_CONNECTION = 'tcp:127.0.0.1:6640'


enable_connection_uri = functools.partial(
    helpers.enable_connection_uri, OVSDB_CONNECTION)


def idl_factory(conn, schema):
    helper = idlutils.get_schema_helper(conn, schema)
    helper.register_all()

    return idl.Idl(conn, helper)


def get_idl_singleton():
    global _idl

    conn = OVSDB_CONNECTION
    schema = "Open_vSwitch"

    if _idl is None:
        _connection = connection.Connection(
            idl=idl_factory(conn, schema),
            timeout=10)
        _idl = impl_idl.OvsdbIdl(_connection)

    return _idl
