import json
import os
import urllib.parse
import urllib.request
from configparser import ConfigParser


class TeamCity:
    def __init__(self):
        self.tc_host = None
        self.tc_user = None
        self.tc_pass = None
        self._prepare()

    def _prepare(self):
        self._read_options()
        if not all((self.tc_host, self.tc_user, self.tc_pass)):
            raise Warning('Specify host, user and password via env or config.conf file')

        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.tc_host, self.tc_user, self.tc_pass)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

    def _read_options(self):
        config = ConfigParser(allow_no_value=True)
        config.optionxform = str
        params_map = {
            'TEAMCITY_HOST': 'tc_host',
            'TEAMCITY_USER': 'tc_user',
            'TEAMCITY_PASS': 'tc_pass',
        }
        if os.path.exists('config.conf'):
            config.read('config.conf')
            if 'default' in config.sections():
                options = config['default']
                for k, attr in params_map.items():
                    setattr(self, attr, options.get(k))

        for attr, env_key in ((v, k) for k, v in params_map.items()):
            if getattr(self, attr, None) is None:
                setattr(self, attr, os.environ.get(env_key))

    def get_services(self):
        url = urllib.parse.urljoin(self.tc_host, '/app/rest/buildTypes')
        headers = {'Accept': 'application/json'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            if resp.code != 200:
                return False, None
            res = json.loads(resp.read().decode())
            return True, [(o['id'], o['name']) for o in res['buildType']]

    def get_branches(self, service):
        url = urllib.parse.urljoin(self.tc_host,
                                   '/app/rest/buildTypes/id:{0}/branches'.format(service))
        headers = {'Accept': 'application/json'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            if resp.code != 200:
                return False, None
            res = json.loads(resp.read().decode())
            return True, [o['name'] for o in res['branch']]

    def run_build(self, service, branch):
        url = urllib.parse.urljoin(self.tc_host, '/app/rest/buildQueue')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/xml',
        }
        data = ('<build personal="true" branchName="{}"><buildType id="{}"/></build>'
                .format(branch, service)).encode()
        req = urllib.request.Request(url, data, headers, method='POST')
        with urllib.request.urlopen(req) as resp:
            return resp.code == 200
