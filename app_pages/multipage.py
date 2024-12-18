import streamlit as st


# Class to generate multiple Streamlit pages using an object oriented approach
class MultiPage:

    def __init__(self, app_name) -> None:
        self.pages = []
        self.app_name = app_name

        st.set_page_config(
            page_title=self.app_name,
            page_icon=":herb:")

    def add_page(self, title, func) -> None:
        self.pages.append({"title": title, "function": func})

    def run(self):
        page = st.sidebar.radio('Menu', self.pages, format_func=lambda page: page['title'])
        page['function']()
        st.write('---')
        st.info(
            'For more detailed information, visit the project '
            'readme available here: \n'
            '[README](https://github.com/RaymondBrien/cherry-ml)'
        )