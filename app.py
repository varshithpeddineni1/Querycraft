import streamlit as st
from groq import Groq
import os
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

st.set_page_config(
    page_title="QueryCraft",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1a1a2e;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .explanation-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">⚡ QueryCraft</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Describe what you want — '
    'Get perfect SQL instantly • Powered by Groq AI</div>',
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    db_type = st.selectbox(
        "Database Type:",
        ["MySQL", "PostgreSQL",
         "SQLite", "SQL Server", "Oracle"]
    )
    
    complexity = st.select_slider(
        "Query Complexity:",
        options=["Simple", "Medium", "Advanced"],
        value="Medium"
    )
    
    st.divider()
    st.markdown("### 📚 Try These Examples")
    
    examples = [
        "Show all users who signed up last month",
        "Find top 10 best selling products",
        "Get average salary by department",
        "Find customers who never ordered",
        "Show daily sales for last 30 days",
        "Find duplicate email addresses",
        "Get employees with salary above average",
        "Show orders with customer names"
    ]
    
    for example in examples:
        if st.button(
            f"📝 {example[:35]}",
            use_container_width=True
        ):
            st.session_state.query_input = example

col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_area(
        "Describe what data you need:",
        value=st.session_state.get('query_input', ''),
        placeholder="Example: Show me all customers "
                   "who made more than 3 orders "
                   "in the last 30 days sorted "
                   "by total spending...",
        height=120
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    schema = st.text_area(
        "Your table schema (optional):",
        placeholder="users(id, name, email)\n"
                   "orders(id, user_id, amount)\n"
                   "products(id, name, price)",
        height=120
    )

generate = st.button(
    "⚡ Generate SQL Query",
    use_container_width=True,
    type="primary"
)

if generate and user_query:
    with st.spinner("🤖 Crafting your perfect query..."):
        
        schema_text = f"\nDatabase Schema:\n{schema}" \
                     if schema else ""
        
        prompt = f"""
        You are an expert SQL developer and teacher
        with 15 years of experience.
        
        Database Type: {db_type}
        Complexity Level: {complexity}
        {schema_text}
        
        User Request: {user_query}
        
        Please provide:
        
        1. The SQL query inside a ```sql code block
        
        2. A clear explanation of each part
        
        3. How it works step by step
        
        4. 2-3 optimization tips
        
        5. Common mistakes to avoid
        
        6. An alternative approach
        
        Make sure the SQL query is always 
        inside ```sql and ``` tags.
        """
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert SQL developer. Always put SQL queries inside ```sql code blocks."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            full_response = response.choices[0].message.content
            success = True
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            success = False
    
    if success:
        st.success("✅ Query Generated Successfully!")
        
        # Extract SQL from code block
        sql_match = re.search(
            r'```sql\n(.*?)```',
            full_response,
            re.DOTALL
        )
        
        if sql_match:
            sql_query = sql_match.group(1).strip()
        else:
            sql_match = re.search(
                r'```\n(.*?)```',
                full_response,
                re.DOTALL
            )
            if sql_match:
                sql_query = sql_match.group(1).strip()
            else:
                sql_query = full_response
        
        # Show SQL Query
        st.markdown("### ⚡ Your SQL Query")
        st.code(sql_query, language="sql")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download Query (.sql)",
                sql_query,
                file_name="query.sql",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.button(
                "📋 Copy to Clipboard",
                use_container_width=True
            )
        
        st.divider()
        
        # Full Analysis in tabs
        st.markdown("### 🧠 Full Analysis")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📖 Explanation",
            "🔧 How It Works",
            "🚀 Optimization",
            "⚠️ Mistakes",
            "🔄 Alternative"
        ])
        
        # Clean response without code blocks
        clean_response = re.sub(
            r'```.*?```',
            '',
            full_response,
            flags=re.DOTALL
        )
        
        # Split response into sections
        sections = clean_response.split('\n\n')
        
        # Distribute sections across tabs
        total = len(sections)
        chunk = max(1, total // 5)
        
        with tab1:
            st.markdown(
                '\n\n'.join(sections[:chunk])
            )
        with tab2:
            st.markdown(
                '\n\n'.join(
                    sections[chunk:chunk*2]
                )
            )
        with tab3:
            st.markdown(
                '\n\n'.join(
                    sections[chunk*2:chunk*3]
                )
            )
        with tab4:
            st.markdown(
                '\n\n'.join(
                    sections[chunk*3:chunk*4]
                )
            )
        with tab5:
            st.markdown(
                '\n\n'.join(sections[chunk*4:])
            )
        
        st.divider()
        
        # Query Stats
        st.markdown("### 📊 Query Stats")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🗄️ Database", db_type)
        with col2:
            st.metric("📊 Complexity", complexity)
        with col3:
            st.metric(
                "📝 Words",
                len(sql_query.split())
            )
        with col4:
            st.metric(
                "📏 Lines",
                len(sql_query.strip().split('\n'))
            )

elif generate and not user_query:
    st.error("Please describe what data you need!")

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("⚡ **QueryCraft**")
with col2:
    st.markdown("Built by **Varshith Peddineni**")
