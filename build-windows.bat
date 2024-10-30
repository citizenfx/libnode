@echo off
pushd node

for %%f in (../patches/*.patch) do (
    echo Applying %%f...
    git apply --reject --whitespace=fix "../patches/%%f"
)

vcbuild.bat release x64 dll no-cctest clang-cl nonpm
