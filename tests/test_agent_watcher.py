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

from unittest.mock import MagicMock
import pytest
from agent_watcher.agent import AgentWatcher


def test_agent_watcher_lifecycle_and_config_store():
    """Test full agent watcher lifecycle with config store NEW, UPDATE, DELETE actions."""
    agent = object.__new__(AgentWatcher)
    agent.watchlist = []
    agent.check_period = 10
    agent.schedule_event = None
    agent.vip = MagicMock()
    agent.core = MagicMock()

    alerts_sent = []

    def mock_send_alert(key, status):
        alerts_sent.append((key, status))

    agent.vip.health.send_alert.side_effect = mock_send_alert

    # 1. Simulate NEW config action from config store
    initial_config = {"watchlist": ["listener", "actuator"], "check-period": 5}
    agent._config_add("config", "NEW", initial_config)
    assert agent.watchlist == ["listener", "actuator"]
    assert agent.check_period == 5
    assert agent.schedule_event is not None

    # 2. Simulate watch_agents execution when both agents are running
    mock_peerlist = MagicMock()
    mock_peerlist.get.return_value = ["listener", "actuator", "platform.control"]
    agent.vip.peerlist.return_value = mock_peerlist

    agent.watch_agents()
    assert len(alerts_sent) == 0

    # 3. Simulate watch_agents when 'actuator' goes missing
    mock_peerlist.get.return_value = ["listener", "platform.control"]
    agent.watch_agents()
    assert len(alerts_sent) == 1
    assert "actuator" in alerts_sent[0][1].context

    # 4. Simulate UPDATE config action with a single watched agent
    updated_config = {"watchlist": ["listener"], "check-period": 2}
    agent._config_mod("config", "UPDATE", updated_config)
    assert agent.watchlist == ["listener"]
    assert agent.check_period == 2

    # Verify watch_agents with updated watchlist (listener is present)
    alerts_sent.clear()
    agent.watch_agents()
    assert len(alerts_sent) == 0

    # 5. Simulate DELETE config action
    agent._config_del("config", "DELETE", {})
    assert agent.watchlist == []
    assert agent.schedule_event is None
