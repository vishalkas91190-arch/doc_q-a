import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Load environment variables
load_dotenv()

PDF_PATH = "pdfs/Placement Policy 2027_B.Tech_MCA.pdf"
FAISS_PATH = "faiss_index"


def main():

    print("\n======================================")
    print("       📄 PDF AI AGENT - INGEST")
    print("======================================")

    # ----------------------------------
    # 1. Check PDF
    # ----------------------------------

    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF not found: {PDF_PATH}")
        return

    print(f"📖 Loading PDF: {PDF_PATH}")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("✅ PDF loaded successfully")
    print(f"📄 Total pages: {len(documents)}")

    # ----------------------------------
    # 2. Split PDF
    # ----------------------------------

    print("\n✂️ Splitting PDF into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    text_chunks = splitter.split_documents(documents)

    print(f"✅ Total chunks created: {len(text_chunks)}")

    # ----------------------------------
    # 3. HuggingFace Embeddings
    # ----------------------------------

    print("\n🧠 Loading HuggingFace embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-mpnet-base-v2"
    )

    print("✅ Embedding model loaded")

    # ----------------------------------
    # 4. Create FAISS Vector Store
    # ----------------------------------

    print("\n💾 Creating FAISS vector database...")

    vectorstore = FAISS.from_documents(
        text_chunks,
        embeddings
    )

    vectorstore.save_local(FAISS_PATH)

    print("\n======================================")
    print("       🎉 INGESTION COMPLETE")
    print("======================================")
    print(f"📄 Pages  : {len(documents)}")
    print(f"🧩 Chunks : {len(text_chunks)}")
    print(f"🗄️ FAISS  : {FAISS_PATH}")
    print("======================================\n")


if __name__ == "__main__":
    main()