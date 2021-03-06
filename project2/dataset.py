import tensorflow as tf
import csv
import numpy as np

RATE_TRAIN = "ee412.train"
RATE_TEST = "ee412.testset.csv"
TEST_DATA_SIZE = 10000
TIME_MIN = 874700000
TIME_MAX = 893300000
USER_MAX = 943
ITEM_MAX = 1682

DATA_FEATURE_SIZE = USER_MAX + ITEM_MAX + 1

def load_dataset(is_train=True):
    File_name = None
    if(is_train):
        File_name = RATE_TRAIN
    else:
        File_name = RATE_TEST
    with open(File_name) as f:
        if(is_train):
            data_read = csv.reader(f, delimiter="\t")
        else:
            data_read = csv.reader(f, delimiter=",")
        data_list = list(data_read)
	    #data_len = len(data_list)
	    #train_data_end = data_len - TEST_DATA_SIZE
	    #find_data = np.array(data_list)[:,[3]]
	    #find_data = find_data.astype(np.float32)
	    #print np.amax(find_data),np.amin(find_data)
	    #if (is_train):
	    #	data_list = data_list[:train_data_end]
	    #else:
	    #	data_list = data_list[train_data_end:]
    #print data_list
    if(is_train):
    	data_features_raw = np.array(data_list)[:,[0,1,3]]
    else:
    	data_features_raw = np.array(data_list)[:,[0,1,2]]
    data_features_raw = data_features_raw.astype(np.float32)
    data_features_raw[:,[2]] = (data_features_raw[:,[2]] - TIME_MIN )/(TIME_MAX-TIME_MIN)

    dataset_size = data_features_raw.shape[0]
    data_features = np.zeros((dataset_size, DATA_FEATURE_SIZE))
    user_data = data_features_raw[:,0].astype(np.int).reshape(dataset_size)
    item_data = data_features_raw[:,1].astype(np.int).reshape(dataset_size)
    time_data = data_features_raw[:,2].reshape(dataset_size)
    #print np.where(user_data == 943)[0]
    #data_features[np.arange(DATA_SIZE),data_features_raw[:,[0]].astype(np.int)] = 1
    data_features[np.arange(dataset_size), user_data-1] = 1
    data_features[np.arange(dataset_size), item_data-1 + USER_MAX] = 1
    data_features[np.arange(dataset_size), USER_MAX + ITEM_MAX] = time_data
    data_features = data_features.astype(np.float32)
    #np.set_printoptions(threshold=np.nan)

    if(is_train):
        data_labels = np.array(data_list)[:,[2]]
        data_labels = data_labels.astype(np.float32)
    else:
        data_labels = np.zeros((dataset_size,1))

    return data_features, data_labels

#features, labels = load_dataset(False)
#print (features.shape,labels.shape)
