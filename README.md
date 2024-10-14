# 양자화와 랭그래프를 이용한 RAG 방법

### 사용 방법
- llama 3.1 8B모델 다운받기
```
https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/tree/main
```
___
- gguf파일로 양자화하기

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
___
- llama-cpp-python 설치하기

  - Microsoft C++ Build Tools 설치하기
  ```
  https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/
  ```

  - 환경변수 설정하기 (GPU사용)
  ```
  set FORCE_CMAKE="1"
  ```
  ```
  set CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCUDA_PATH=/usr/local/cuda-12.2 -DCUDAToolkit_ROOT=/usr/local/cuda-12.2 -DCUDAToolkit_INCLUDE_DIR=/usr/local/cuda-12/include -DCUDAToolkit_LIBRARY_DIR=/usr/local/cuda-12.2/lib64"
  ```

  - cuda12.2 설치하기
  ```
  conda install -c "nvidia/label/cuda-12.2.0" cuda-toolkit
  ```

  - llama-cpp-python(cuda12.2) 설치하기
  ```
  python -m pip install llama-cpp-python --prefer-binary --extra-index-url=https://abetlen.github.io/llama-cpp-python/whl/cu122
  ```
  
    - CPU version으로 먼저 설치되어 있다면, 지우고(pip uninstall llama-cpp-python) GPU version으로 다시 설치해야함
