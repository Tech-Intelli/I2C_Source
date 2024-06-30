
import time
from io import StringIO
import streamlit as st
import asyncio
from utils.timer import advanced_timer_decorator

@advanced_timer_decorator(threshold=1.0, log_to_console=True, log_return_value=True)
async def stream_text(stream, batch_size=5, sleep_time=0.01):
    """Generate and display stream text

    Args:
        stream: an iterable streaming API response
        batch_size: number of chunks to batch before updating the display
        sleep_time: time to sleep between batches
    """
    success_stream = st.empty()
    full_text_io = StringIO()
    batch = []

    for chunk in stream:
        message_content = chunk["message"]["content"].replace("\n", "<br>")
        batch.append(message_content)

        if len(batch) >= batch_size:
            full_text_io.write(''.join(batch))
            success_stream.markdown(full_text_io.getvalue(), unsafe_allow_html=True)
            batch = []
            await asyncio.sleep(sleep_time)

    # Write any remaining chunks
    if batch:
        full_text_io.write(''.join(batch))
        success_stream.markdown(full_text_io.getvalue(), unsafe_allow_html=True)

    success_stream.success(full_text_io.getvalue())