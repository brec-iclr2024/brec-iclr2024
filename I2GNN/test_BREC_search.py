import os
SEED = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for seed in SEED:
    script_base = f'python test_BREC_no4v_60cfi.py --SEED={seed} --h=8 --node_label=spd --layers=5 --BATCH_SIZE=16 --LEARNING_RATE=1e-5 --WEIGHT_DECAY=1e-4'
    print(script_base)
    os.system(script_base)
