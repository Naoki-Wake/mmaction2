import os
import os.path as osp

import mmcv
import pdb
data_file = '/dataset'
video_list = '/dataset/annotation/video_info_custom.csv' #'/dataset/annotation/video_info_new.csv'
anno_file = '/dataset/annotation/annotation_custom.json' #'/dataset/annotation/anet_anno_action.json'
rawframe_dir = '/dataset/rawframes'
action_name_list = '/dataset/annotation/action_name_custom.csv' #'action_name.csv'


def generate_rawframes_filelist():
    anet_annotations = mmcv.load(anno_file)

    videos = open(video_list).readlines()
    videos = [x.strip().split(',') for x in videos]
    attr_names = videos[0][1:]
    # the first line is 'video,numFrame,seconds,fps,rfps,subset,featureFrame'
    attr_names = [x.lower() for x in attr_names]
    attr_types = [int, float, float, float, str, int]

    video_annos = {}
    for line in videos[1:]:
        name = line[0]
        data = {}
        for attr_name, attr_type, attr_val in zip(attr_names, attr_types,
                                                  line[1:]):
            data[attr_name] = attr_type(attr_val)
        video_annos[name] = data

    # only keep downloaded videos
    video_annos = {
        k: v
        for k, v in video_annos.items() if k in anet_annotations
    }
    #pdb.set_trace()
    # update numframe
    for video in video_annos:
        pth = osp.join(rawframe_dir, video)
        if osp.exists(pth):
            num_imgs = len(os.listdir(pth))
            # one more rgb img than flow
            if (num_imgs - 1) % 3 == 0:
                print(video)
                num_frames = (num_imgs - 1) // 3
                print(str(video_annos[video]['numframe'])+'>'+str(num_frames))
                video_annos[video]['numframe'] = num_frames
            else:
                video_annos[video]['isValid'] = False
        else:
            video_annos[video]['isValid'] = False
    video_annos = {key:val for key, val in video_annos.items() if 'isValid' not in val.keys()} 
    #pdb.set_trace()
    
    anet_labels = open(action_name_list).readlines()
    anet_labels = [x.strip() for x in anet_labels[1:]]

    train_videos, val_videos, test_videos = {}, {}, {}
    for k, video in video_annos.items():
        if video['subset'] == 'training':
            train_videos[k] = video
        elif video['subset'] == 'validation':
            val_videos[k] = video
        elif video['subset'] == 'testing':
            test_videos [k] = video

    def simple_label(video_idx):
        anno = anet_annotations[video_idx]
        label = anno['annotations'][0]['label']
        return anet_labels.index(label)

    train_lines = [
        k + ' ' + str(train_videos[k]['numframe']) + ' ' +
        str(simple_label(k)) for k in train_videos
    ]
    val_lines = [
        k + ' ' + str(val_videos[k]['numframe']) + ' ' + str(simple_label(k))
        for k in val_videos
    ]
    test_lines = [
        k + ' ' + str(test_videos[k]['numframe']) + ' ' + str(simple_label(k))
        for k in test_videos
    ]    
    #pdb.set_trace()
    with open(osp.join(data_file, 'anet_train_video.txt'), 'w') as fout:
        fout.write('\n'.join(train_lines))
    with open(osp.join(data_file, 'anet_val_video.txt'), 'w') as fout:
        fout.write('\n'.join(val_lines))
    with open(osp.join(data_file, 'anet_test_video.txt'), 'w') as fout:
        fout.write('\n'.join(test_lines))

    def clip_list(k, anno, vidanno):
        num_seconds = anno['duration_second']
        num_frames = vidanno['numframe']
        fps = num_frames / num_seconds
        segs = anno['annotations']
        lines = []
        for seg in segs:
            segment = seg['segment']
            label = seg['label']
            label = anet_labels.index(label)
            start, end = int(segment[0] * fps), int(segment[1] * fps)
            if end > num_frames - 1:
                end = num_frames - 1
            newline = f'{k} {start} {end - start + 1} {label}'
            lines.append(newline)
        return lines

    train_clips, val_clips, test_clips = [], [], []
    for k in train_videos:
        train_clips.extend(clip_list(k, anet_annotations[k], train_videos[k]))
    for k in val_videos:
        val_clips.extend(clip_list(k, anet_annotations[k], val_videos[k]))
    for k in test_videos:
        test_clips.extend(clip_list(k, anet_annotations[k], test_videos[k]))

    with open(osp.join(data_file, 'anet_train_clip.txt'), 'w') as fout:
        fout.write('\n'.join(train_clips))
    with open(osp.join(data_file, 'anet_val_clip.txt'), 'w') as fout:
        fout.write('\n'.join(val_clips))
    with open(osp.join(data_file, 'anet_test_clip.txt'), 'w') as fout:
        fout.write('\n'.join(test_clips))

if __name__ == '__main__':
    generate_rawframes_filelist()
