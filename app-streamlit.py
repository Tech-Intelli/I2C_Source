import streamlit as st

COMPANY_NAME = "ExplAIstic"
COMPANY_LOGO = "Background.png"
BACKGROUND_IMAGE = "Background.png"


def generate_caption(image_path, video_path, caption_size):
    return f"Generated caption for image: {image_path}, video: {video_path}, size: {caption_size}"


def app():
    st.set_page_config(page_title=COMPANY_NAME, page_icon=COMPANY_LOGO)
    st.image(COMPANY_LOGO)
    st.markdown('<style>img { display: block; margin: auto; }</style>', unsafe_allow_html=True)
    st.markdown(f"""
        <style>
            body {{
                background-image: url('{BACKGROUND_IMAGE}');
                background-size: cover;
            }}
        </style>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])
    uploaded_video = st.file_uploader(
        "Upload Video", type=["mp4", "mov"])

    caption_size = st.slider("Caption Size", 1, 2, 3)

    if st.button("Generate Caption"):
        if uploaded_image is not None and uploaded_video is not None:
            st.error("Please upload only one of either an image or a video.")
        elif uploaded_image is None and uploaded_video is None:
            st.error("Please upload either an image or a video.")
        else:
            image_path = uploaded_image.name if uploaded_image is not None else None
            video_path = uploaded_video.name if uploaded_video is not None else None
            caption = generate_caption(image_path, video_path, caption_size)
            st.success(caption)


if __name__ == "__main__":
    app()
