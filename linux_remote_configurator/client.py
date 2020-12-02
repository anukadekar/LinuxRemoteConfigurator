from os import system
from paramiko import RSAKey, SSHException, SSHClient, AutoAddPolicy, AuthenticationException
import logging

logging.basicConfig(filename="build/logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RemoteClient :
    def __init__(self, host, user, ssh_key_filepath, password) :
        self.host = host
        self.user = user
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.client = None
        self.conn = None
        self._get_ssh_key()
        self._upload_ssh_key()

    def _get_ssh_key(self) :
        self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
        try :
            self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
            logger.info(f'Found ssh key at {self.ssh_key_filepath}')
        except SSHException as error :
            logger.error(error)
            print(self.ssh_key_filepath)
        return self.ssh_key

    def _upload_ssh_key(self) :
        try :
            system(
                f'sshpass -p {self.password} ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1')
            system(
                f'sshpass -p {self.password} ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')
            logger.info(f'{self.ssh_key_filepath} uploaded to {self.host}')
        except FileNotFoundError as error :
            logger.error(error)

    def _connect(self) :
        if self.conn is None :
            try :
                self.client = SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                self.client.connect(self.host, username=self.user, key_filename=self.ssh_key_filepath,
                                    look_for_keys=True, timeout=5000)
            except AuthenticationException as error :
                logger.error(f'Authentication failed')
                raise error
        return self.client

    def disconnect(self) :
        if self.client :
            self.client.close()


