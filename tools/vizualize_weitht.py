import numpy as np
import torch
from mmcv import Config
from mmaction.apis import inference_recognizer, init_recognizer
import os.path as osp


#----settings-----
checkpoint = '/lfovision_log/tsm_learningrate/lr_0.01_wd_0.0005_momentum_0.9_bn_true_cosine/epoch_50.pth'
fp_config = '/lfovision_log/tsm_learningrate/lr_0.01_wd_0.0005_momentum_0.9_bn_true_cosine/config.py'
label = ' /lfovision_sthv2_breakfast/annotations/something-something-v2-labels.txt'
# assign the desired device.
device = torch.device('cuda:0')
cfg = Config.fromfile(fp_config)
cfg_options = {}
cfg.merge_from_dict(cfg_options)
# build the recognizer from a config file and checkpoint file/url
model = init_recognizer(fp_config, checkpoint, device=device)
weight = model.cls_head.fc_cls.weight.cpu().detach().numpy()
bias = model.cls_head.fc_cls.bias.cpu().detach().numpy()
# save the weight and bias to a file
outdir = checkpoint = '/lfovision_log/tsm_learningrate/lr_0.01_wd_0.0005_momentum_0.9_bn_true_cosine/'
np.save(osp.join(outdir, 'weight.npy'), weight)
np.save(osp.join(outdir, 'bias.npy'), bias)
# save image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
# show the weight and bias
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(weight, cmap=cm.jet)
ax.set_title('weight')
plt.savefig(osp.join(outdir, 'weight.png'))
