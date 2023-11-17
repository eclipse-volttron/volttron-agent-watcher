## volttron-agent-watcher

The Agent Watcher is used to monitor agents running on a VOLTTRON instance. Specifically it monitors whether a set of 
VIP identities (peers) are connected to the instance. If any of the peers in the set are not present then an alert will 
be sent.

# Prerequisites

* Python 3.8

## Python

<details>
<summary>To install Python 3.8, we recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.8
pyenv install 3.8.10

# make it available globally
pyenv global system 3.8.10
```
</details>

# Installation
If VOLTTRON is already installed, proceed to step 3.

1. Create and activate a virtual environment.

    ```shell
    python -m venv env
    source env/bin/activate
    ```
2. Install VOLTTRON

    ```shell
    pip install volttron
    ```

3. Start VOLTTRON
    ```shell
    # Start platform with output going to volttron.log
    volttron -vv -l volttron.log &
    ```
3. Create your configuration file. In this example it is named `config`

    The agent has two configuration values:

    * watchlist: a list of VIP identities to watch on the platform instance
    * check-period: interval in seconds between the agent watcher checking the platform peerlist and publishing alerts

    ```
    {
        "watchlist": [
            "platform.driver",
            "platform.actuator"
        ],
        "check-period": 10
    }
    ```
4. Install and start agent watcher in VOLTTRON.

    Installing the agent watcher in VOLTTRON requires you to setup a configuration file. Instructions are shown below in the configuration section. 
    ```shell
    vctl install volttron-agent-watcher --agent-config <path to config> --vip-identity platform.agent_watcher --start --force
    ```



### Example Publish

The following is an example publish from a platform with an instance of the Platform Driver installed but not running.

```
(volttron-agent-watcher-0.1.0 142838) agent_watcher.agent(74) WARNING: Agent(s) expected but but not running ['platform.driver', 'platform.actuator']
(volttron-listener-0.2.0rc0 139056) listener.agent(104) INFO: Peer: pubsub, Sender: platform.agent_watcher:, Bus: , Topic: alerts/AgentWatcher/None_platform_agent_watcher, Headers: {'alert_key': 'AgentWatcher', 'min_compatible_version': '3.0', 'max_compatible_version': ''}, Message: 
('{"status": "BAD", "context": "Agent(s) expected but but not running '
 '[\'platform.driver\', \'platform.actuator\']", "last_updated": '
 '"2023-10-25T18:09:01.663138+00:00"}')
```

# Disclaimer Notice

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
