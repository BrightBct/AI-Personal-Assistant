import torch

from transformers import T5Tokenizer
from transformers import T5ForConditionalGeneration
from text_sum import image_summarization
from text_sum import url_summarization
from practice_english import practice_english

model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')
device = torch.device('cpu')

menu = "What do you want to do?\n" \
       "1.Summarization\n" \
       "2.Practice English\n" \
       "3...\n" \
       "4.Exit Program\n: "

while True:
    status = int(input(menu))
    if status == 1:
        while True:
            iou = int(input("\nSummarization\n"
                            "1.Image Url Summarization\n"
                            "2.Url Summarization (Wiki Url)\n"
                            "3.Search on Wiki\n"
                            "4.Exit from Summarization\n: "))
            if iou == 1:
                image_summarization.image_sum(model, tokenizer, device)
            elif iou == 2:
                url_summarization.url_sum(model, tokenizer, device)
            elif iou == 3:
                url_summarization.search_wiki(model, tokenizer, device)
            elif iou == 4:
                print("Quit from Summarization\n")
                break
            else:
                print("Invalid Input\n")
    elif status == 2:
        practice_english.english_practice()
    elif status == 4:
        print("End off program")
        break
    else:
        print("Invalid Input!\n")
