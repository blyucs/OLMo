import pandas as pd
import numpy as np
# 加载.npy文件
loaded_data = np.load('/home/lvbo/olmo_data/output_olmo/0_00000.npy',allow_pickle=True)

# 将NumPy数组转换为DataFrame
loaded_df = pd.DataFrame(loaded_data)
print(loaded_df[0][0])