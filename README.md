[![Run Unit Tests](https://github.com/dasdipanjan04/ExplAIstic/actions/workflows/run_tests.yml/badge.svg?branch=main)](https://github.com/dasdipanjan04/ExplAIstic/actions/workflows/run_tests.yml) [![Pylint](https://github.com/dasdipanjan04/ExplAIstic/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/dasdipanjan04/ExplAIstic/actions/workflows/pylint.yml)
## ExplAIstic

![ExplAIstic Logo](/src/resources/Background.png)

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

ExplAIstic is licensed under the MIT license. See [LICENSE](LICENSE) for more information.

## Logo License
See [LOGO LICENSE](https://github.com/dasdipanjan04/ExplAIstic/blob/main/LOGO%20LICENSE) for more information.
## Acknowledgments 👏
Thank you to the PyTorch, OpenAI, and Hugging Face communities for providing pre-trained models that were instrumental in the creation of this project. Special thanks to the Telegram team for providing an easy-to-use API for messaging.

## Join the Discord Community
<a href="https://discord.gg/UvMWN7k7"><img class="icon-3AqZ2e" src="https://cdn.discordapp.com/icons/1097599444800770060/5bc54720d99c6bc7b86322a3b8683fd6.webp?size=240" alt=" " width="100" height="100" aria-hidden="true"></a>

