# Pseudo-Random Number Generation and Analysis
ISML Generator and testing using Diehard - MS, MUIA

## Project Objective

The objective of this project is to generate a sample of pseudo-random numbers using the **IMSL Multiplicative Congruential Generator**, with multiplier $a=16807$ and modulus $m=2^{31}-1$.

The generator is defined by the following recurrence relation:

$$
X_{n+1}=(16807\cdot X_n)\bmod(2^{31}-1)
$$

The resulting states are normalized to produce values in the interval $(0,1)$:

$$
U_n=\frac{X_n}{2^{31}-1}
$$

The generated sample is subsequently evaluated using **[Dieharder](https://webhome.phy.duke.edu/~rgb/General/dieharder.php)**, a statistical testing suite designed to assess the quality of random number generators.

## Environment Setup

To reproduce this project, a Linux environment is required, as Dieharder is used as a command-line tool.

### 1. Windows: Installing WSL

On Windows, the Windows Subsystem for Linux (WSL) can be used to provide a Linux environment. Open PowerShell as Administrator and execute:

```powershell
wsl --install -d Ubuntu
```

Once the installation is complete, restart the computer if necessary and launch Ubuntu from the Windows Start menu.

### 2. Ubuntu: Installing Dependencies

Update the package lists and install Python, virtual environment tools, Git, and Dieharder:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git dieharder
```

### 3. Clone the Repository and Create a Virtual Environment

Clone the repository and navigate to its directory:

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_DIRECTORY>
```

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies required to run the notebook:

```bash
python -m pip install --upgrade pip
python -m pip install jupyter numpy
```

### 4. Launch Jupyter Notebook

From the project directory, with the virtual environment activated, execute:

```bash
jupyter notebook
```

Jupyter Notebook will open in the web browser. Select the project notebook from the interface to run the different stages of pseudo-random number generation and statistical analysis.