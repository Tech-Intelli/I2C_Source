[![Unit Tests](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/run_tests.yml/badge.svg?branch=main)](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/run_tests.yml) [![Pylint](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/pylint.yml) [![Docs](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/documentation.yml/badge.svg?branch=main)](https://github.com/Tech-Intelli/I2C_Source/actions/workflows/documentation.yml)

## ExplAIstic

ExplAIstic is an image captioning and image hashtagging application that generates nicely written captions and adds related hashtags to your images and reels. It utilizes pre-trained Imagenet models and ChatGPT for the image analysis and caption generation, and the Telegram API for the messaging feature.

## Installation 🚀

To use the application, you need to install the following dependencies:

- Python 3.10 (All the dependencies don't support Python 3.11)
- Flask==2.2.3
- openai==0.27.2
- opencv_python==4.7.0.72
- Pillow==9.5.0
- python-telegram-bot==20.2
- streamlit==1.21.0
- torch==2.0.0
- transformers==4.27.4
- boto3
- ritetag
- pytest
- pytest-mock
- dnspython
- email-validator
- PyJWT

You can install all of these dependencies by running `pip install -r requirements.txt` from the project directory.

The current version of ExplAIstic uses Streamlit to generate the website. To use this app run

```
cd src
streamlit run app-streamlit.py
```

An endpoint to generate the caption has been created. Run the following command:

```
Open one termianl
cd src
python app_endpoints.py
```

Open another termianl

## Register

```
curl -X POST -H "Content-Type: application/json" -d '{"email":"example@email.com","password":"password"}' http://localhost:9000/register_user --cookie-jar cookies.txt
```

## login

```
curl -X POST -H "Content-Type: application/json" -d '{"email":"example@email.com","password":"password"}' http://localhost:9000/login_user --cookie-jar cookies.txt
```

## Upload Image or Video

```
curl -X POST -H "Content-Type: multipart/form-data" \
    -H "Authorization: Bearer your-token" \
    -F "file=@/path/to/your/file.jpg" \
    --cookie cookies.txt \
    http://localhost:9000/upload_file \
    --cookie-jar cookies.txt
```

## Generate Caption

```
curl -X GET 
    -H "Authorization: Bearer your-token" \
    "http://localhost:9000/generate_image_video_caption?caption_size=small&context=some_context&style=cool&num_hashtags=3&tone=casual&social_media=instagram" \
    --cookie cookies.txt
```

## How to run the Dockerfile

If you want to containerize it and run it as a Docker image use the Dockerfile from the root of the repo. Add your API keys there. As this use pre-trained model, therefore initializing the pre-trained model everytime can be memory expensive and time consuming. Use a Docker Volume before running the docker file.

```
docker volume create explaistic_volume
docker build -t explaistic_docker .
docker run -v explaistic_volume:/app/data -p 8501:8501 explaistic_docker
```

If you are using a Mac with M1 or M2 Chip and encountering `RuntimeError: torch.UntypedStorage(): Storage device not recognized: mps` use the following command instead

```
docker volume create explaistic_volume
docker buildx create --use --name explaisticbuilder
docker buildx build --platform linux/amd64,linux/arm64 -t explaistic_docker .
docker run -v explaistic_volume:/app/data -p 8501:8501 explaistic_docker
```

## Contributing 🤝

If you find any bugs or issues, feel free to open an issue on GitHub. Pull requests are also welcome!

## Credits 🙏

ExplAIstic was created by [Dipanjan Das](https://github.com/dasdipanjan04). It utilizes pre-trained Imagenet models from PyTorch, ChatGPT from OpenAI, and the transformers package from Hugging Face. The Telegram API was used for messaging.

## License 📝

ExplAIstic is licensed under the Proprietary Software License. See [LICENSE](LICENSE) for more informatio

## Acknowledgments 👏

Thank you to the PyTorch, OpenAI, and Hugging Face communities for providing pre-trained models that were instrumental in the creation of this project. Special thanks to the Telegram team for providing an easy-to-use API for messaging.

## Join the Discord Community

`<a href="https://discord.gg/UvMWN7k7"><img class="icon-3AqZ2e"  src="https://cdn.discordapp.com/icons/1097599444800770060/5bc54720d99c6bc7b86322a3b8683fd6.webp?size=240" alt=" " width="100" height="100" aria-hidden="true">``</a>`

## ==================================================================

## IMPORTANT NOTE:

This application can have OOM (Out of Memory) problem if you are using conda which will eventually lead to the following problem

```
_pickle.PicklingError: Can't pickle <class 'builtins.safe_open'>: it's not found as builtins.safe_open
```

_***Therefore, it is strongly advised to install python 3.10 and install packages globally on your python environment.***_

After the installation of python 3.10 check your python version using

```
python --version
```

If it gives any version below 3.10 uninstall that python version immediately and remove the associated paths from user and system environment variable.

If it gives anything other than 3.10 meaning you have other python versions installed then try the following:

```
C:\Users\<USER_NAME>\AppData\Local\Programs\Python\Python310\python.exe --version
```

## Download Conda

Download [MiniConda](https://docs.anaconda.com/miniconda/) or [Anaconda](https://www.anaconda.com/download/) for Windows. I am personally using Anaconda this comes with a GUI and CLI installer.
Simply provide your email address and download the Anaconda distribution for Windows.

## Download and Install Cuda Toolkit

As we will be using out gpus, it is important to install the cuda toolkit in order to make the torch and transformer function properly on the gpus
Use the link to download [cuda toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local)
If you are using anything other than Windows 11, just select the appropriate platform from the platform selector in the link. Install the cuda toolkit and restart your pc.
It is important to restart your pc after the installation of the cuda toolkit.

## Create a Conda Environment at your desired directory

Installing conda will create the basic conda environment in the system's directory, after the installation of Conda use the following command to create a conda environment at your desired location. You can create multiple conda environments if you want, therefore it is important to have a dedicated directory for all the conda environments. I have created a directory named
`conda_env`where I create all my needed conda environments. Open a terminal and execute the following command. It is important to remember that after the installation it is crucial to restart your terminal. Once the installation is complete test with the following command whether Conda CLI has been activated.

```
conda --help
```

If that works go on with the next command, otherwise just restart your pc and continue

```
conda create --prefix D:\Codes_All\Development\conda_envs\Image_Video_Caption_AI_py310 python=3.10
```

## Activate Conda Environment

Use the following command to activate your conda environment

```
conda activate D:\Codes_All\Development\conda_envs\Image_Video_Caption_AI_py310
```

## Install pytorch, torchvision and trochaudio

Installation of pytorch requires some environment selection from the [link](https://pytorch.org/get-started/locally/)
Precisely, you will need to execute the following command in your conda environment

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

***if you are not using conda meaning installing python packages globally***

```
C:\Users\<USER_NAME>\AppData\Local\Programs\Python\Python310\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

if your default python version is 3.10 then replace `C:\Users\<USER_NAME>\AppData\Local\Programs\Python\Python310\python.exe` with `python`

After this stage enable a python terminal within the conda environment and check whether torch is able to access your gpu

```
python -c "import torch; print(torch.cuda.is_available())"
```

If torch is able to access the gpu, this should print `True`

## Checkout Transformers from Github

The current realeased version of Transformer library does not yet support the bits and bytes, blip2 with 8 bit quantization, therefore we will directly install the updated code base.
Use the following command to checkout the latest transformers library.

```
cd \path\to\your\desired\lodation\where\you\want\to\checkout (DO NOT CHECK TRANSFORMERS INSIDE OF THIS REPOSITORY)
git clone https://github.com/huggingface/transformers.git
```

```
cd transformers
pip install -e .
```

At the end of the installation you may get the following ERROR:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
torch 2.3.1 requires mkl<=2021.4.0,>=2021.1.1; platform_system == "Windows", which is not installed.
```

Don't worry about it because we will not be needing mkl rightnow.

## Download and Install Ollama

[Download](https://ollama.com/download/OllamaSetup.exe) the ollama setup.exe and install.

## Install Pip Dependencies

Once all the previous steps are done, do the following

```
cd \path\to\I2C_Source
pip install -r requirements_updated.txt
```

You might get an ERROR like the following if you already have ipython notebook install as a part of anaconda installation.
You don't have to worry about this, we will not be using ipython notebook or google collab in this project,

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
ipykernel 6.29.4 requires ipython>=7.23.1, which is not installed.
ipykernel 6.29.4 requires matplotlib-inline>=0.1, which is not installed.
ipykernel 6.29.4 requires traitlets>=5.4.0, which is not installed.
jupyter-client 8.6.1 requires traitlets>=5.3, which is not installed.
```

But you need to take action on the following error message if that happens

```
AttributeError: partially initialized module 'charset_normalizer' has no attribute 'md__mypyc' (most likely due to a circular import)
```

In order to resolve the error use the following command

```
pip install -U --force-reinstall charset-normalizer
pip install -U --force-reinstall numpy<1.24
```

## Model Initialization and Cache Creation

Check whether your Ollama is running

If it is not running start it from the application or simply execute the following command

```
ollama serve
```

Once these are done
Use the following command to create the model cache

```
cd src
python -m streamlit run app_streamlit.py
```

or if you are not using conda then the following

```
C:\Users\dasdi\AppData\Local\Programs\Python\Python310\python.exe -m streamlit run .\app_streamlit.py
```
