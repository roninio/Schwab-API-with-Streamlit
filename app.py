import streamlit as st
import hmac



if "password_correct" not in st.session_state:
    st.session_state.password_correct = False



def check_password():
    """Returns `True` if the user had the correct password.

    Add below file:
           .streamlit/secrets.toml

          password = "streamlit123"
    """

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def login():
    if check_password():
        st.rerun()


def logout():
    if st.button("Log out"):
        st.session_state["password_correct"] = False
    
        st.Page(login, title="Log out", icon=":material/logout:")
        st.rerun()


if not check_password():
    st.stop()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "ui/user.py", title="Account", icon=":material/dashboard:", default=True
)
# bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
option_trade_page = st.Page(
    "ui/optionchain_flow.py", title="Option trade", icon=":material/notification_important:"
)

chart = st.Page("ui/chart.py", title="Chart", icon=":material/finance_mode:")


if st.session_state.password_correct:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, option_trade_page, chart],
            # "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
