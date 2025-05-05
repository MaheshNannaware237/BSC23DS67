import streamlit as st
import hashlib
import time

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = []

# Function to create a new block
def create_block(index, data, previous_hash):
    block = {
        "index": index,
        "data": data,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "previous_hash": previous_hash
    }
    return block

# Function to generate SHA-256 hash of a block
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Create Genesis block
def create_genesis_block():
    genesis_data = {
        "passenger": "Genesis",
        "route": "None",
        "fare": 0
    }
    genesis_block = create_block(0, genesis_data, "0")
    st.session_state.blockchain.append(genesis_block)

# Add a new ticket block
def add_ticket(passenger, route, fare):
    previous_block = st.session_state.blockchain[-1]
    new_index = previous_block["index"] + 1
    new_hash = generate_hash(previous_block)

    ticket_data = {
        "passenger": passenger,
        "route": route,
        "fare": fare
    }

    new_block = create_block(new_index, ticket_data, new_hash)
    st.session_state.blockchain.append(new_block)

# ---------- Streamlit App UI ----------

st.title("🚌 Bus Ticket Blockchain Ledger")

# Create Genesis block only once
if len(st.session_state.blockchain) == 0:
    create_genesis_block()

# Ticket form
st.subheader("➕ Add New Ticket")
with st.form("ticket_form"):
    passenger = st.text_input("Passenger Name")
    route = st.text_input("Route (e.g., A to B)")
    fare = st.number_input("Fare", min_value=0)
    submit = st.form_submit_button("Add Ticket")

    if submit:
        if passenger and route and fare > 0:
            add_ticket(passenger, route, fare)
            st.success("✅ Ticket added to the blockchain!")
        else:
            st.error("Please fill all fields correctly.")

# Display Blockchain
st.subheader("📜 Blockchain Ledger")

for block in st.session_state.blockchain:
    with st.expander(f"Block #{block['index']}"):
        st.write("**Passenger:**", block["data"]["passenger"])
        st.write("**Route:**", block["data"]["route"])
        st.write("**Fare:** ₹", block["data"]["fare"])
        st.write("**Timestamp:**", block["timestamp"])
        st.code(block["previous_hash"], language="text")
