# Inf2Cat

Small python script I wrote to create `*.cat` files (which are PKCS #7 object) so I can install unsigned drivers.


# How to install TRULY unsigned driver

1. Build your driver
2. Execute this inf2cat
3. Move created file to your driver package
4. `8<----Next steps are no longer needed---`
5. Find Windows that can work from Live CD
6. Boot to it
7. Execute `dism /Image:DiskLetterOfDestinationWindows /Add-Driver /Driver:Path\To\Your\Driver\Inf\File /ForceUnsigned`
8. Viola
