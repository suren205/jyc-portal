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
# --- ३. वडा विकास ड्यासबोर्ड (Ward Dashboard) ---
elif choice == "📊 वडा विकास ड्यासबोर्ड":
    st.title("📊 मिर्चैया-८ विकास र सुशासन ड्यासबोर्ड")
    st.info("यो ड्यासबोर्डले वडामा भइरहेका विकास निर्माणका कामहरूको पारदर्शी विवरण देखाउँछ।")

    # वडा विकासका मुख्य बुँदाहरू
    st.subheader("🚀 हाम्रो विकास प्राथमिकताहरू")
    development_goals = {
        "शिक्षा": "वडाका हरेक बालबालिकाको गुणस्तरीय शिक्षामा पहुँच र डिजिटल साक्षरता।",
        "कृषि": "स्मार्ट कृषि प्रणाली, सिँचाइ सुविधा र किसानहरूका लागि बजार व्यवस्थापन।",
        "स्वास्थ्य": "सुलभ स्वास्थ्य सेवा र गाउँघर क्लिनिकको सुदृढीकरण।",
        "पूर्वाधार": "स्तरीय सडक सञ्जाल, ढल निकास र उज्यालो वडा अभियान।"
    }
    
    cols = st.columns(2)
    for i, (goal, desc) in enumerate(development_goals.items()):
        cols[i % 2].write(f"**🔹 {goal}:** {desc}")

    # प्रगति विवरण (यदि Sheet जोडिएको छैन भने यो नमुना देखिनेछ)
    st.write("---")
    st.subheader("🏗️ चालु योजनाहरूको प्रगति")
    try:
        df_ward = conn.read(spreadsheet=WARD_SHEET_URL, ttl=0)
        for index, row in df_ward.iterrows():
            st.write(f"**{row['water_fullfilment']}** ({row['40']}%)")
            st.progress(int(row['40']))
    except:
        # नमुना डाटा
        st.write("*पिच सडक निर्माण - वडा नं. ८ (७५%)*")
        st.progress(75)
        st.write("*कृषि सिँचाइ विस्तार (४०%)*")
        st.progress(40)

# --- ४. हाम्रो बारेमा (About JYC) ---
elif choice == "ℹ️ हाम्रो बारेमा":
    st.title("ℹ️ जनसेवा युथ क्लब (JYC) र नेतृत्व")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # यहाँ तपाईंको फोटो वा क्लबको लोगो राख्न सकिन्छ
        try:
            st.image("307286262_1066058600717181_5062110872657776485_n.jpg", width=200)
        except:
            st.write("📷 **JYC Logo**")

    with col2:
        st.subheader("संस्थाको परिचय")
        st.write(f"""
        **जनसेवा युथ क्लब (JYC)** मिर्चैया नगरपालिका वडा नं. ८ मा आधारित एक अग्रणी युवा संस्था हो। 
        २०७९ सालमा स्थापना भएको यस क्लबले समाज परिवर्तन र युवा सशक्तिकरणका लागि निरन्तर काम गर्दै आएको छ।
        
        **संस्थापक अध्यक्ष:** सुरेन्द्र कुमार यादव (Suren Kumar)
        **स्थापना:** २०७९ BS
        **स्थान:** मिर्चैया-८, सिराहा, मधेश प्रदेश
        """)

    st.write("---")
    st.subheader("🎯 हाम्रो मुख्य उद्देश्यहरू")
    objectives = [
        "मिर्चैया-८ का युवाहरूलाई सिपमूलक तालिम र प्रविधिसँग जोड्ने।",
        "वडामा डिजिटल पुस्तकालय र ई-लर्निङ सेन्टर स्थापना गरी शिक्षामा सुधार ल्याउने।",
        "स्थानीय विकासका कामहरूमा पारदर्शिता र जनसहभागिता सुनिश्चित गर्ने।",
        "खेलाडीहरूको प्रतिभा पहिचान र खेलकुद विकासमा लगानी गर्ने।",
        "२०८४ को स्थानीय निर्वाचन मार्फत मिर्चैया-८ लाई एक 'नमुना डिजिटल वडा' बनाउने।"
    ]
    
    for obj in objectives:
        st.write(f"✅ {obj}")

    st.success("🤝 हामीसँग जोडिएर मिर्चैया-८ को विकासमा सहकार्य गर्न सबै युवाहरूलाई हार्दिक निमन्त्रणा गर्दछौं।")

