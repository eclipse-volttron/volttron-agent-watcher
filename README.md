# volttron-agent-watcher

The VOLTTRON Agent Watcher is used to monitor agents running on a VOLTTRON instance. Specifically it monitors whether a set of
VIP identities (peers) are connected to the instance. If any of the peers in the set are not present then an alert will
be sent.

## Requires

* python >= 3.10
* volttron >= 10.0

## Installation

Before installing, VOLTTRON should be installed and running.  Its virtual environment should be active.
Information on how to install of the VOLTTRON platform can be found
[here](https://github.com/eclipse-volttron/volttron-core).

Create a directory called `config` and use the change directory command to enter it.

```shell
mkdir config
cd config
```

After entering the config directory, create a file called `agentwatcher.json`, use the below JSON to populate your new file.

The agent has two configuration values:

* watchlist: a list of VIP identities to watch on the platform instance
* check-period: interval in seconds between the agent watcher checking the platform peerlist and publishing alerts

The agent watcher requires other agents to watch. In the below example, we are watching the platform.driver and platform.actuator.

In your config add the following JSON.

```json
{
    "watchlist": [
        "platform.driver",
        "platform.actuator"
    ],
    "check-period": 10
}
```

Install and start the agent watcher in VOLTTRON.

```shell
vctl install volttron-agent-watcher --agent-config agentwatcher.json --vip-identity platform.agent_watcher --start --force
```

View the status of the installed agent

```shell
vctl status
```

## Development

Please see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).

Please see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)

## Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
