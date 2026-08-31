# -*- coding: utf-8 -*- {{{
# ===----------------------------------------------------------------------===
#
#                 Installable Component of Eclipse VOLTTRON
#
# ===----------------------------------------------------------------------===
#
# Copyright 2024 Battelle Memorial Institute
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ===----------------------------------------------------------------------===
# }}}

import logging

from volttron import utils
from volttron.client.messaging.health import STATUS_BAD, Status
from volttron.client.vip.agent import Agent, Core
from volttron.utils.scheduling import periodic


_log = logging.getLogger(__name__)

__version__ = '0.1'


class AgentWatcher(Agent):

    def __init__(self, config_path, **kwargs):
        super(AgentWatcher, self).__init__(**kwargs)
        config = utils.load_config(config_path)
        self.watchlist = []
        self.check_period = 10
        self.schedule_event = None
        self.vip.config.set_default("config", config)
        self.vip.config.subscribe(self._config_add, actions="NEW", pattern="config")
        self.vip.config.subscribe(self._config_del, actions="DELETE", pattern="config")
        self.vip.config.subscribe(self._config_mod, actions="UPDATE", pattern="config")

    def _config_add(self, config_name, action, contents):
        self.watchlist = contents.get("watchlist", [])
        self.check_period = contents.get("check-period", 10)
        if self.schedule_event:
            self.schedule_event.cancel()
            self.schedule_event = None
        self.schedule_event = self.core.schedule(periodic(self.check_period), self.watch_agents)

    def _config_del(self, config_name, action, contents):
        self.watchlist = []
        self.check_period = 10
        if self.schedule_event:
            self.schedule_event.cancel()
            self.schedule_event = None

    def _config_mod(self, config_name, action, contents):
        self.watchlist = contents.get("watchlist", [])
        self.check_period = contents.get("check-period", 10)
        if self.schedule_event:
            self.schedule_event.cancel()
            self.schedule_event = None
        self.schedule_event =self.core.schedule(periodic(self.check_period), self.watch_agents)

    def watch_agents(self):
        peerlist = self.vip.peerlist().get()
        _log.info("Peerlist: {}".format(peerlist))
        missing_agents = []
        for vip_id in self.watchlist:
            if vip_id not in peerlist:
                missing_agents.append(vip_id)

        if missing_agents:
            alert_key = "AgentWatcher"
            context = "Agent(s) expected but but not running {}".format(missing_agents)
            _log.warning(context)
            status = Status.build(STATUS_BAD, context=context)
            self.vip.health.send_alert(alert_key, status)


def main():
    utils.vip_main(AgentWatcher, version=__version__)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
