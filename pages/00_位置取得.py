import streamlit as st
from streamlit_js_eval import streamlit_js_eval


def get_location():
    # JavaScript で `navigator.geolocation` を使って位置情報を取得
    coords = streamlit_js_eval(
        js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
        want_output=True,
        key="get_location",
    )

    if coords:
        return coords["latitude"], coords["longitude"]

    return None, None


# Streamlit UI
st.title("📍 スマホの現在位置を取得")

latitude, longitude = get_location()

if latitude is not None:
    st.success(f"✅ 緯度: {latitude}, 経度: {longitude}")
else:
    st.warning("⏳ 位置情報を取得中...")

# デバッグ用に session_state を表示
st.write(st.session_state)
