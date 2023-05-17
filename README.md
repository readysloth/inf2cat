# Inf2Cat

Small python script I wrote to create `*.cat` files (which are PKCS #7 object) so I can install unsigned drivers.


# How to install TRULY unsigned driver

1. Build your driver
2. Execute this inf2cat
3. Move created file to your driver package
4. Find Windows that can work from Live CD
5. Boot to it
6. Execute `dism /Image:DiskLetterOfDestinationWindows /Add-Driver /Driver:Path\To\Your\Driver\Inf\File /ForceUnsigned`
7. Viola
