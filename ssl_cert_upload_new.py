import os
import logging
from abc import ABC, abstractmethod
from getpass import getpass
from cterasdk import Edge, CTERAException, settings
from cterasdk.exceptions import ConsentException

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
        if self.host:
            self.host.logout()

class FilerConfigurator(AbstractConfigurator):
    def __init__(self, host, username, password, hostname, private_key, certificates, force=False):
        super().__init__()
        self.host_address = host
        self.username = username
        self.password = password
        self.hostname = hostname
        self.private_key = private_key
        self.certificates = certificates  # List of certificate contents
        self.force = force

    def before(self):
        # Initialize Edge connection
        self.host = Edge(self.host_address)
        self.host.test()
        # Check if previously configured
        if self.host.initialized:
            if self.force:
                logging.getLogger().debug('Proceeding with filer configuration without confirmation')
                return
            else:
                if ask('This filer was previously configured. Continue? [This script will override existing configuration]'):
                    try:
                        if confirm('To confirm, type in the local admin account password', self.password, secure=True):
                            logging.getLogger().debug('Proceeding with filer configuration')
                            return
                    except KeyboardInterrupt:
                        logging.getLogger().debug('Interrupt. Exiting.')
                        raise
                else:
                    raise CTERAException('Cancelled by user.')
        else:
            logging.getLogger().debug('Configuring a new filer')
            return

    def execute(self):
        self._add_first_user()
        self._update_certificate()
        self._export_settings()

    def _add_first_user(self):
        if self.host.initialized:
            logging.getLogger().debug('Logging in %s', {'username': self.username})
            self.host.login(self.username, self.password)
        else:
            logging.getLogger().debug('Creating first user %s', {'username': self.username})
            self.host.users.add_first_user(self.username, self.password)

    def _update_certificate(self):
        logging.getLogger().debug('Updating certificate')
        self.host.ssl.import_certificate(self.private_key, *self.certificates)

    def _export_settings(self):
        self.host.config.export(os.path.expanduser('~/Downloads/%s.xml' % self.hostname))

def cert_upload(host, username, password, hostname, private_key_path, certificate_paths, force=False):

    # Configure logging level if needed
    logging.basicConfig(level=logging.INFO)
    settings.sessions.management.ssl = False  # Ignore certificate errors connecting to CTERA Edge Filer

    try:
        # Read the private key and certificates from provided file paths
        with open(private_key_path, 'r') as pk_file:
            private_key = pk_file.read()
        certificates = []
        for cert_path in certificate_paths:
            with open(cert_path, 'r') as cert_file:
                certificates.append(cert_file.read())

        logging.getLogger().debug('Running Configurator.')
        configurator = FilerConfigurator(
            host=host,
            username=username,
            password=password,
            hostname=hostname,
            private_key=private_key,
            certificates=certificates,
            force=force
        )
        configurator.run()
        logging.getLogger().debug('Completed.')
    except FileNotFoundError as e:
        logging.getLogger().fatal(f"File not found: {e}")
    except CTERAException as error:
        logging.getLogger().fatal(str(error))
    except Exception as e:
        logging.getLogger().fatal(f"An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        logging.getLogger().fatal('Cancelled by user.')
