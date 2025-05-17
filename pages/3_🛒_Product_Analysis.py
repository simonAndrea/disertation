import streamlit as st, pandas as pd, re

st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Using CSS file
with open('main_style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":shopping_trolley: Market Basket Analysis")

def expandable_html_viewer(session_key: str, button_text: str, file_path: str):
    if session_key not in st.session_state:
        st.session_state[session_key] = False

    expander_container = st.container()

    with expander_container:
        arrow = ":arrow_down_small:" if not st.session_state[session_key] else ":arrow_up_small:"

        if st.button(f"{arrow} {button_text} "):
            st.session_state[session_key] = not st.session_state[session_key]
            st.rerun()

        if st.session_state[session_key]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_string = f.read()
                st.components.v1.html(html_string, height=700, width=1000, scrolling=True)
            except FileNotFoundError:
                st.error(f"File not found: {file_path}")


def extract_unique_products(rules_series):
    products = set()
    for rule in rules_series:
        items = rule.replace("{", "").replace("}", "").split("=>")
        for part in items:
            for item in part.split(","):
                clean_item = item.replace("_", " ").strip()
                if clean_item:
                    products.add(clean_item)
    return sorted(products)

def clean_product_string(product_str):
    return product_str.replace("{", "").replace("}", "").replace("_", " ").strip()


# Extract and clean the associated product names from RHS
def extract_lhs_products(rules_series):
    lhs_products = set()
    for rule in rules_series:
        lhs = rule.split("=>")[0]
        for item in lhs.split(","):
            clean_item = clean_product_string(item)
            if clean_item:
                lhs_products.add(clean_item)
    return sorted(lhs_products)

def extract_rhs_clean(rule):
    parts = rule.split("=>")
    rhs = parts[1] if len(parts) > 1 else ""
    return clean_product_string(rhs)

# Function to filter by LHS (Left Hand Side) based on selected product
def product_in_lhs(rule, selected_product):
    lhs = rule.split("=>")[0]  # LHS is everything before '=>'
    return selected_product in lhs  # Check if selected product is in the LHS

def product_association_explorer(csv_path: str):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"File not found: {csv_path}")
        return
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    if "rules" not in df.columns:
        st.warning("This file doesn't have a 'rules' column.")
        return

    all_lhs_products = extract_lhs_products(df['rules'])
    selected_product = st.selectbox(":mag: Search for a product: ", all_lhs_products, key=csv_path, index=None, placeholder="Enter a product")

    if selected_product:
        related_rules = df[df['rules'].apply(lambda rule: product_in_lhs(rule, selected_product))].copy()

        if len(related_rules) > 0:
            related_rules["Associated Products"] = related_rules["rules"].apply(extract_rhs_clean)
            unique_products = related_rules["Associated Products"].drop_duplicates().sort_values().reset_index(drop=True)
            unique_products_df = unique_products.to_frame(name="Associated Products")

            st.dataframe(unique_products_df, use_container_width=True, hide_index=True)


        else:
            st.write("No associated products found.")


city = st.selectbox(
        label='Select a City:',
        options=['Miercurea Ciuc', 'Odorheiu Secuiesc', 'Reghin', 'Sfantu Gheorghe', 'Targu Mures']
    )

#Miercurea Ciuc

if city == 'Miercurea Ciuc':
    with st.expander("Store: Centrum", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_11_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('centrum_expanded', 'Display Product Network For Centrum', 'D:/MESTERI/Diszertacio/disertation - Copy/mba/site11_market_basket_network.html')
    
    with st.expander("Store: Nagyret", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_12_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('nagyret_expanded', 'Display Product Network For Nagyret', 'D:/MESTERI/Diszertacio/disertation - Copy/mba/site12_market_basket_network.html')


# #Odorheiu Secuiesc
if city == 'Odorheiu Secuiesc':
    with st.expander("Store: Szuper Diszkont", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_5_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('diszkont_expanded', 'Display Product Network For Diszkont', 'D:/MESTERI/Diszertacio/disertation - Copy/mba/site5_market_basket_network.html')

    with st.expander("Store: Szuper Market", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_6_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('market_expanded', 'Display Product Network For Market', 'D:/MESTERI/Diszertacio/disertation - Copy/mba/site6_market_basket_network.html')

    with st.expander("Store: Szuper Csemege", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_7_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('csemege_expanded', 'Display Product Network For Csemege','D:/MESTERI/Diszertacio/disertation - Copy/mba/site7_market_basket_network.html')

    with st.expander("Store: Szuper Kokereszt", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_8_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('kokereszt_expanded', 'Display Product Network For Kokereszt','D:/MESTERI/Diszertacio/disertation - Copy/mba/site8_market_basket_network.html')

    with st.expander("Store: Szuper Horizont", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_9_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('horizont_expanded', 'Display Product Network For Horizont','D:/MESTERI/Diszertacio/disertation - Copy/mba/site9_market_basket_network.html')

    with st.expander("Store: Merkur Bethlen", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_14_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('bethlen_expanded', 'Display Product Network For Merkur Bethlen','D:/MESTERI/Diszertacio/disertation - Copy/mba/site14_market_basket_network.html')
        
    with st.expander("Store: Merkur Aruhaz", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_15_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('aruhaz_expanded', 'Display Product Network For Aruhaz','D:/MESTERI/Diszertacio/disertation - Copy/mba/site15_market_basket_network.html')



# #Reghin
if city == 'Reghin':
    with st.expander("Store: Merkur Reghin", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_31_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('reghin_expanded', 'Display Product Network For Merkur Reghin','D:/MESTERI/Diszertacio/disertation - Copy/mba/site31_market_basket_network.html')

# #Sfantu Gheorghe
if city == 'Sfantu Gheorghe':
    with st.expander("Store: Merkur Sfantu Gheorghe", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_10_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('merkur_sg_expanded', 'Display Product Network For Mekrur','D:/MESTERI/Diszertacio/disertation - Copy/mba/site10_market_basket_network.html')
    
    with st.expander("Store: Merkur Oltmezo", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_32_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('oltmezo_expanded', 'Display Product Network For Oltmezo','D:/MESTERI/Diszertacio/disertation - Copy/mba/site32_market_basket_network.html')
    

# #Targu Mures
if city == 'Targu Mures':
    with st.expander("Store: Merkur Tudor", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_25_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('targu_mures_expanded', 'Display Product Network For Tudor','D:/MESTERI/Diszertacio/disertation - Copy/mba/site25_market_basket_network.html')

    with st.expander("Store: Merkur Dozsa", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_26_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('dozsa_expanded', 'Display Product Network For Dozsa','D:/MESTERI/Diszertacio/disertation - Copy/mba/site26_market_basket_network.html')

    with st.expander("Store: Merkur Fantanele", expanded=False):
        product_association_explorer("D:/MESTERI/Diszertacio/disertation - Copy/products/site_33_mba.csv")
        st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)
        expandable_html_viewer('unirii_expanded', 'Display Product Network For Fantanele','D:/MESTERI/Diszertacio/disertation - Copy/mba/site33_market_basket_network.html')

