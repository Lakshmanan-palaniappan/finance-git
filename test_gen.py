from generators.common.storage import ADLSStorage

storage = ADLSStorage()

print("\nFolders in ADLS:\n")

for item in storage.list_files():

    print(item)