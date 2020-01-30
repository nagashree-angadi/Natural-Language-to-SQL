# Natural-Language-to-SQL

The text generation problem of generating SQL queries from natural language has long been a popular and useful task attracting considerable interest among researchers. The de facto approach used is to a sequence-to-sequence model but it suffers from having multiple equivalent queries to the same SQL. 

SQLNet [1] solves this problem by avoiding the sequence-to-sequence structure when the order does not matter by employing a sketch-based approach. We observed that SQLNet does not apply weight sharing mechanism for the question and the table header encoding. 

In this project, we propose the various models as an alternative to overcome the findings and suggestions to the state of the art SQLNet model: (1) The information learned from one sub-module is passed on to the next by the mechanism of weight sharing. (2) We leverage pre-trained BERT embeddings for word representations (3) To get better representations for natural language questions, we employ a bidirectional attention flow model for learning the representations.

## From the paper

> Xiaojun Xu, Chang Liu, Dawn Song. 2017. SQLNet: Generating Structured Queries from Natural Language Without Reinforcement Learning.

## Installation
The data is in `data.tar.bz2`. Unzip the code by running
```bash
tar -xjvf data.tar.bz2
```
Install other dependency by running 
```bash
pip install -r requirements.txt
```

Additional Requirements for Bert:

pip install bert-embedding
If you want to run on GPU machine, please install `mxnet-cu92`.
pip install mxnet-cu92

## Extract the bert embedding for training.
Run the following command to process the pretrained glove embedding for training the word embedding:
```bash
python extract_vocab.py
```

## Train
Train a SQLNet model with column attention:
```bash
python train.py --ca
```

## Test
Test a trained SQLNet model with column attention
```bash
python test.py --ca
```
