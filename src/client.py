import os
from dotenv import load_dotenv
import schwabdev


# @st.cache_resource
def get_client(name="A"):
    global client

    load_dotenv()
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")
    client = schwabdev.Client(app_key, app_secret, show_linked=False)
    # print(client.accounts.accountNumbers().json())
    client.update_tokens_auto()  # update tokens automatically (except refresh token)
    # st.session_state.client = client
    return client
