import streamlit as st

link = 'https://www.github.com'
link2 = 'https://www.github.com'
text = 'hi'
d = [link,link2]
for i in d:
    st.markdown(f'1 | [hi there]({i})')

table1 = f"""
| Syntax | Description |\n| - | -|\n| Header | Title |\n| Paragraph | [hi there]({i}) |
"""
table2 = table1+'| 1 | 1 |'
print(table2)
#st.write(table2)
st.markdown(table2)
