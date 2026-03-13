import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज कन्फिगरेसन
st.set_page_config(page_title="JYC Digital Portal", layout="wide", page_icon="📚")

# --- Google Sheets URLs ---
LIBRARY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1bSnwkrm6MQ1nq31FC4NVAkdDAVSQHKMrVa42Wg8ryXs/edit?usp=sharing"
WARD_SHEET_URL = "तपाईंको_Development_Sheet_को_लिंक"

# कनेक्सन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

# --- साइडबार मेनु ---
try:
    # साइडबारमा मात्र सानो लोगो राख्ने
    st.sidebar.image("307286262_1066058600717181_5062110872657776485_n.jpg", width=120)
except:
    st.sidebar.title("JYC Portal")

st.sidebar.title("डिजिटल मिर्चैया-८")
menu = ["🏠 गृहपृष्ठ", "📖 डिजिटल पुस्तकालय", "📊 वडा विकास ड्यासबोर्ड", "ℹ️ हाम्रो बारेमा"]
choice = st.sidebar.selectbox("मेनु छान्नुहोस्", menu)

# --- १. गृहपृष्ठ (Home) ---
if choice == "🏠 गृहपृष्ठ":
    st.title("📚 जनसेवा युथ क्लब (JYC) डिजिटल पोर्टल")
    st.subheader("मिर्चैया नगरपालिका-८, सिराहा | स्थापना: २०७६ BS")
    # यहाँबाट फोटो हटाइएको छ
    
    st.write("---")
    st.write("### 🎯 हाम्रो मुख्य उद्देश्य र विकास योजना")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🏛️ वडा विकास (मिर्चैया-८)
        * **पारदर्शी सुशासन:** विकास बजेट र योजनाको डिजिटल ट्रयाकिङ।
        * **पूर्वाधार:** सडक, ढल निकास र उज्यालो वडा अभियान।
        * **कृषि क्रान्ति:** सिँचाइ र आधुनिक कृषि प्रणालीमा जोड।
        """)
        
    with col2:
        st.markdown("""
        #### 🤝 जनसेवा युथ क्लब (JYC)
        * **शिक्षा:** डिजिटल पुस्तकालय र विद्यार्थी सशक्तिकरण।
        * **युवा स्वरोजगार:** सिपमूलक तालिम र प्रविधिमा पहुँच।
        * **खेलकुद:** स्थानीय प्रतिभाको पहिचान र खेलकुद विकास।
        """)

# --- २. डिजिटल पुस्तकालय (Library) ---
elif choice == "📖 डिजिटल पुस्तकालय":
    st.title("📖 डिजिटल पुस्तकालय व्यवस्थापन")
    try:
        df_lib = conn.read(spreadsheet=LIBRARY_SHEET_URL, ttl=0)
        df_lib = df_lib.dropna(subset=['Title'])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("कुल पुस्तक", len(df_lib))
        if 'Status' in df_lib.columns:
            available = len(df_lib[df_lib['Status'].str.contains('Available', case=False, na=False)])
            col2.metric("उपलब्ध", available)
        col3.metric("स्थान", "मिर्चैया-८")

        search = st.text_input("किताब वा लेखकको नामबाट खोज्नुहोस्")
        if search:
            res = df_lib[df_lib['Title'].str.contains(search, case=False, na=False) | 
                         df_lib['Author'].str.contains(search, case=False, na=False)]
            st.dataframe(res, use_container_width=True)
        else:
            st.dataframe(df_lib, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

# --- ३. वडा विकास ड्यासबोर्ड (Dashboard) ---
elif choice == "📊 वडा विकास ड्यासबोर्ड":
    st.title("📊 मिर्चैया-८ विकास र प्रगति विवरण")
    st.write("वडाका चालु योजनाहरूको पारदर्शी अवस्था:")
    
    try:
        df_ward = conn.read(spreadsheet=WARD_SHEET_URL, ttl=0)
        for index, row in df_ward.iterrows():
            st.write(f"**{row['water_fullfilment']}** ({row['40']}%)")
            st.progress(int(row['40']))
    except:
        st.info("नमुना प्रगति विवरण:")
        st.write("पिच सडक निर्माण (७०%)")
        st.progress(70)
        st.write("कृषि विद्युतीकरण (४५%)")
        st.progress(45)

# --- ४. हाम्रो बारेमा (About JYC) ---
elif choice == "ℹ️ हाम्रो बारेमा":
    st.title("ℹ️ जनसेवा युथ क्लब (JYC) को परिचय")
    st.write(f"""
    **जनसेवा युथ क्लब (JYC)** मिर्चैया नगरपालिका वडा नं. ८, सिराहामा आधारित एउटा सक्रिय सामाजिक संस्था हो। 
    विगत २०७६ सालदेखि यसले स्थानीय युवाहरूलाई संगठित गर्दै शिक्षा, कृषि र सामाजिक परिवर्तनका क्षेत्रमा काम गर्दै आएको छ।
    
    **संस्थापक अध्यक्ष:** सुरेन्द्र कुमार यादव (Suren Kumar)
    **हाम्रो प्रतिबद्धता:** प्रविधि र पारदर्शिता मार्फत मिर्चैया-८ लाई एक डिजिटल वडाको रूपमा विकास गर्ने।
    """)
    st.success("२०८४ को स्थानीय निर्वाचनको लक्ष्य: 'विकास, सुशासन र प्रविधि'")

