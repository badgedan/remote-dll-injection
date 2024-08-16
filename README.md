# Remote DLL Injector

This project includes a Python script for injecting a DLL into a remote process and a DLL that displays a message box when injected.

## Components

### Python Script

The Python script uses the `ctypes` library to interact with Windows API functions for DLL injection. The script performs the following steps:

1. **Open a Process**: Opens the target process with full access rights.
2. **Allocate Memory**: Allocates memory in the target process's address space for the DLL.
3. **Write DLL**: Writes the DLL into the allocated memory.
4. **Get LoadLibraryA Address**: Retrieves the address of `LoadLibraryA` from the kernel32 module.
5. **Create Remote Thread**: Creates a remote thread in the target process to execute `LoadLibraryA` with the address of the injected DLL.

### DLL File

When injected into a process, the DLL is a simple example that displays a message box saying "Hello world!".

## Prerequisites

- Python 3.x
- `ctypes` library (included with Python)
- Windows operating system

## Usage

1. **Set the `dll` and `pid` Variables**:
   - `dll`: Set this to the byte content of your DLL file.
   - `pid`: Set this to the Process ID (PID) of the target process where you want to inject the DLL.

2. **Run the Python Script**:
   ```bash
   python injector.py

3. **DLL Execution:**
   - Upon successful injection, the DLL will be loaded into the target process, and you should see a message box displaying "Hello world!"..
