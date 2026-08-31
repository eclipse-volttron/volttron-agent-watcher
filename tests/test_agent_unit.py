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


@pytest.fixture
def mock_agent():
    agent = object.__new__(AgentWatcher)
    agent.watchlist = []
    agent.check_period = 10
    agent.schedule_event = None
    agent.vip = MagicMock()
    agent.core = MagicMock()
    return agent


def test_config_add(mock_agent):
    """Test that _config_add sets watchlist, period, and schedules periodic task."""
    mock_event = MagicMock()
    mock_agent.core.schedule.return_value = mock_event

    config = {"watchlist": ["agent.a", "agent.b"], "check-period": 5}
    mock_agent._config_add("config", "NEW", config)

    assert mock_agent.watchlist == ["agent.a", "agent.b"]
    assert mock_agent.check_period == 5
    assert mock_agent.schedule_event == mock_event
    mock_agent.core.schedule.assert_called_once()


def test_config_add_cancels_existing_schedule(mock_agent):
    """Test that _config_add cancels existing schedule if called again."""
    old_event = MagicMock()
    new_event = MagicMock()
    mock_agent.schedule_event = old_event
    mock_agent.core.schedule.return_value = new_event

    config = {"watchlist": ["agent.c"], "check-period": 3}
    mock_agent._config_add("config", "NEW", config)

    old_event.cancel.assert_called_once()
    assert mock_agent.schedule_event == new_event
    assert mock_agent.watchlist == ["agent.c"]


def test_config_mod(mock_agent):
    """Test that _config_mod cancels old schedule and reschedules with new parameters."""
    old_event = MagicMock()
    new_event = MagicMock()
    mock_agent.schedule_event = old_event
    mock_agent.core.schedule.return_value = new_event

    updated_config = {"watchlist": ["agent.x"], "check-period": 2}
    mock_agent._config_mod("config", "UPDATE", updated_config)

    old_event.cancel.assert_called_once()
    assert mock_agent.watchlist == ["agent.x"]
    assert mock_agent.check_period == 2
    assert mock_agent.schedule_event == new_event


def test_config_del(mock_agent):
    """Test that _config_del clears watchlist and cancels the schedule event."""
    mock_event = MagicMock()
    mock_agent.schedule_event = mock_event
    mock_agent.watchlist = ["agent.a"]

    mock_agent._config_del("config", "DELETE", {})

    assert mock_agent.watchlist == []
    assert mock_agent.check_period == 10
    mock_event.cancel.assert_called_once()
    assert mock_agent.schedule_event is None


def test_watch_agents_with_missing(mock_agent):
    """Test watch_agents triggers health alert when watched agents are missing."""
    mock_agent.watchlist = ["agent.present", "agent.missing"]
    mock_get = MagicMock()
    mock_get.get.return_value = ["agent.present", "platform.control"]
    mock_agent.vip.peerlist.return_value = mock_get

    mock_agent.watch_agents()

    mock_agent.vip.health.send_alert.assert_called_once()
    call_args = mock_agent.vip.health.send_alert.call_args[0]
    assert call_args[0] == "AgentWatcher"
    assert "agent.missing" in call_args[1].context


def test_watch_agents_all_present(mock_agent):
    """Test watch_agents does not send alert when all watched agents are present."""
    mock_agent.watchlist = ["agent.present", "platform.control"]
    mock_get = MagicMock()
    mock_get.get.return_value = ["agent.present", "platform.control"]
    mock_agent.vip.peerlist.return_value = mock_get

    mock_agent.watch_agents()

    mock_agent.vip.health.send_alert.assert_not_called()
