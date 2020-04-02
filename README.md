# jupyter-utils

## `kernel_create.py`

`kernel_create.py` creates a jupyter kernel in `$HOME/.local/share/jupyter/kernels` that uses the python that's active on the environment where it is run. Such kernel will be atomatically avaialable when launching a notebook on [http://jupyter.cscs.ch|http://jupyter.cscs.ch]

For instance, let's say we want to create a virtual environment and make a jupyter kernel that uses it. We first create the virtual environment
```bash
module load cray-python/3.6.5.7
python -m venv myenv
```
In order to use a virtual environment as jupyter kernel, it has to have the ipykernel package installed. For that, we activate the environment and install ipykernel with `pip`.
```bash
source myenv/bin/activate
pip install ipykernel
```
Now, with the virtual environment still activated, we can run the `kernel-create.py` script
```bash
kernel-this -n myenv-kernel
```
Here we named the kernel `myenv-kernel`. The script should print
```bash
Kernel 'myenv-kernel' created successfully in '~/.local/share/jupyter/kernels/myenv-kernel'
```
In case it's not possible to activate an environment. The `kernel_create.py` will create a kernel from a python executable provided through the environment variable `$TARGET_PYTHON_EXE`:
```bash
TARGET_PYTHON_EXE=/path/to/my/bin/python kernel-this -n mykernel
```
