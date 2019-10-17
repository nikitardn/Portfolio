bsub -n 4 -W 0:50 -o log_test -R "rusage[mem=2048, ngpus_excl_p=1]" python ~/mp_project/RosenDeepGarten/test.py
watch -n 1 bjobs

