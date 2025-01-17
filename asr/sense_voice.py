from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import streamlit as st

model_dir = "iic/SenseVoiceSmall"

@st.cache_resource
def load_asr_model():
	model = AutoModel(
		model=model_dir,
		trust_remote_code=True,
		remote_code="./model.py",  
		vad_model="fsmn-vad",
		vad_kwargs={"max_single_segment_time": 30000},
		device="cuda:0",
	)
	return model

def get_asr_text(model, absolute_audio_path):
	res = model.generate(
		input=absolute_audio_path,
		cache={},
		language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
		use_itn=True,
		batch_size_s=60,
		merge_vad=True,
		merge_length_s=15,
	)
	text = rich_transcription_postprocess(res[0]["text"])
	return res[0]["text"]