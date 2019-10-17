bsub -n 4 -W 40:00 -o log_test8 -R "rusage[mem=2048, ngpus_excl_p=1]" -R "select[gpu_mtotal0>=10240]" python ~/mp_project/RosenDeepGarten/train.py

