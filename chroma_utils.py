from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List
import os

# === PDF to URL Map ===

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


pdf_url_map = {
    "TIP-Report-2024_Introduction_V10_508-accessible_2.13.2025.pdf":
        "https://www.state.gov/reports/2024-trafficking-in-persons-report",
    "Polaris-Analysis-of-2021-Data-from-the-National-Human-Trafficking-Hotline.pdf":
        "https://polarisproject.org/wp-content/uploads/2020/07/Polaris-Analysis-of-2021-Data-from-the-National-Human-Trafficking-Hotline.pdf",
    "In-Harms-Way-How-Systems-Fail-Human-Trafficking-Survivors-by-Polaris-modifed-June-2023.pdf":
        "https://polarisproject.org/resources/in-harms-way-how-systems-fail-human-trafficking-survivors/",
    "Hotline-Trends-Report-2023.pdf":
        "https://polarisproject.org/wp-content/uploads/2020/07/Hotline-Trends-Report-2023.pdf",
    "GLOTIP2024_Chapter_1.pdf":
        "https://www.unodc.org/unodc/en/data-and-analysis/glotip.html",
    "GLOTIP2024_Chapter_2.pdf":
        "https://www.unodc.org/unodc/en/data-and-analysis/glotip.html",
    "GLOTIP2024_Chapter_3.pdf":
        "https://www.unodc.org/unodc/en/data-and-analysis/glotip.html",
    "Polaris-Typology-of-Modern-Slavery-1.pdf":
        "https://polarisproject.org/wp-content/uploads/2019/09/Polaris-Typology-of-Modern-Slavery-1.pdf",
    "Parent Resource Guide_FINAL_update 2021.pdf":
        "https://ctip.defense.gov/Portals/12/Parent%20Resource%20Guide_FINAL_update%202025.pdf",
    "RESOURCE-GUIDE-ONLINE-SAFETY-GROOMING-&-SEXTORTION.pdf":
        "https://www.eyesupappalachia.org/_files/ugd/14b638_bf90969f778f42318734e03df56bd448.pdf",
    "HUMAN TRAFFICKING RESPONSE GUIDE for School Resource Officers.pdf":
        "https://www.dhs.gov/sites/default/files/2024-06/240624_bc_human_trafficking_response_guide_school_resource_officers.pdf",
    "HUMAN TRAFFICKING AWARENESS GUIDE for Convenience Retail Employees.pdf":
        "https://www.dhs.gov/sites/default/files/2024-06/240624_bc_convenience_store_guide.pdf",
    "HOW TO TALK TO YOUTH ABOUT HUMAN TRAFFICKING A Guide for Youth Caretakers and Individuals Working with Youth.pdf":
        "https://www.dhs.gov/sites/default/files/publications/blue_campaign_youth_guide_508_1.pdf",
    "FIU-Peer-to-Peer-Platforms-Case-Study.pdf":
        "https://polarisproject.org/wp-content/uploads/2024/05/FIU-Peer-to-Peer-Platforms-Case-Study.pdf",
    "Combating Child Sex Trafficking a Guide for Law Enforcement.pdf":
        "https://www.theiacp.org/sites/default/files/IACPCOPSCombatingChildSexTraffickingAGuideforLELeaders.pdf",
    "CaseStudies-voi.pdf":
        "https://sharedhope.org/wp-content/uploads/2020/10/CaseStudies-voi.pdf",
    "2023-Federal-Human-Trafficking-Report-WEB-Spreads-LR.pdf":
        "https://traffickinginstitute.org/wp-content/uploads/2024/06/2023-Federal-Human-Trafficking-Report-WEB-Spreads-LR.pdf",
    "2017_April_AZ_SexTraffickingResearch.pdf":
        "https://ag.nv.gov/uploadedFiles/agnvgov/Content/Human_Trafficking/2017_April_AZ_SexTraffickingResearch.pdf"
}

# === Setup ===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

embedding_function = OpenAIEmbeddings()

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

# === Load and Split ===
def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    documents = loader.load()
    splits = text_splitter.split_documents(documents)
    return splits

# === Index Single Document ===
def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        filename = os.path.basename(file_path)
        source_url = pdf_url_map.get(filename, "Unknown Source")
        
        for idx,doc in enumerate(splits):
            doc.metadata["file_id"] = file_id
            doc.metadata["file_name"] = filename
            doc.metadata["source"] = source_url
            # 👇 Print small preview of each doc chunk:
            print(f"\n📝 Chunk {idx+1}:")
            print(f"Content Preview: {doc.page_content[:200]}...")  # First 200 characters
            print(f"Metadata: {doc.metadata}")

        
        vectorstore.add_documents(splits)
 
        
        return True
    except Exception as e:
        print(f"Error indexing {file_path}: {e}")
        return False

# === Index All PDFs ===
def index_all_pdfs_in_directory(directory_path: str):
    file_id = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            success = index_document_to_chroma(file_path, file_id)
            if success:
                print(f"✅ Indexed {filename} with file_id={file_id}")
                file_id += 1
            else:
                print(f"❌ Failed to index {filename}")



# === Main ===
if __name__ == "__main__":
    directory_path = "./knowledgebase"  # Your PDF folder
    print(f"📂 Indexing all PDFs inside {directory_path}...\n")
    index_all_pdfs_in_directory(directory_path)
    print("\n✅ All PDF documents processed.")
