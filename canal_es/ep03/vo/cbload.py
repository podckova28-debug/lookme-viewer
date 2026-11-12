from pathlib import Path
import torch
from safetensors.torch import load_file
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals
from chatterbox.models.t3 import T3
from chatterbox.models.t3.modules.t3_config import T3Config
from chatterbox.models.s3gen import S3Gen
from chatterbox.models.tokenizers import MTLTokenizer
from chatterbox.models.voice_encoder import VoiceEncoder
def load_latam(d="ckpt_latam", device="cpu"):
    d=Path(d); cpu=torch.device("cpu")
    ve=VoiceEncoder(); ve.load_state_dict(torch.load(d/"ve.pt",map_location=cpu,weights_only=True)); ve.eval()
    t3=T3(T3Config.multilingual()); st=load_file(d/"t3_es_mx_latam.safetensors")
    if "model" in st: st=st["model"][0]
    t3.load_state_dict(st); t3.eval()
    s3=S3Gen(); missing,unexpected=s3.load_state_dict(torch.load(d/"s3gen.pt",map_location=cpu,weights_only=True),strict=False)
    bad=[k for k in missing if not k.startswith("tokenizer.")]
    assert not bad and not unexpected, (bad, unexpected)
    s3.eval()
    tok=MTLTokenizer(str(d/"grapheme_mtl_merged_expanded_v1.json"))
    conds=Conditionals.load(d/"conds.pt",map_location=cpu).to(device) if (d/"conds.pt").exists() else None
    return ChatterboxMultilingualTTS(t3,s3,ve,tok,device,conds=conds)
