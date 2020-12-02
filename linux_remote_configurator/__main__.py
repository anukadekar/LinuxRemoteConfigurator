import client
import os
import json
import app

with open('../resources/config.json', 'r') as f :
    data = json.load(f)

remote_user = data["REMOTE_USER"]
host = input("Enter the remote host IP address: ")
password = input("Enter the remote host password: ")
ssh_key_filepath = f"/home/{os.environ['USER']}/.ssh/id_rsa"
commands = data["COMMAND_SET"]


def _execute_command_on_remote(exec_command) :
    exec_command.execute_command()


def main() :
    remote = client.RemoteClient(host, remote_user, ssh_key_filepath, password)
    exec_command = app.LinuxRemoteConfigurator(host, remote_user, ssh_key_filepath, password, commands)
    _execute_command_on_remote(exec_command)
    remote.disconnect()


if __name__ == '__main__' :
    main()
