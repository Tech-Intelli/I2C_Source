import base64
import streamlit as st


def generate_interim_gif(GIPHY_IMAGE):
    """
    Generates gif placeholder

    Returns:
        str: gif placeholder
    """

    gif_placeholder = None
    with open(GIPHY_IMAGE, "rb") as file_gif:
        contents = file_gif.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_gif.close()
        gif_placeholder = st.empty()
        gif_placeholder.markdown(
            f"""<img src="data:image/gif;base64,
                {data_url}" alt="explaistic gif">""",
            unsafe_allow_html=True,
        )
    return gif_placeholder
