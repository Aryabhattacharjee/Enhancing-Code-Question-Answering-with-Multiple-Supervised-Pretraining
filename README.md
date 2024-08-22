# Enhancing-Code-Question-Answering-with-Multiple-Supervised-Pretraining

## Introduction
The objective of this project is to make a code-question-answering model with two different pretraining strategy to achieve improved performance metric. I used CodeT5+ model as a base model.

## Dataset
Two primary datasets were utilized: CodeSum and CodeQA.  
• CodeSum: This dataset consists of 465,939 rows, where each row contains a Java code snippet along with its corresponding description. The CodeSum dataset is primarily used for code summarization tasks, where the goal is to generate a concise and accurate description of a given code snippet.  
• CodeQA: The CodeQA dataset is split into three subsets: training, testing, and development. The training set contains 95,778 rows, while the testing and development sets each contain 12,000 rows. This dataset is designed for code question answering tasks, where the aim is to generate accurate answers to questions related to the given code snippets.  

## Data Cleaning

• Duplicate Removal: Initially, the CodeSum dataset contained a significant number of duplicate rows which were identified and removed, reducing the total number of rows to 269,270.  
• URL Removal: The descriptions in the CodeSum dataset contained approximately 550 unnecessary URLs. Using Python’s urllib library, these URLs were systematically removed to clean the text data.  
• Dataset Consistency Check: To ensure the integrity of the training, testing, and development sets in the CodeQA dataset, we checked if any code snippets in the development and testing sets were duplicated in the training set. This was done to avoid data leakage and ensure a fair evaluation. No matches were found, confirming the datasets’ consistency.

## Methodology

#### Code Annotation: 
For the pre-training task of code-to-description generation, a custom script was developed in Python using the javalang library. This script annotates the most important parts of the Java code, helping the model distinguish between different elements. The annotations used are:  
– [U VARIABLE]: User-defined variable  
– [U CLASS]: User-defined class  
– [U METHOD]: User-defined method  
– [R]: Reserved keyword  
– [S CLASS]: System class  
– [S PACKAGE]: System package  
– [S METHOD]: System method  
  
#### Description Completion Task:
The training process for the code-to-description task involves several key steps:  
  
Data Loading and Preparation:  
train_processed.code contains annotated code snippets.  
clean_ur_train.comment includes corresponding natural language descriptions.  
  
Preprocessing:  
Code snippets are truncated to 499 tokens, and descriptions to 99 tokens.  
Code snippets are appended with <extra id 0> and descriptions with the End Of Sequence (EOS) token.  
  
Train Dataset Creation:  
The preprocessed data is organized into a Pandas DataFrame and then converted into a Hugging Face Dataset object for efficient tokenization and training.  
  
Tokenization:  
A tokenization function processes the code and descriptions, ensuring they fit within the model’s input constraints.Tokenized descriptions are set as target labels for supervised learning.  
  
Training and Evaluation Split:  
95% of the data is used for training. 5% is reserved for evaluating the model's performance.  
  
Training Configuration:  
![image](https://github.com/user-attachments/assets/e0a3f44c-2bca-4e84-a45a-eaa9b395e9e5)  

#### Partial Description Generation Summary
Tokenization:  
Input code is limited to a maximum of 450 tokens.  
Partial description is Limited to a maximum of 50 tokens.  
Generated description is limited to a maximum of 30 tokens.  
The model is trained to generate the remaining part of a description when provided with both the code and a partial description, helping it learn to complete descriptions based on partial information.  
![image](https://github.com/user-attachments/assets/65157ef7-f7eb-49b5-b332-23b43d810d83)

![image](https://github.com/user-attachments/assets/3a2320d1-f0e2-4d3c-99c5-2155865be883)


Training Procedure:  
The training setup mirrors the code-to-description task, but with different input and output token limits.  
The model focuses on completing partial descriptions, improving its ability to generate coherent and contextually relevant descriptions.  

#### QLoRA Fine-tune
The model is then fine tuned on the the CodeQA dataset, for 15 epoch. I used 4-bit quantization for the training. The final result is as follows  
BLEU: 40.46  
ROUGE-L: 39.95  
METEOR: 16.40  
EM: 14.33  
F1: 41.09

