import sys
# caution: path[0] is reserved for script path
sys.path.insert(1, '/home/arya/my_python/my_torch/cq')
from useful_function import processed_write


input_file = "/home/arya/my_python/my_torch/cq/noun_data/clean_train.code"
output_file = "/home/arya/my_python/my_torch/cq/noun_data/train_processed.code"

processed_write(input_file,output_file)
