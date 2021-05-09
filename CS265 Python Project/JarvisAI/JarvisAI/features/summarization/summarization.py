import torch
from JarvisAI.JarvisAI.features.summarization.sum import url_summarization, image_summarization

from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')
device = torch.device('cpu')


def summarization(iou):
    if iou == 1:
        image_summarization.image_sum(model, tokenizer, device)
    elif iou == 2:
        url_summarization.url_sum(model, tokenizer, device)
    elif iou == 3:
        url_summarization.search_wiki(model, tokenizer, device)


if __name__ == '__main__':
    model = T5ForConditionalGeneration.from_pretrained('t5-base')
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    device = torch.device('cpu')
    summarization()
