from transformers import BartTokenizer, BartForConditionalGeneration

def download_model():
    model_name = 'facebook/bart-large-cnn'
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer.save_pretrained('./bart-large-cnn')
    model.save_pretrained('./bart-large-cnn')

if __name__ == "__main__":
    download_model()
