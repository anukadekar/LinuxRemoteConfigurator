import json
from client import RemoteClient
import logging

logging.basicConfig(filename="build/logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

with open('../resources/config.json', 'r') as f :
    data = json.load(f)


class LinuxRemoteConfigurator :
    def __init__(self, host, user, ssh_key_filepath, password, commands) :
        self.host = host
        self.user = user
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.commands = commands
        self.conn = None

    def cat_file(self) :
        self.conn = RemoteClient._connect(self)
        file_name = data["REMOTE_FILE_NAME"]
        cmd = 'cat ' + file_name
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        if stdout.channel.recv_exit_status() == 0 :
            response = stdout.readlines()
            for line in response :
                logger.info(f'{line}')
        else :
            logger.error("File does not exist")

    def create_directory(self) :
        self.conn = RemoteClient._connect(self)
        directory_name = data["REMOTE_DIR_NAME"]
        cmd = 'mkdir ' + directory_name
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        if stdout.channel.recv_exit_status() == 0 :
            logger.info("Directory created")
        else :
            logger.error("Directory already exists")

    def list_files(self) :
        self.conn = RemoteClient._connect(self)
        directory_name = data["LIST_FILES_DIRECTORY_NAME"]
        cmd = "ls -lrth " + directory_name
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        response = stdout.readlines()
        for line in response :
            logger.info(f'{line}')

    def execute_command(self) :
        self.conn = RemoteClient._connect(self)
        for cmd in self.commands :
            if cmd == "display_file" :
                self.cat_file()
            elif cmd == "create_directory" :
                self.create_directory()
            elif cmd == "list_files" :
                self.list_files()
