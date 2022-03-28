import argparse
import os
import nltk
import torch
import numpy as np
from tqdm import tqdm
from utils.basic_utils import load_json, flat_list_of_lists, save_json, load_jsonl
from baselines.multimodal_transformer.transformer.tvc_dataset import TVCaptionDataset


def build_vocab_idx(word_insts, min_word_count):
    full_vocab = set(w for sent in word_insts for w in sent)
    print("[Info] Original Vocabulary size =", len(full_vocab))

    word2idx = {
        TVCaptionDataset.PAD_TOKEN: TVCaptionDataset.PAD,
        TVCaptionDataset.CLS_TOKEN: TVCaptionDataset.CLS,
        TVCaptionDataset.SEP_TOKEN: TVCaptionDataset.SEP,
        TVCaptionDataset.VID_TOKEN: TVCaptionDataset.VID,
        TVCaptionDataset.BOS_TOKEN: TVCaptionDataset.BOS,
        TVCaptionDataset.EOS_TOKEN: TVCaptionDataset.EOS,
        TVCaptionDataset.UNK_TOKEN: TVCaptionDataset.UNK,
    }

    word_count = {w: 0 for w in full_vocab}

    for sent in word_insts:
        for word in sent:
            word_count[word] += 1

    ignored_word_count = 0
    for word, count in word_count.items():
        if word not in word2idx:
            if count > min_word_count:
                word2idx[word] = len(word2idx)
            else:
                ignored_word_count += 1

    print("[Info] Trimmed vocabulary size = {},".format(len(word2idx)),
          "each with minimum occurrence = {}".format(min_word_count))
    print("[Info] Ignored word count = {}".format(ignored_word_count))
    return word2idx


def load_transform_data(data_path):
    data = load_json(data_path)
    transformed_data = []
    for v_id, cap in data.items():
        cap["v_id"] = v_id
        transformed_data.append(cap)
    return transformed_data


def load_glove(filename):
    """ returns { word (str) : vector_embedding (torch.FloatTensor) }
    """
    glove = {}
    with open(filename) as f:
        for line in f.readlines():
            values = line.strip("\n").split(" ")  # space separator
            word = values[0]
            vector = np.asarray([float(e) for e in values[1:]])
            glove[word] = vector
    return glove


def extract_glove(word2idx, raw_glove_path, vocab_glove_path, glove_dim=300):
    # Make glove embedding.
    print("Loading glove embedding at path : {}.\n".format(raw_glove_path))
    glove_full = load_glove(raw_glove_path)
    print("Glove Loaded, building word2idx, idx2word mapping.\n")
    idx2word = {v: k for k, v in word2idx.items()}

    glove_matrix = np.zeros([len(word2idx), glove_dim])
    glove_keys = glove_full.keys()
    for i in tqdm(range(len(idx2word))):
        w = idx2word[i]
        w_embed = glove_full[w] if w in glove_keys else np.random.randn(glove_dim) * 0.4
        glove_matrix[i, :] = w_embed
    print("vocab embedding size is :", glove_matrix.shape)
    torch.save(glove_matrix, vocab_glove_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_path", type=str, default="/data/tvc_train_release.jsonl")
    parser.add_argument("--dset_name", type=str, default="tvc", choices=["tvc"])
    parser.add_argument("--cache", type=str, default="./cache")
    parser.add_argument("--min_word_count", type=int, default=5)
    parser.add_argument("--raw_glove_path", type=str, help="downloaded glove vectors path")

    opt = parser.parse_args()
    if not os.path.exists(opt.cache):
        os.makedirs(opt.cache)

    # load, merge, clean, split data
    train_datalist = load_jsonl(opt.train_path)
    all_sentences = flat_list_of_lists([[sub_e["desc"] for sub_e in e["descs"]] for e in train_datalist])
    all_sentences = [nltk.tokenize.word_tokenize(sen.lower()) for sen in all_sentences]
    word2idx = build_vocab_idx(all_sentences, opt.min_word_count)
    print("[Info] Dumping the processed data to json file", opt.cache)
    save_json(word2idx, os.path.join(opt.cache, "{}_word2idx.json".format(opt.dset_name)))
    print("[Info] Finish.")

    if opt.raw_glove_path:
        vocab_glove_path = os.path.join(opt.cache, "{}_vocab_glove.pt".format(opt.dset_name))
        extract_glove(word2idx, opt.raw_glove_path, vocab_glove_path)


if __name__ == "__main__":
    main()
