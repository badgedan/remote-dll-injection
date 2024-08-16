from ctypes import *
from ctypes import wintypes

kernel32=windll.kernel32
LPCTSTR=c_char_p
SIZE_T=c_size_t

OpenProcess = kernel32.OpenProcess # Returns the handle of a specified process
OpenProcess.argtypes=(wintypes.DWORD,wintypes.BOOL,wintypes.DWORD)
OpenProcess.restype=wintypes.HANDLE

VirtualAllocEx=kernel32.VirtualAllocEx # Locates an area in the memory
VirtualAllocEx.argtypes=(wintypes.HANDLE,wintypes.LPVOID,SIZE_T,wintypes.DWORD,wintypes.DWORD)
VirtualAllocEx.restype=wintypes.LPVOID

WriteProcessMemory=kernel32.WriteProcessMemory # Writes data to an area of memory in the specified process
WriteProcessMemory.argtypes=(wintypes.HANDLE,wintypes.LPVOID,wintypes.LPCVOID,SIZE_T,POINTER(SIZE_T))
WriteProcessMemory.restype=wintypes.BOOL

class _SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', wintypes.DWORD),  # Use DWORD for nLength
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle', wintypes.BOOL)]

SECURITY_ATTRIBUTES=_SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES=POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE=wintypes.LPVOID

CreateRemoteThread=kernel32.CreateRemoteThread # Creates a thread in the virtual memory of a process
CreateRemoteThread.argtypes=(wintypes.HANDLE,LPSECURITY_ATTRIBUTES,SIZE_T,wintypes.LPVOID,wintypes.LPVOID,wintypes.DWORD,wintypes.LPVOID)
CreateRemoteThread.restype=wintypes.HANDLE

GetModuleHandleA=kernel32.GetModuleHandleA # Retrieves a module handle for a specified module
GetModuleHandleA.argtypes=(wintypes.LPCSTR, )
GetModuleHandleA.restype=wintypes.HANDLE

GetProcAddress=kernel32.GetProcAddress
GetProcAddress.argtypes=(wintypes.HMODULE,wintypes.LPCSTR)


PAGE_READWRITE=0x04
MEM_COMMIT=0x00001000
MEM_RESERVE=0x00002000
EXECUTE_IMMEDIATELY=0x0
PROCESS_ALL_ACCESS=(0x000F000 | 0x00100000 | 0x00000FFF)

dll=b'' # Specify the destination of the dll
pid=1111 # Specify the process ID

process_handle=OpenProcess(PROCESS_ALL_ACCESS,False,pid)

if not process_handle: 
    raise WinError()

print(f"Handle -> {process_handle}")


memory_address=VirtualAllocEx(process_handle,None,len(dll)+1,MEM_COMMIT|MEM_RESERVE,PAGE_READWRITE)

print (f"Memory address -> {hex(memory_address)}")


if not WriteProcessMemory(process_handle,memory_address,dll,len(dll)+1,None):
    raise WinError()

load_lib=GetProcAddress(GetModuleHandleA(b'kernel32.dll'),b'LoadLibraryA')

if not load_lib:
    raise WinError()

rthread=CreateRemoteThread(process_handle,None,0,load_lib,memory_address,EXECUTE_IMMEDIATELY,None)


if not rthread:
    raise WinError()
    