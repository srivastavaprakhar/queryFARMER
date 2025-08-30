import os
import sys
import logging
import contextlib
import requests
from llama_index.core.settings import Settings
from config import MODEL_PATH, DB_PATH, INDEX_PATH
from auth.user_auth import init_user_table, signup, login
from models.Mistral.mistral_engine import MistralEngine
from embed_and_index import build_index

# ========== Logging Setup ==========
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/system.log",
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# ========== Suppress LLM Output ==========
@contextlib.contextmanager
def suppress_output(to_logfile=True):
    if to_logfile:
        f = open("logs/llama.log", "a")
    else:
        f = open(os.devnull, 'w')
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = f, f
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr
        f.close()

with suppress_output():
    Settings.llm = None  # Disable OpenAI default

logger.info("LLM is explicitly disabled.")

# ========== Helper: Notify API ==========
def notify_api(endpoint: str, data: dict):
    try:
        response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=data)
        if response.status_code == 200:
            logger.info(f"Synced to API {endpoint}: {response.json()}")
        else:
            logger.warning(f"API {endpoint} failed: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Could not connect to API server for {endpoint}: {e}")

# ========== Core Logic ==========
def answer_question(index, question: str, model) -> str:
    with suppress_output():
        query_engine = index.as_query_engine(similarity_top_k=4, similarity_cutoff=0.6)
        response_obj = query_engine.query(question)

    with open("logs/retrieval_debug.log", "a", encoding="utf-8") as f:
        f.write(f"\n--- Query: {question} ---\n")
        for i, node in enumerate(response_obj.source_nodes):
            score = f"{node.score:.3f}" if node.score is not None else "N/A"
            f.write(f"[{i+1}] Score: {score}\n")
            f.write(node.node.text[:500].strip() + "\n---\n")
            
    table_counts = {}
    for node in response_obj.source_nodes:
        table = node.node.metadata.get("table", "unknown")
        table_counts[table] = table_counts.get(table, 0) + 1

    most_relevant_table = max(table_counts, key=table_counts.get)
    logger.info(f"[🔍] Most relevant table inferred: {most_relevant_table}")        

    filtered_nodes = [
        node for node in response_obj.source_nodes
        if node.score is not None and node.score >= 0.5
    ]

    if not filtered_nodes and response_obj.source_nodes:
        print("[⚠️] Fallback: Using top 3 chunks below cutoff")
        filtered_nodes = response_obj.source_nodes[:3]

    if not filtered_nodes:
        print("[❌] No chunks retrieved. Returning fallback message.")
        return "Sorry, I don't have that information."

    context = "\n\n".join(node.node.text for node in filtered_nodes).strip()

    prompt = f"""You are QueryFARMER, a chatbot for farmers.  
Always answer in **plain English** with short, practical advice.  
Never output SQL, code, or database queries.  
Only use the provided factual context.  

### Student's Question:
{question}

### Factual Context:
{context}

### Answer:
"""

    with suppress_output():
        try:
            response = model.generate(prompt).strip()
        except Exception as e:
            return f"Error generating response: {e}"

    if not response or response.lower() in ["", "answer:", "context:", "question:"]:
        return "Sorry, I could not generate a response."

    if "sorry" in response.lower() and "don't have that" in response.lower():
        return "Sorry, I don't have that information."
    
    # Optional post-filter for SQL-like output
    if "select" in response.lower() or "from" in response.lower():
        return "Sorry, I only return plain English answers."

    return response

def safe_llm_init():
    with suppress_output():
        model = MistralEngine(model_path=MODEL_PATH)
    logger.info("MistralEngine initialized.")
    return model

# ========== Main CLI ==========
def main():
    os.makedirs("database", exist_ok=True)
    init_user_table()

    print("=== CLI Chat Assistant ===")

    while True:
        choice = input("1. Login\n2. Signup\nChoose (1/2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid input. Please enter only 1 or 2.")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if choice == '1':
        if login(username, password):
            print(f"\n✅ Welcome, {username}!")
            logger.info(f"User '{username}' logged in.")
            notify_api("/login", {"username": username, "password": password})
        else:
            print("❌ Login failed.")
            logger.warning(f"Login failed for user '{username}'.")
            return

    elif choice == '2':
        if signup(username, password):
            print("✅ Signup successful. Please restart to login.")
            logger.info(f"User '{username}' signed up.")
            notify_api("/signup", {"username": username, "password": password})
            return
        else:
            print("❌ Username already exists.")
            logger.warning(f"Signup failed: username '{username}' exists.")
            return

    # Proceed with chat
    if not os.path.exists(MODEL_PATH):
        print("❌ Model file missing.")
        logger.error(f"Model not found at: {MODEL_PATH}")
        return

    print("⏳ Loading model...")
    model = safe_llm_init()

    logger.info("Building RAG index...")
    with suppress_output():
        index = build_index(db_path=DB_PATH, persist_path=INDEX_PATH)

    print("\nYou can start chatting! (type 'exit' to quit)\n")

    while True:
        user_query = input("You: ").strip()
        if user_query.lower() in ['exit', 'quit']:
            print("Bot: Goodbye! 👋")
            break

        logger.info(f"User query: {user_query}")
        print("Bot: ", end="", flush=True)

        try:
            response = answer_question(index, user_query, model)
            print(response)
            logger.info(f"Bot response: {response}")
            notify_api("/ask", {"question": user_query})
        except Exception as e:
            print("Sorry, something went wrong.")
            logger.exception("Error during response generation")

if __name__ == "__main__":
    main()
