import os
import sys
import logging
import configparser
from abc import ABC, abstractmethod
from getpass import getpass
from cterasdk import config, Gateway, CTERAException
from cterasdk.exception import ConsentException
from cterasdk.lib.filesystem import FileSystem

def find_file(path):
    logging.getLogger().debug('Looking for file. %s', {'path': path})
    info = FileSystem.get_local_file_info(path)
    logging.getLogger().debug('Found file. %s', {'name': info['name'], 'size': info['size']})
    return info

def ask(question):
    answer = None
    answers = ['Y', 'n', 'Q']
    question = question + ' (' + '/'.join(answers) + '): '
    try:
        while answer not in answers:
            try:
                answer = input(question)
            except EOFError:
                raise ConsentException()
    except KeyboardInterrupt:
        answer = 'Q'
    if answer == 'Y':
        return True
    if answer == 'Q':
        raise ConsentException()
    return False

def confirm(question, answer, secure=False):
    user_answer = None
    answers = [answer]
    question = question + ('' if secure else ' (' + '/'.join(answers) + ')') + ': '
    while user_answer not in answers:
        try:
            if secure:
                user_answer = getpass(question)
            else:
                user_answer = input(question)
        except EOFError:
            raise ConsentException()
    if user_answer == answer:
        return True

class AbstractConfigurator(ABC):
    def __init__(self):
        self.host_config = HostConfig.instance()
        self.host = None

    def run(self):
        logging.getLogger().debug('Run before execution')
        self.before()
        logging.getLogger().debug('Execute')
        self.execute()
        logging.getLogger().debug('Run after execution')
        self.after()

    def before(self):
        pass

    @abstractmethod
    def execute(self):
        raise NotImplementedError("Implementing class must implement this method")

    def after(self):
        pass

class HostConfig:
    __instance = None

    @staticmethod
    def instance():
        return HostConfig.__instance

    @staticmethod
    def from_file(path):
        find_file(path)
        if HostConfig.__instance is None:
            HostConfig(path)
        return HostConfig.__instance

    def __init__(self, path):
        if HostConfig.__instance is not None:
            raise Exception("Cannot instantiate twice.")
        logging.getLogger().debug('Parsing config file. %s', {'path': path})
        self.config_parser = configparser.ConfigParser(interpolation=None)
        self.config_parser.optionxform = str  # case sensitive
        self.config_parser.read(path)
        logging.getLogger().debug('Parsed config file. %s', {'path': path})
        HostConfig.__instance = self

    def get(self, section, option, as_type=None):
        if self.config_parser.has_section(section):
            if self.config_parser.has_option(section, option):
                if as_type is bool:
                    return self.config_parser.getboolean(section, option)
                if as_type is int:
                    return self.config_parser.getint(section, option)
                return self.config_parser.get(section, option)
            else:
                logging.getLogger().error('Could not find option in section. %s',
                                          {'section': section, 'option': option})
        else:
            logging.getLogger().error('Could not find section. %s', {'section': section})
        return None

    def options(self, section):
        if self.config_parser.has_section(section):
            for option in self.config_parser.options(section):
                yield option
        else:
            logging.getLogger().error('Could not find section. %s', {'section': section})
        return None

class FilerConfigSection:
    General = 'Edge Filer'
    Certificate = 'Certificate'

class FilerConfigGeneral:
    Host = 'Host'
    Username = 'Username'
    Password = 'Password'
    Hostname = 'Hostname'

class FilerConfigCertificate:
    PK = 'Private Key'
    Certificate = 'Certificate'

class FilerConfigurator(AbstractConfigurator):
    def __init__(self):
        super().__init__()

    def before(self):
        # init
        self.host = Gateway(self.host_config.get(FilerConfigSection.General, FilerConfigGeneral.Host), https=True)
        self.host.test()
        # check if previously configured
        password = self.host_config.get(FilerConfigSection.General, FilerConfigGeneral.Password)
        if self.host.initialized:
            if ask('This filer was previously configured. Continue? [This script will override existing configuration]'):
                try:
                    if confirm('To confirm, type in the local admin account password', password, secure=True):
                        logging.getLogger().debug('Proceeding with filer configuration')
                        return
                except KeyboardInterrupt:
                    logging.getLogger().debug('Interrupt. Exiting.')
                    raise
        else:
            logging.getLogger().debug('Configuring a new filer')
            return
        raise CTERAException('Cancelled by user.')

    def execute(self):
        self._add_first_user()
        self._update_certificate()
        self._export_settings()

    def _add_first_user(self):
        username = self.host_config.get(FilerConfigSection.General, FilerConfigGeneral.Username)
        password = self.host_config.get(FilerConfigSection.General, FilerConfigGeneral.Password)
        if self.host.initialized:
            logging.getLogger().debug('Logging in %s', {'username': username})
            self.host.login(username, password)
        else:
            logging.getLogger().debug('Creating first user %s', {'username': username})
            self.host.users.add_first_user(username, password)

    def _update_certificate(self):
        secrets = [(secret, self.host_config.get(FilerConfigSection.Certificate, secret)) for secret in
                   self.host_config.options(FilerConfigSection.Certificate)]
        if len(secrets) < 3:
            logging.error('Invalid certificate chain')
            return
        pk_key, pk_value = secrets.pop(0)
        if pk_key != FilerConfigCertificate.PK:
            logging.error('Incorrect certificate definition. %s',
                          {'expected_key': FilerConfigCertificate.PK, 'actual_key': pk_key})
            return
        certificates = [v for k, v in secrets]
        logging.getLogger().debug('Updating certificate')
        self.host.ssl.import_certificate(pk_value, *certificates)

    def _export_settings(self):
        hostname = self.host_config.get(FilerConfigSection.General, FilerConfigGeneral.Hostname)
        self.host.config.export(os.path.expanduser('~/Downloads/%s.xml' % hostname))

def usage():
    print()
    print('Usage: ' + sys.argv[0] + ' ' + '<config>')

if __name__ == '__main__':
    config.http['ssl'] = 'Trust'  # ignore certificate errors connecting to CTERA Edge Filer
    args = sys.argv
    if len(args) < 2:
        logging.getLogger().error('You did not specify a config file. Exiting.')
        usage()
        quit()
    if len(args) > 2:
        logging.getLogger().error('Too many arguments.')
        usage()
        quit()
    try:
        HostConfig.from_file(args[1])
        logging.getLogger().debug('Running Configurator.')
        FilerConfigurator().run()
        logging.getLogger().debug('Completed.')
    except CTERAException as error:
        logging.getLogger().fatal(str(error))
    except KeyboardInterrupt:
        logging.getLogger().fatal('Cancelled by user.')
