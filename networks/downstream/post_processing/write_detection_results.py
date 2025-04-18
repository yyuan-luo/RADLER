import json
import numpy as np

from networks.downstream.post_processing import post_process_single_frame


def get_class_name(class_id, classes):
    n_class = len(classes)
    if 0 <= class_id < n_class:
        class_name = classes[class_id]
    elif class_id == -1000:
        class_name = '__background'
    else:
        raise ValueError("Class ID is not defined")
    return class_name


def write_single_frame_detection_results(results, results_file, frame_id):
    max_dets, _ = results.shape
    with open('../../../networks/downstream/configs/object_config.json', 'r') as f:
        object_cfg = json.load(f)
    classes = object_cfg['classes']
    with open(results_file, 'a+') as f:
        for d in range(max_dets):
            cla_id = int(results[d, 0])
            if cla_id == -1:
                continue
            row_id = results[d, 1]
            col_id = results[d, 2]
            conf = results[d, 3]
            f.write("%d %s %d %d %.4f\n" % (int(frame_id), get_class_name(cla_id, classes), row_id, col_id, conf))


if __name__ == '__main__':
    output = np.load('/Users/yluo/Project/Radio-Vision-CityGML/datasets/test/visualize_sdm/test-1/000095_sdm.npy')
    for i in range(output.shape[0]):
        results = post_process_single_frame(output[i])
        write_single_frame_detection_results(results, './results.txt', i)
