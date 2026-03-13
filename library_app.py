import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज कन्फिगरेसन
st.set_page_config(page_title="JYC Digital Portal", layout="wide", page_icon="📚")

# --- Google Sheets URL (सुधारिएको ढाँचा) ---
# अन्तिमको /edit... हटाएर सिधै ID मात्र प्रयोग गर्दा वा यो ढाँचामा राख्दा राम्रो हुन्छ
LIBRARY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1bSnwkrm6MQ1nq31FC4NVAkdDAVSQHKMrVa42Wg8ryXs/edit?usp=sharing"
WARD_SHEET_URL = "तपाईंको_Development_Sheet_को_लिंक"

# कनेक्सन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

# --- साइडबार मेनु ---
# फोटो लोड गर्दा एरर नआओस् भनेर try-except राखिएको छ
try:
    st.sidebar.image("307286262_1066058600717181_5062110872657776485_n.jpg", width=150)
except:
    st.sidebar.title("JYC Logo")

st.sidebar.title("डिजिटल मिर्चैया-८")
menu = ["🏠 गृहपृष्ठ", "📖 डिजिटल पुस्तकालय", "📊 वडा विकास ड्यासबोर्ड", "ℹ️ हाम्रो बारेमा"]
choice = st.sidebar.selectbox("मेनु छान्नुहोस्", menu)

# --- १. गृहपृष्ठ (Home) ---
if choice == "🏠 गृहपृष्ठ":
    st.title("📚 जनसेवा युथ क्लब (JYC) डिजिटल पोर्टल")
    st.subheader("मिर्चैया नगरपालिका-८, सिराहा | स्थापना: २०७९ BS")
    try:
        st.image("307286262_1066058600717181_5062110872657776485_n.jpg", use_container_width=True)
    except:
        st.write("*(फोटो लोड हुन सकेन)*")
    
    st.write("### मुख्य सुविधाहरू:")
    col1, col2 = st.columns(2)
    with col1:
        st.info("✅ **डिजिटल पुस्तकालय:** वडाका विद्यार्थीहरूका लागि अनलाइन पुस्तक खोज्ने र पढ्ने सुविधा।")
    with col2:
        st.success("✅ **विकास ड्यासबोर्ड:** वडाका योजना र बजेटको पारदर्शी विवरण।")

# --- २. डिजिटल पुस्तकालय (Library) ---
elif choice == "📖 डिजिटल पुस्तकालय":
    st.title("📖 डिजिटल पुस्तकालय व्यवस्थापन")
    try:
        # ttl=0 ले सधैं ताजा डाटा तान्छ (Cache बस्दैन)
        df_lib = conn.read(spreadsheet=LIBRARY_SHEET_URL, ttl=0)
        
        # खाली भएका लाइनहरू हटाउने
        df_lib = df_lib.dropna(subset=['Title'])

        col1, col2, col3 = st.columns(3)
        col1.metric("कुल पुस्तक", len(df_lib))
        
        # 'Status' कोलम चेक गर्ने
        if 'Status' in df_lib.columns:
            available = len(df_lib[df_lib['Status'].str.contains('Available', case=False, na=False)])
            col2.metric("उपलब्ध", available)
        else:
            col2.metric("उपलब्ध", "N/A")
            
        col3.metric("स्थान", "मिर्चैया-८")

        search = st.text_input("किताब वा लेखकको नामबाट खोज्नुहोस्")
        if search:
            res = df_lib[df_lib['Title'].str.contains(search, case=False, na=False) | 
                         df_lib['Author'].str.contains(search, case=False, na=False)]
            st.dataframe(res, use_container_width=True)
        else:
            st.dataframe(df_lib, use_container_width=True)
    except Exception as e:
        st.warning("पुस्तकालयको डाटाबेस लोड हुन सकेन।")
        st.error(f"Error Details: {e}")

# (बाँकी कोड Ward Dashboard र About JYC उस्तै रहनेछ...)
