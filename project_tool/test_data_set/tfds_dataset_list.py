import tensorflow_datasets as tfds

all_datasets = tfds.list_builders()
print(f"共收录 {len(all_datasets)} 个数据集")
print("示例前 20 个：")
print(all_datasets[:20])