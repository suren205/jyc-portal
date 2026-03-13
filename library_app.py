import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# पेज कन्फिगरेसन
st.set_page_config(page_title="JYC Digital Portal", layout="wide", page_icon="📚")

# --- Google Sheets URLs (आफ्नो वास्तविक लिंक यहाँ हाल्नुहोस्) ---
LIBRARY_SHEET_URL = "https://docs.google.com/spreadsheets/d/1bSnwkrm6MQ1nq31FC4NVAkdDAVSQHKMrVa42Wg8ryXs/edit?usp=sharing"
WARD_SHEET_URL = "तपाईंको_Development_Sheet_को_लिंक"

# कनेक्सन सेटअप
conn = st.connection("gsheets", type=GSheetsConnection)

# --- साइडबार मेनु ---
st.sidebar.image("307286262_1066058600717181_5062110872657776485_n.jpg") # क्लबको लोगो भए यहाँ राख्नुहोला
st.sidebar.title("डिजिटल मिर्चैया-८")
menu = ["🏠 गृहपृष्ठ", "📖 डिजिटल पुस्तकालय", "📊 वडा विकास ड्यासबोर्ड", "ℹ️ हाम्रो बारेमा"]
choice = st.sidebar.selectbox("मेनु छान्नुहोस्", menu)

# --- १. गृहपृष्ठ (Home) ---
if choice == "🏠 गृहपृष्ठ":
    st.title("📚 जनसेवा युथ क्लब (JYC) डिजिटल पोर्टल")
    st.subheader("मिर्चैया नगरपालिका-८, सिराहा | स्थापना: २०७९ BS")
    st.image("307286262_1066058600717181_5062110872657776485_n.jpg")
    
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
        df_lib = conn.read(spreadsheet=LIBRARY_SHEET_URL)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("कुल पुस्तक", len(df_lib))
        col2.metric("उपलब्ध", len(df_lib[df_lib['Status'] == "Available"]))
        col3.metric("स्थान", "मिर्चैया-८")

        search = st.text_input("किताब वा लेखकको नामबाट खोज्नुहोस्")
        if search:
            res = df_lib[df_lib['Title'].str.contains(search, case=False, na=False) | 
                         df_lib['Author'].str.contains(search, case=False, na=False)]
            st.dataframe(res, use_container_width=True)
        else:
            st.dataframe(df_lib, use_container_width=True)
    except:
        st.warning("पुस्तकालयको डाटाबेस लोड हुन सकेन। कृपया Google Sheet लिंक चेक गर्नुहोस्।")

# --- ३. वडा विकास ड्यासबोर्ड (Ward Dashboard) ---
elif choice == "📊 वडा विकास ड्यासबोर्ड":
    st.title("📊 वडा विकास र सुशासन ड्यासबोर्ड")
    st.write("वडाका योजनाहरूको वास्तविक अवस्था:")

    try:
        df_ward = conn.read(spreadsheet=WARD_SHEET_URL)
        
        # प्रगति बारहरू (Progress Bars)
        st.write("### योजनाहरूको प्रगति विवरण")
        for index, row in df_ward.iterrows():
            st.write(f"**{row['Project_Name']}** ({row['Progress_Percent']}%)")
            st.progress(int(row['Progress_Percent']))
        
        # बजेट विश्लेषण (Budget Chart)
        st.write("---")
        st.write("### बजेट विनियोजन विवरण")
        st.bar_chart(data=df_ward, x='Project_Name', y='Budget')
        
    except:
        # यदि सिट कनेक्ट छैन भने नमुना डाटा
        st.write("*(सिट जोडिएको छैन, त्यसैले नमुना डाटा देखाइएको छ)*")
        sample_data = pd.DataFrame({
            'Project_Name': ['सडक पिच', 'स्वास्थ्य केन्द्र', 'कृषि सिँचाइ'],
            'Progress_Percent': [80, 45, 95],
            'Budget': [1500000, 500000, 1200000]
        })
        for i, r in sample_data.iterrows():
            st.write(f"{r['Project_Name']} ({r['Progress_Percent']}%)")
            st.progress(r['Progress_Percent'])
        st.bar_chart(data=sample_data, x='Project_Name', y='Budget')

# --- ४. हाम्रो बारेमा (About) ---
elif choice == "ℹ️ हाम्रो बारेमा":
    st.title("ℹ️ जनसेवा युथ क्लब (JYC) को बारेमा")
    st.write(f"""
    * **स्थापना:** २०७९ BS
    * **संस्थापक अध्यक्ष:** सुरेन्द्र कुमार यादव (Suren Kumar)
    * **उद्देश्य:** मिर्चैया-८ को विकास र युवाहरूलाई प्रविधिसँग जोड्ने।
    
    हामी आगामी २०८४ को स्थानीय निर्वाचनमा वडा नं. ८ लाई 'डिजिटल र पारदर्शी वडा' बनाउने लक्ष्यका साथ अगाडि बढिरहेका छौं।

    """)
