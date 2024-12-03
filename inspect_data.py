import numpy as np
from cached_path import cached_path

from olmo.config import TrainConfig
from olmo.data import build_memmap_dataset

# Update these paths to what you want:
data_order_file_path = cached_path("/home/lvbo/05_npy_all_common/Run_20241125-114925_2000_to_4000_0_00000.npy")  # 这个应该是流程中生产的。 用于训练中使用。
train_config_path = "configs/tiny-my/OLMo-120M.yaml"


cfg = TrainConfig.load(train_config_path)
dataset = build_memmap_dataset(cfg, cfg.data)
# 把 yaml 对应的data数据全部映射到内存中，例{'path': 'https://olmo-data.org/preprocessed/olmo-mix/v1_5-sample/
# gpt-neox-20b-pii-special/part-000-00000.npy'}如，有0~2621438 个2048 token的片段。
# 疑问是为什么映射这么快？下载下来了才映射吗？
batch_size = cfg.global_train_batch_size
global_indices = np.memmap(data_order_file_path, mode="r+", dtype=np.uint16)


def get_batch_instances(batch_idx: int) -> list[list[int]]:
    batch_start = batch_idx * batch_size
    batch_end = (batch_idx + 1) * batch_size
    batch_indices = global_indices[batch_start:batch_end]
    batch_instances = []
    for index in batch_indices:
        token_ids = dataset[index]["input_ids"].tolist()
        batch_instances.append(token_ids)
    return batch_instances


# Get all 2048 x 2048 token IDs in the first batch.
get_batch_instances(0)