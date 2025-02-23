from transformers import AutoModel, AutoTokenizer
# Configuración del modelo GOT_OCR2_0
tokenizer = AutoTokenizer.from_pretrained('srimanth-d/GOT_CPU', trust_remote_code=True)
model = AutoModel.from_pretrained(
    'srimanth-d/GOT_CPU',
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    use_safetensors=True,
    pad_token_id=tokenizer.eos_token_id
).eval()