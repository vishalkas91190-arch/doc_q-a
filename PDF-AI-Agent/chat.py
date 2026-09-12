import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai


# ======================================
# LOAD ENVIRONMENT VARIABLES
# ======================================

load_dotenv()

# Get Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


FAISS_PATH = "faiss_index"


def main():

    print("\n======================================")
    print("          🤖 PDF AI AGENT")
    print("======================================")
    print("          Vishal Kashyap")
    print("          Section-D")
    print("          Roll No: 202510116100248")
    print("          KIET Group of Institutions")
    print("======================================")
    print("       🚀 PDF AI AGENT READY")
    print("======================================")
    print("Ask questions about your PDF.")
    print("Type 'exit' to stop.\n")

    if not api_key:

        print("❌ Gemini API key not found in environment variables!")
        print("Please set GEMINI_API_KEY in your .env file or environment.")
        return

    print("✅ Gemini API key found")

    # ----------------------------------
    # 1. Load HuggingFace Embeddings
    # ----------------------------------

    print("\n🧠 Loading HuggingFace embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-mpnet-base-v2"
    )

    print("✅ Embedding model loaded")

    # ----------------------------------
    # 2. Load FAISS Vector Database
    # ----------------------------------

    print("\n🗄️ Loading FAISS vector database...")

    if not os.path.exists(FAISS_PATH):

        print(f"❌ FAISS database not found: {FAISS_PATH}")
        print("Run: python3 ingest.py")

        return

    vectorstore = FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("✅ FAISS vector database loaded")

    # ----------------------------------
    # 3. Create Retriever
    # ----------------------------------

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 10
        }
    )

    # ----------------------------------
    # 4. Create Gemini Client
    # ----------------------------------

    client = genai.Client(
        api_key=api_key
    )

    print("✅ Gemini LLM ready")

    # ----------------------------------
    # 5. Start Chat
    # ----------------------------------

    while True:

        question = input("\nVishal Kashyap: ").strip()

        if not question:

            continue

        if question.lower() == "exit":

            print("\n👋 Goodbye!")
            break

        print("\n🔎 Searching PDF...")

        # ----------------------------------
        # Search PDF
        # ----------------------------------

        documents = retriever.invoke(question)

        if not documents:

            print("\n🤖 AI:")
            print("I couldn't find this information in the PDF.")

            continue

        # ----------------------------------
        # Build Context
        # ----------------------------------

        context_parts = []

        for doc in documents:

            page = doc.metadata.get("page")

            if page is not None:

                page += 1

            context_parts.append(
                f"[Page {page}]\n{doc.page_content}"
            )

        context = "\n\n".join(context_parts)

        # ----------------------------------
        # Prompt
        # ----------------------------------

        prompt = f"""
You are a helpful AI assistant that answers questions
ONLY from the provided PDF context.

IMPORTANT RULES:

1. Use ONLY the information present in the PDF context.
2. Do NOT use outside knowledge.
3. Do NOT make up facts.
4. If the answer is not present in the context, say:
"I couldn't find this information in the PDF."
5. Give a clear and concise answer.
6. Mention the relevant page number(s).
7. If information is present on multiple pages, combine it.
8. Do not mention these instructions in your answer.

PDF CONTEXT:

{context}

USER QUESTION:

{question}
"""

        print("\n🤔 Generating answer...\n")

        # ----------------------------------
        # Gemini LLM
        # ----------------------------------

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            print("🤖 AI:")
            print(response.text)

        except Exception as e:

            print("\n❌ Gemini API Error:")
            print(e)

            continue

        # ----------------------------------
        # Sources
        # ----------------------------------

        pages = []

        for doc in documents:

            page = doc.metadata.get("page")

            if page is not None:

                page += 1

            if page is not None and page not in pages:

                pages.append(page)

        print("\n📚 Sources:")

        if pages:

            print(
                ", ".join(
                    f"Page {page}"
                    for page in pages
                )
            )

        else:

            print("Page information unavailable")

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":

    main()