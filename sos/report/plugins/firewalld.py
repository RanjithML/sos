# Copyright (C) 2014 Red Hat, Inc. Jamie Bainbridge <jbainbri@redhat.com>
# Copyright (C) 2014 Red Hat, Inc. Bryn M. Reeves <bmr@redhat.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin


class FirewallD(Plugin, RedHatPlugin):

    short_desc = 'Firewall daemon'

    plugin_name = 'firewalld'
    profiles = ('network',)

    packages = ('firewalld',)

    def setup(self):

        self.add_copy_spec("/etc/firewalld/firewalld.conf",
                           tags='firewalld_conf')

        self.add_copy_spec([
            "/etc/firewalld/*.xml",
            "/etc/firewalld/icmptypes/*.xml",
            "/etc/firewalld/services/*.xml",
            "/etc/firewalld/zones/*.xml",
            "/etc/firewalld/ipsets/*.xml",
            "/etc/firewalld/policies/*.xml",
            "/etc/firewalld/helpers/*.xml",
            "/etc/sysconfig/firewalld",
            "/var/log/firewalld",
        ])

        # use a 10s timeout to workaround dbus problems in
        # docker containers.
        self.add_cmd_output([
            "firewall-cmd --direct --get-all-chains",
            "firewall-cmd --direct --get-all-rules",
            "firewall-cmd --direct --get-all-passthroughs",
            "firewall-cmd --get-log-denied",
            "firewall-cmd --list-all-zones",
            "firewall-cmd --permanent --list-all-zones",
            "firewall-cmd --list-all-policies",
            "firewall-cmd --permanent --list-all-policies",
            "firewall-cmd --permanent --direct --get-all-chains",
            "firewall-cmd --permanent --direct --get-all-rules",
            "firewall-cmd --permanent --direct --get-all-passthroughs",
            "firewall-cmd --state"
        ], timeout=10, cmd_as_tag=True)

# vim: set et ts=4 sw=4 :
