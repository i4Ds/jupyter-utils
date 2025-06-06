# jupyter-utils

## `kernel-create`

`kernel_create.py` creates a jupyter kernel in `$HOME/.local/share/jupyter/kernels` from the python environment that's active on the environment. The newly-created kernel will be automatically available on the notebooks launched on the FHNW Cluster ([cs.technik.fhnw.ch/jupyhub](cs.technik.fhnw.ch/jupyhub)).

For instance, let's say we want to create a virtual environment and make a jupyter kernel based on it. We first create the virtual environment
```bash
python -m venv myenv
```
For a virtual environment to be used as jupyter kernel, it has to have the `ipykernel` package installed. It can be installed with `pip`, only first the environment has to be activated
```bash
source myenv/bin/activate
pip install ipykernel
```
Now everything is ready to create a jupyter kernel from `myenv`.
With the environment still activated, we run the `kernel-create` command and specify the name we want to give to the environment
```bash
kernel-create -n myenv-kernel
```
Here we named the kernel `myenv-kernel`. The script should print
```
Kernel 'myenv-kernel' created successfully in '~/.local/share/jupyter/kernels/myenv-kernel'
```
Giving a look to the directory `~/.local/share/jupyter/kernels/myenv-kernel`, we can see that two files have been created: `kernel.json` and `launcher`.

In case it's not possible to activate the virtual environment, the variable `$TARGET_PYTHON_EXE` can be used to specify the python executable to be used by the kernel:
```bash
TARGET_PYTHON_EXE=/path/to/my/bin/python kernel-create -n mykernel
```
