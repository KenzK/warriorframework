'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

"""Warrior Network diagnostics module """
import re
from Framework.ClassUtils.WNetwork.base_class import Base
from Framework.Utils import  cli_Utils
from Framework.Utils.testcase_Utils import pNote
class Diag(Base):
    """Warrior Diagnostics class """

    def __init__(self, *args, **kwargs):
        """ Constructor """
        super(Diag, self).__init__(*args, **kwargs)

    @staticmethod
    def ping_from_remotehost(session_object, ip_type,
                             dest_address, prompt, count):
        """ping  to dest_system from remote host

        :Arguments:
            1. session_object(string)  = expect session object
            2. command(string) = command to be executed
            3. ip_type = ip/ipv6/dns
            4. dest_address(string) = ip or dns name
            3. prompt(string) = prompt

        :Returns:
            1. bool (True/False)

        """

        ping_cmd = "ping"
        if ip_type == "ipv6":
            ping_cmd = "ping6"

        command = ping_cmd +" -c {} {}".format(count, dest_address)

        output = cli_Utils.send_command_and_get_response(session_object, ".*",
                                                         prompt, command)

        linux_res = re.search(r'[1-9][0-9]* received', output)
        solaris_res = re.search(r'alive', output)
        if linux_res or solaris_res :
            pNote("ping successfully completed")
            status = True
        else:
            pNote("ping command failed ")
            status = False

        return status

    @staticmethod
    def traceroute_from_remotehost(session_object, ip_type, dest_address,
                                   prompt):
        """traceroute to dest_system from remote host

        :Arguments:
            1. session_object(string)  = expect session object
            2. command(string) = command to be executed
            3. ip_type = ip/ipv6/dns
            4. dest_address(string) = ip or dns name
            3. prompt(string) = prompt

        :Returns:
            1. bool (True/False)

        """
        traceroute_cmd = "traceroute"
        if ip_type == "ipv6":
            traceroute_cmd = "traceroute6"

        command = traceroute_cmd +" {}".format(dest_address)

        output = cli_Utils.send_command_and_get_response(session_object, ".*",
                                                         prompt, command)
        if not isinstance(output, str):
            pNote("traceroute command returned invalid value", "error")
            return False

        output_list = output.split("\n")
        for output in output_list:
            match = re.search(r'^ *(\d+) .*?'+dest_address, output)
            if match:
                break
        if match:
            pNote("Traceroute completed in {} hop".format(match.group(1)))
            status = True
        else:
            status = False
            pNote("Traceroute failed", "error")

        return status

