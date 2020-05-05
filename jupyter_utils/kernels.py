import os
import sys
import pathlib
import stat
import argparse
from inspect import cleandoc


class PythonEnv():
    def __init__(self):
        self.shortver = '%s.%s' % (sys.version_info.major,
                                   sys.version_info.minor)
        self.bin_dir = os.path.join(sys.prefix, 'bin')
        self.lib_dir = os.path.join(sys.prefix, 'lib',
                                    'python%s' % self.shortver,
                                    'site-packages')

    def has_activate(self):
        activate_script = os.path.join(self.bin_dir, 'activate')
        return True if os.path.exists(activate_script) else False

    def uses_system_site_packages(self):
        venv_cfg = os.path.join(sys.prefix, 'pyvenv.cfg')
        try:
            with open(venv_cfg) as f:
                for l in f.readlines():
                    k, v = l.split('=')
                    if k.strip() == 'include-system-site-packages':
                        if v.strip().lower() == 'true':
                            system_site_packages = True
                        if v.strip().lower() == 'false':
                            system_site_packages = False

        except FileNotFoundError:
            return False

        return system_site_packages

    @property
    def dist(self):
        dists = ['anaconda',
                 'cray']
        for d in dists:
            if d in sys.version.lower():
                return d

        return 'unknown'


class PythonJupyterKernel():
    def __init__(self, name):
        if not self.has_ipykernel():
            exit('ERROR: `ipykernel` is not installed on this python env.\n'
                 'Please, install it so this python env can be used as a '
                 'jupyter kernel.')

        self.env = PythonEnv()
        self.name = name

    @property
    def kernel_str(self):
        _kernel = '''
        {{
         "display_name": "{kernel_name}",
         "language": "python",
         "argv": [
         "{kernel_dir}/launcher",
         "-f",
         "{{connection_file}}"
         ]
        }}
        '''
        return cleandoc(_kernel.format(**self.format_dict))

    @property
    def launcher_str(self):
        _launcher = '''
        #!/usr/bin/env bash
        {kernel_env}
        {activate}
        {python_exe} -m ipykernel_launcher $@
        '''
        return cleandoc(_launcher.format(**self.format_dict))

    def make_kernel_dir(self, overwrite):
        if overwrite:
            pathlib.Path(self.dir).mkdir(parents=True, exist_ok=True)
        else:
            try:
                pathlib.Path(self.dir).mkdir(parents=True)
            except FileExistsError:
                exit("ERROR: folder '%s' already exists"
                     % self.dir)

    @property
    def format_dict(self):
        _format_dict = {
            'kernel_name': self.name,
            'kernel_dir': self.dir,
            'activate': ('source %s' % self.activate_script
                         if self.activate_script else ''),
            'kernel_env': self.kernel_env,
            'python_exe': sys.executable,
        }

        return _format_dict

    @property
    def dir(self):
        return os.path.join(pathlib.Path.home(),
                            '.local/share/jupyter/kernels/'
                            '%s' % self.name)

    @property
    def activate_script(self):
        if self.env.has_activate():
            return os.path.join(self.env.bin_dir, 'activate')
        else:
            return None

    @property
    def kernel_env(self):
        if self.env.uses_system_site_packages():
            kernel_env = 'source $HOME/.jupyterhub.env'
        else:
            kernel_env = "export PYTHONPATH=''"

        return kernel_env

    def has_ipykernel(self):
        try:
            import ipykernel
            return True
        except ModuleNotFoundError:
            return False

    def write(self, overwrite=False):
        self.make_kernel_dir(overwrite)
        filenames = ['kernel.json', 'launcher']
        file_strings = [self.kernel_str, self.launcher_str]
        for n, s in zip(filenames, file_strings):
            abs_path = os.path.join(self.dir, n)
            with open(abs_path, 'w') as f:
                print(s, file=f)

            # make the launcher file executable
            if 'launcher' in n:
                st = os.stat(abs_path)
                os.chmod(abs_path, st.st_mode | stat.S_IEXEC)

        print("Kernel '{kernel_name}' created successfully in "
              "'{kernel_dir}'".format(**self.format_dict))


def main():
    parser = argparse.ArgumentParser(
        description='Creates jupyter kernel for the '
                    'current python executable.')
    parser.add_argument('-n', dest='kernel_name',
                        help='set name of the kernel',
                        required=True)
    parser.add_argument('-f', dest='overwrite',
                        help='overwrite if kernel folder exists',
                        action='store_true')
    args = parser.parse_args()

    kernel = PythonJupyterKernel(args.kernel_name)
    kernel.write(args.overwrite)
