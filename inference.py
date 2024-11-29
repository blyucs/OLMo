from transformers import AutoModelForCausalLM, AutoTokenizer

# olmo = AutoModelForCausalLM.from_pretrained("/home/lvbo/hf_pt")
# tokenizer = AutoTokenizer.from_pretrained("/home/lvbo/hf_pt")
olmo = AutoModelForCausalLM.from_pretrained("/home/lvbo/hf_pt/OLMo-1B")
tokenizer = AutoTokenizer.from_pretrained("/home/lvbo/hf_pt/OLMo-1B")

message = ["Language is "]
# message = ["Mathmatics is "]
inputs = tokenizer(message, return_tensors='pt', return_token_type_ids=False)
response = olmo.generate(**inputs, max_new_tokens=100, do_sample=True, top_k=20, top_p=0.95)
print(tokenizer.batch_decode(response, skip_special_tokens=True)[0])