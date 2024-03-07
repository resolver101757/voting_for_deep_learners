import streamlit as st
import validators

# Pre-populated list of links
default_links = [
    {'url': 'https://example.com', 'comment': 'This is an example link.', 'votes': 5},
    {'url': 'https://openai.com', 'comment': 'Check out OpenAI!', 'votes': 3},
    {'url': 'https://streamlit.io', 'comment': 'Streamlit is awesome for building ML apps.', 'votes': 4},
]

# Initialize session state for storing links if it doesn't exist
if 'links' not in st.session_state:
    st.session_state['links'] = default_links.copy()  # Use a copy to avoid modifying the original list

st.title('Link Sharing App')

with st.form(key='link_form'):
    link_url = st.text_input('Link URL', help='Enter the URL of the link you want to share.')
    link_comment = st.text_area('Comment', help='Add a comment for your link.')
    submit_link = st.form_submit_button('Add Link')

if submit_link and link_url:
    if validators.url(link_url):
        existing_links = [link['url'] for link in st.session_state.links]
        if link_url not in existing_links:
            st.session_state.links.append({
                'url': link_url,
                'comment': link_comment,
                'votes': 0,
            })
        else:
            st.error('This link already exists.')
    else:
        st.error('The URL you entered is not valid. Please enter a valid URL.')

# Sort the links by votes in descending order before displaying them
sorted_links = sorted(st.session_state.links, key=lambda x: x['votes'], reverse=True)

# Display the links and their comments using a more structured layout
links_container = st.container()

for i, link in enumerate(sorted_links):
    with links_container.expander(f"Link #{i+1}: {link['url']} ({link['votes']} votes)", expanded=True):
        # Using markdown for a richer presentation of the URL and comment
        st.markdown(f"**URL**: [Visit Link]({link['url']})\n\n**Comment**: {link['comment']}")
        
        # Upvote button aligned to the right for a cleaner look
        if st.button('👍 Upvote', key=f'vote_{i}'):
            # Increase the vote for the original list to maintain consistency
            original_index = st.session_state.links.index(link)
            st.session_state.links[original_index]['votes'] += 1
            st.experimental_rerun()

st.write('End of Links')
