# I<sup>2</sup>Transformer: Intra- and Inter-relation Embedding Transformer for TV Show Captioning
This package contains the accompanying code for the following paper:

Tu, Yunbin, et al. ["I<sup>2</sup>Transformer: Intra- and Inter-relation Embedding Transformer for TV Show Captioning."](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9738841), which has appeared as regular paper in IEEE TIP。 

## We illustrate the training details as follows:

### 1. Prepare feature files
Download [tvc_feature_release.tar.gz ](https://drive.google.com/file/d/1bSjxbKSxp1qEBCSwAmk8YlkRl1ztgrWO/view?usp=sharing) (23GB).
After downloading the file, extract it to the `data` directory.
```
tar -xf path/to/tvc_feature_release.tar.gz -C data
```
You should be able to see `video_feature` under `data/tvc_feature_release` directory. 
It contains video features (ResNet, I3D, ResNet+I3D). Plase note that this code only used the features of ResNet+I3D.


### 2. Install dependencies:
- Ubuntu 16.04
- Python 2.7
- PyTorch 1.1.0
- nltk
- easydict
- tqdm
- h5py
- tensorboardX
- An RTX 2080Ti

### 3. Add project root to `PYTHONPATH`
```
source setup.sh
```
Note that you need to do this each time you start a new session.


### 4. Git clone the Microsoft COCO evaluation server to evaluate captions and place it in the dir: 'I2Transformer/standalone_eval/'
```
git clone https://github.com/tylin/coco-caption.git
```

### 5. Build Vocabulary
```
bash baselines/multimodal_transformer/scripts/build_vocab.sh
```
Running this command will build vocabulary `cache/tvc_word2idx.json` from TVC train set. 
 
### 6. I<sup>2</sup>Transformer training
```
bash baselines/multimodal_transformer/scripts/train.sh video_sub resnet_i3d
```
This code will load all the data (~30GB) into RAM to speed up training,
use `--no_core_driver` to disable this behavior. 

Training using the above config will stop at around epoch 22, around 7 hours with a single 2080Ti GPU.
You should get ~47.2 CIDEr and ~11.4 BLEU@4 scores on val set. 
The resulting model and config will be saved at a dir: `baselines/multimodal_transformer/results/video_sub-res-*`

### 7. I<sup>2</sup>Transformer inference
After training, you can inference using the saved model on val or test_public set:
```
bash baselines/multimodal_transformer/scripts/translate.sh MODEL_DIR_NAME SPLIT_NAME
```
`MODEL_DIR_NAME` is the name of the dir containing the saved model, 
e.g., `video_sub-res-*`.  `SPLIT_NAME` could be `val` or `test_public`. 

### 8. our results 
The generated captions and evaluation scores on the val and test_public set are in the dir: 'our_results'

## Citing
If you find this helps your research, please consider citing:
```
@article{tu2022i2transformer,
  title={I2Transformer: Intra-and Inter-relation Embedding Transformer for TV Show Captioning},
  author={Tu, Yunbin and Li, Liang and Su, Li and Gao, Shengxiang and Yan, Chenggang and Zha, Zheng-Jun and Yu, Zhengtao and Huang, Qingming},
  journal={IEEE Transactions on Image Processing},
  year={2022},
  publisher={IEEE}
}
```

## Contact
My email is tuyunbin1995@foxmail.com

Any discussions and suggestions are welcome!


## Acknowledgement
This work and code are inspired by [TVCaption](https://github.com/jayleicn/TVCaption). Thanks for their solid work!
