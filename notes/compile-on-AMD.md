# Compile on AMD GPU

the branch with changes for Crusher is: https://bitbucket.org/eschnett/cactusamrex/pull-requests/27 which should compile. Instructions to compile are:

This is for a setup using ExternalLibraries in rhaas80's github repo which self-compile.

```
./GetComponents https://gist.githubusercontent.com/rhaas80/a7c3e58bf23e6f25c605938046829a57/raw/f9cfe1f799a87d9d20f39d0a489b55bf5a33d3cd/crusher.th
cd Cactus
```

This may require manually copying in the (private) GRHydroX repo.

Then switch to rhaas/crusher branch of simfactory:

```
cd simfactory
git checkout rhaas/crusher
cd ..
cd repos/cactusamrex
git checkout rhaas/crusher
cd -
```

set up simfactory as usual

```
./simfactory/bin/sim setup-silent
```

and create a configuration with an invalid thornlist to stop simfactory's build process

```
./simfactory/bin/sim build --thornlist /dev/null
```

You will see some warnings b/c Cactus does not know about clang and flang (yet, I have a patch for this).

Get a shell with all modules that simfactory would load:

```
./simfactory/bin/sim execute 'bash -i'
```

Copy in actual thornlist

```
cp thornlists/crusher.th configs/sim/ThornList
```

Build all ExternalLibraries

```
for i in repos/ExternalLibraries-* ; do make -j4 sim-build BUILDLIST=${i##*-} ; done
```

Edit configs/sim/OptionList and uncomment the -x hip and --hip-link flags in CXXFLAGS and LDFLAGS.
Configure with new options and build remainder of code:

```
# edit OptionList
make sim-config options=configs/sim/OptionList
make -j4 sim
```

This will fail at link stage and we need to overwrite CFLAGS to compile datestamp.c as a HIP C++ file to make the linker happy:

```
make -j4 sim CFLAGS="-pipe -g3 -std=c++17 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX90A__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx90a -fgpu-rdc -x hip" CXXFLAGS="-pipe -g3 -std=c++17 -D__HIP_ROCclr__ -D__HIP_ARCH_GFX90A__=1 --rocm-path=${ROCM_PATH} --offload-arch=gfx90a -fgpu-rdc"
```

Exit the simfactory shell:

```
exit
```

This should give a Cactus executable with GPU support in AMReX for HIP. You can verify looking at AMReX_Config.h in configs/sim/scratch/external/AMReX/include.
