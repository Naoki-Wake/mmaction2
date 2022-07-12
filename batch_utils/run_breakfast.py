from mmcv import Config, DictAction
from numpy import argsort
from mmaction.apis import inference_recognizer, init_recognizer
import os.path as osp
import os
import time
from glob import glob
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run breakfast')
    parser.add_argument('--dir-root', default='/tmp/repo', type=str)
    parser.add_argument('--config', default='configs/recognition/arr_tsm2022/tsm_r50_1x1x8_50e_breakfast_rgb.py', type=str)
    parser.add_argument('--load-from', default='/lfovision_sthv2_breakfast/pretrained_models/tsm_r50_256h_1x1x8_50e_sthv2_rgb_20210816-032aa4da.pth', type=str)
    parser.add_argument('--work-dir-root', default='/lfovision_log/tsm_learningrate/', type=str)
    parser.add_argument('--work-dir-name', default='', type=str)
    parser.add_argument('--train-file-dir', default='/lfovision_sthv2_breakfast/annotations/with_pseudo_largedatanum/', type=str)
    parser.add_argument('--dir-videos-root', default='/lfovision_sthv2_breakfast/', type=str)
    parser.add_argument('--videos-per-gpu', default=30, type=int)
    parser.add_argument('--workers-per-gpu', default=4, type=int)
    parser.add_argument('--lr', default=0.0075, type=float)
    parser.add_argument('--weight_decay', default=0.0005, type=float)
    parser.add_argument('--momentum', default=0.9, type=float)

    args = parser.parse_args()
    # ----settings-----
    fp_config_out = '/tmp/config.py'
    if args.work_dir_name == '':
        work_dir_name = "lr_{}_wd_{}_momentum_{}".format(args.lr, args.weight_decay, args.momentum)
    cfg = Config.fromfile(osp.join(args.dir_root,args.config))
    cfg_options = {'work_dir': osp.join(args.work_dir_root,work_dir_name),
                   'data.train.ann_file': osp.join(args.train_file_dir, 'breakfast_train_list_videos.txt'),
                   'data.val.ann_file': osp.join(args.train_file_dir, 'breakfast_val_list_videos.txt'),
                   'data.test.ann_file': osp.join(args.train_file_dir, 'breakfast_test_list_videos.txt'),
                   'data.train.data_prefix': args.dir_videos_root,
                   'data.val.data_prefix': args.dir_videos_root,
                   'data.test.data_prefix': args.dir_videos_root,
                   'load_from': args.load_from,
                   'data_root': args.dir_videos_root,
                   'data_root_val': args.dir_videos_root,
                   'ann_file_train': osp.join(args.train_file_dir, 'breakfast_train_list_videos.txt'),
                   'ann_file_val': osp.join(args.train_file_dir, 'breakfast_val_list_videos.txt'),
                   'ann_file_test': osp.join(args.train_file_dir, 'breakfast_test_list_videos.txt'), 
                   'data.videos_per_gpu': args.videos_per_gpu,
                   'data.workers_per_gpu': args.workers_per_gpu,
                   'optimizer.lr': args.lr,
                   'optimizer.weight_decay': args.weight_decay,
                   'optimizer.momentum': args.momentum,}
    cfg.merge_from_dict(cfg_options)
    cfg.dump(fp_config_out)

    train_command = str(osp.join(args.dir_root, "tools/dist_train_onlyheader.sh")) + \
        " " + fp_config_out + " 1 --validate --seed 0 --deterministic --gpu-ids 0"
    import subprocess
    print(train_command)
    #subprocess.run([train_command], shell=True)
#
    test_command = "python " + str(osp.join(args.dir_root, "tools/test_several.py")) + " " + fp_config_out + " " + osp.join(
        osp.join(args.work_dir_root,args.work_dir_name),
        'epoch_0.pth') + " --eval top_k_accuracy mean_class_accuracy --out " + osp.join(
        osp.join(args.work_dir_root,args.work_dir_name),
        'test_result.json')
    print(test_command)
