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


import libvirt
from lxml import etree

LIBVIRT_CONN = None
SUPPORTED_NETWORKS = ('network', 'bridge')


class NotFound(Exception):
    pass


class DomainDict(dict):
    def __init__(self):
        self.update({
            'undercloud': [],
            'controller': [],
            'compute': [],
            'anet': [],
        })

    def add(self, value):
        try:
            self[value.type].append(value)
        except KeyError:
            print("Unknown domain %s, ignoring ..." % value.type)


class Domain(object):
    def __init__(self, domain):
        self.domain = domain
        self.name = domain.name()
        self.type = self.name.split('-')[0]
        self.domxml = None
        self.interfaces = []

    def load_xml_definition(self):
        self.domxml = etree.fromstring(self.domain.XMLDesc())
        self.interfaces = [
            interface_factory(iface) 
            for iface in self.domxml.findall('./devices/interface')
            if iface.attrib['type'] in SUPPORTED_NETWORKS]

    def get_interface_by_network(self, network_name):
        for iface in self.interfaces:
            if iface.network == network_name:
                return iface
        raise NotFound("Network %s was not found")

    def __repr__(self):
        return "<%s %s: %s>" % (self.type ,self.name, self.interfaces)


class Interface(object):
    def __init__(self, interface):
        self.mac = interface.find('./mac').attrib['address']
        self.device = interface.find('./target').attrib['dev']

    def __repr__(self):
        return "<interface %s %s>" % (self.device, self.mac)

    __str__ = __repr__


class BridgeInterface(Interface):
    def __init__(self, interface):
        super(BridgeInterface, self).__init__(interface)
        self.bridge = interface.find('./source').attrib['bridge']

    def __repr__(self):
        return "<bridge %s %s %s>" % (
            self.bridge, self.mac, self.device)


class NetworkInterface(Interface):
    def __init__(self, interface):
        super(NetworkInterface, self).__init__(interface)
        self.network = interface.find('./source').attrib['network']
        self.bridge = interface.find('./source').attrib['bridge']

    def __repr__(self):
        return "<network %s %s %s %s>" % (
            self.network, self.mac, self.bridge, self.device)


TYPE_TO_IFACE = {
    "network": NetworkInterface,
    "bridge": BridgeInterface,
}


def interface_factory(interface):
    return TYPE_TO_IFACE[interface.attrib['type']](interface)


def get_libvirt_connetion():
    global LIBVIRT_CONN

    if LIBVIRT_CONN is None:
        LIBVIRT_CONN = libvirt.openReadOnly()
    return LIBVIRT_CONN


def get_domains():
    domains = DomainDict()
    conn = get_libvirt_connetion()
    for libv_domain in conn.listAllDomains():
        domain = Domain(libv_domain)
        domains.add(domain)
        domain.load_xml_definition()

    return domains
