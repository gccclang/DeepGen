Welcome to the homepage of DeepGen! DeepGen is a deep-learning based tool to generate programs for compiler testing.

## Requirements
We recommend using CONDA and GPU to configure your environment
* python 3.6
* tf-gpu >=1.12.0

## Usage
* pre-process seed programs
  python cleandata.py
* train data
  bash scripts/seed_base_gpu.sh train_data
* train Transformer-xl
  bash scripts/seed_base_gpu.sh train
* infer programs
  bash scripts/seed_base_gpu.sh inference
* test compilers
  python testcompilers.py

## Detail Information of Folders
* './seed' is the seed corpus that includes 3934 seed programs for pro-processing
* './inferseed' is the inference corpus that is generated after pro-processing
* './generated-file' obtains the newly generated test programs
* './detectbug' includes nine sub-folders:
  * './detectbug/clang', './detectbug/clango0', './detectbug/gcc', and './detectbug/gcco0' obtain the compiled information of each test programs
  * './detectbug/crash' obtains the test programs that trigger crashing compiler bugs
  * './detectbug/invalid' obtains the invalid test programs
  * './detectbug/reject' obtains the test programs that trigger reject-valid compiler bugs
  * './detectbug/timeout' obtains the test programs that trigger time-out compiler bugs
  * './detectbug/wrongcode' obtains the test programs that trigger wrong-code compiler bugs
