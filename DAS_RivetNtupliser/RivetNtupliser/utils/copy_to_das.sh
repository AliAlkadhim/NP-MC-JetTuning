#!/bin/bash
copy_to_das() {
local_path="/home/ali/Desktop/Pulled_Github_Repositories/NP-MC-JetTuning/DAS_RivetNtupliser/src/RivetNtupliser_CMS_2021_I1972986.cc"
das_path="/afs/desy.de/user/a/aalkadhi/DAS/Darwin/CMSSW_12_4_0/src/Core/Ntupliser/src"
scp $local_path aalkadhi@naf-cms.desy.de:$das_path
}

copy_from_das() {
local_path="/home/ali/Desktop/Pulled_Github_Repositories/NP-MC-JetTuning/DAS_RivetNtupliser/src/RivetNtupliser_CMS_2021_I1972986.cc"
das_path="/afs/desy.de/user/a/aalkadhi/DAS/Darwin/CMSSW_12_4_0/src/Core/Ntupliser/src"
scp aalkadhi@naf-cms.desy.de:$das_path $local_path
}

