# volttron-agent-watcher

The VOLTTRON Agent Watcher is used to monitor agents running on a VOLTTRON instance. Specifically it monitors whether a set of
VIP identities (peers) are connected to the instance. If any of the peers in the set are not present then an alert will
be sent.

## Requires

* python >= 3.10
* volttron >= 10.0
* volttron-lib-base-driver

## Installation

Before installing, VOLTTRON should be installed and running.  Its virtual environment should be active.
Information on how to install of the VOLTTRON platform can be found
[here](https://github.com/eclipse-volttron/volttron-core).

Create a directory called `config` and use the change directory command to enter it.

```shell
mkdir config
cd config
```

After entering the config directory, create a file called `agentwatcher.config`, use the below JSON to populate your new file.

The agent has two configuration values:

* watchlist: a list of VIP identities to watch on the platform instance
* check-period: interval in seconds between the agent watcher checking the platform peerlist and publishing alerts

In your config add the following JSON. Adjust to fit your needs.

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
vctl install volttron-agent-watcher --agent-config agentwatcher.config --vip-identity platform.agent_watcher --start --force
```

## Example Publish

Observe Data

To see data being published to the bus, install a [Listener Agent](https://pypi.org/project/volttron-listener/):

```bash
vctl install volttron-listener --start
```

Once installed, you should see the data being published by viewing the Volttron logs file that was created in step 2.
To watch the logs, open a separate terminal and run the following command:

```bash
tail -f <path to folder containing volttron.log>/volttron.log
```

The following is an example publish from a platform with an instance of the Platform Driver installed but not running.

```bash
(volttron-agent-watcher-0.1.0 142838) agent_watcher.agent(74) WARNING: Agent(s) expected but not running ['platform.driver', 'platform.actuator']
(volttron-listener-0.2.0rc0 139056) listener.agent(104) INFO: Peer: pubsub, Sender: platform.agent_watcher:, Bus: , Topic: alerts/AgentWatcher/None_platform_agent_watcher, Headers: {'alert_key': 'AgentWatcher', 'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message:
('{"status": "BAD", "context": "Agent(s) expected but but not running '
'[\'platform.driver\', \'platform.actuator\']", "last_updated": '
'"2023-10-25T18:09:01.663138+00:00"}')
```

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
