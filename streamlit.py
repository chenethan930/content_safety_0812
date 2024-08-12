from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
import streamlit as st
import pandas as pd
import numpy as np
key = st.secrets['key']
endpoint = st.secrets['endpoint']

st.title('亂說話測試')
prompt = st.text_input('請輸入訊息')
if prompt:

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    blocklist_name = "block_0812"

    content = prompt

    # Construct a request
    request = AnalyzeTextOptions(text=content, blocklist_names=[blocklist_name], halt_on_blocklist_hit=False)

    # Analyze text
    try:
        response = client.analyze_text(request)
        if response and response.blocklists_match:
                print("\nBlocklist match results: ")
                for match_result in response.blocklists_match:
                    print(
                        f"BlocklistName: {match_result.blocklist_name}, BlockItemId: {match_result.blocklist_item_id}, "
                        f"BlockItemText: {match_result.blocklist_item_text}"
                    )
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")

        st.markdown("#")
        st.caption('仇恨指標')
        st.write(f"Hate severity: {hate_result.severity}")

        st.markdown("#")
        st.caption('色情指標')
        st.write(f"Sexual severity: {sexual_result.severity}")

        st.markdown("#")
        st.caption('暴力指標')
        st.write(f"Violence severity: {violence_result.severity}")

        st.markdown("#")
        st.caption('自殘指標')
        st.write(f"Self Harm severity: {self_harm_result.severity}")



