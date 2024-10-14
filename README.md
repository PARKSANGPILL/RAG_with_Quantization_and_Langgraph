# 양자화와 랭그래프를 이용한 RAG 방법

### 사용 방법
- llama 3.1 8B모델 다운받기
```
https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/tree/main
```

- gguf파일로 양자화하기
___
  - llama.cpp 클론하기
  ```
  git clone https://github.com/ggerganov/llama.cpp.git
  ```
  ```
  cd llama.cpp
  ```

  - requirements.txt 설치
  ```
  pip install -r requirements.txt
  ```

  - huggingface에서 받은 모델을 gguf로 변환하기 (양자화)
  ```
  python convert-hf-to-gguf.py 허깅페이스모델경로 --outtype q8_0
  ```

  - --outtype 옵션에는 f32, f16, bf16, q8_0, auto가 있음

- llama-cpp-python 설치하기
___
  - 환경변수 설정하기 (GPU사용)
  ```
  set CMAKE_ARGS="-DGGML_CUDA=on"
  ```
  ```
  pip install llama-cpp-python
  ```
