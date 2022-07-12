from mmcv import Config, DictAction
from mmaction.apis import inference_recognizer, init_recognizer
import os.path as osp
import os
import time
from glob import glob


if __name__ == '__main__':
    # ----settings-----
    fp_config = 'mmaction2/configs/recognition/arr_tsm2022/tsm_r50_1x1x8_50e_breakfast_rgb.py'
    fp_config_out = 'mmaction2/tmp/config.py'
    cfg = Config.fromfile(fp_config)
    cfg_options = {'work_dir': dir_workdir_next,
                   'data.train.ann_file': train_data_next_mixed,
                   'data.val.ann_file': val_data,
                   'data.test.ann_file': test_data,
                   'data.train.data_prefix': dir_videos_root,
                   'data.val.data_prefix': dir_videos_root,
                   'data.test.data_prefix': dir_videos_root,
                   'load_from': fp_checkpoint_current,
                   'data_root': dir_videos_root,
                   'data_root_val': dir_videos_root,
                   'ann_file_train': train_data_next_mixed,
                   'ann_file_val': val_data,
                   'ann_file_test': test_data, }
    cfg.merge_from_dict(cfg_options)
    cfg.dump(fp_config_next)

    train_command = mmaction_root + "/tools/dist_train_onlyheader.sh " + \
        fp_config_next + " 1 --validate --seed 0 --deterministic --gpu-ids 0"
    import subprocess
    print(train_command)
    #subprocess.run([train_command], shell=True)
#
    #test_command = mmaction_root + "/tools/test_several.py " + fp_config_next + " " + osp.join(
    #    dir_workdir_next,
    #    'epoch_50.pth') + " --eval top_k_accuracy mean_class_accuracy --out " + osp.join(
    #    dir_workdir_next,
    #    'test_result.json')
    #print(test_command)
