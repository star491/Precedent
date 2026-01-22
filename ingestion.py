import json
import uuid
import logging
from typing import List
from pypdf import PdfReader
from groq import Groq
from sentence_transformers import SentenceTransformer
from backend.config import settings
from backend.models import DecisionNode
from backend.qdrant_client_wrapper import db_client
from qdrant_client.http import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Groq Client
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Configure Local Embedding Model
# This downloads the model to ~/.cache/torch/sentence_transformers on first run
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_decisions_using_llm(text: str, filename: str) -> List[DecisionNode]:
    """
    Uses Groq (Llama 3) to parse the raw text and extract structured decision data.
    """
    logger.info(f"Extracting decisions from {filename} using Groq...")
    
    prompt = f"""
    You are a Senior Technical Auditor. Your job is to extract detailed decision records.
    
    CRITICAL INSTRUCTION: THE USER WANTS EXTREME VERBOSITY.
    - DO NOT SUMMARIZE.
    - Each 'rationale' point must be a FULL PARAGRAPH (4-5 sentences).
    - Capture EVERY financial figure, date, and name.
    - If the text explains a trade-off, write down the ENTIRE explanation.
    - PREFER LONG, DETAILED SENTENCES over short ones.

    Input Text:
    {text[:100000]}

    Return a JSON list of objects with this EXACT structure:
    {{
        "decision_title": "The main decision made",
        "decision_date": "YYYY-MM-DD",
        "team": "The team responsible",
        "rationale": [
            "Detailed Point 1: (Must be 50+ words). Example: 'The team explicitly rejected Azure despite the generous $100k credit offer because the engineering team lacked familiarity with Azure Resource Manager templates. Training them would incur a 3-month learning curve, which would unacceptably delay the critical Phoenix product launch scheduled for Q3.'",
            "Detailed Point 2: (Must contain numbers). Example: 'Staying on-premise was deemed financially unviable because it required an immediate $200,000 capital expenditure for 14 new Dell PowerEdge servers. This upfront cost would severely impact the Q2 cash flow, whereas AWS offered a monthly operational expense model.'"
        ],
        "alternatives": ["Alternative 1 and why it was rejected", "Alternative 2 and why it was rejected"],
        "outcome": "The final result or action item",
        "tags": ["tag1", "tag2"]
    }}
    """

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs raw JSON without markdown code fences."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=settings.LLM_MODEL,
            temperature=0,
            # response_format={"type": "json_object"} # Groq supports this for Llama 3.1, for 3 it's safer to prompt
        )

        content = chat_completion.choices[0].message.content
        
        # Clean up potential markdown code blocks if the model ignores instruction
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "")
        elif "```" in content:
             content = content.replace("```", "")
            
        data = json.loads(content)
        
        nodes_data = data if isinstance(data, list) else []
        
        # Handle dict wrapper
        if isinstance(data, dict):
             if "decisions" in data:
                 nodes_data = data["decisions"]
             elif "Decision Logs" in data: # Handle potential key variation
                 nodes_data = data["Decision Logs"]
             elif "decision_title" in data: # Handle raw single object
                 nodes_data = [data]
             else:
                 for val in data.values():
                     if isinstance(val, list):
                         nodes_data = val
                         break

        results = []
        for item in nodes_data:
            item["source_file"] = filename
            
            # Ensure rationale is a list (handle LLM inconsistency)
            if "rationale" in item and isinstance(item["rationale"], str):
                 # Split by bullets or just wrap
                 rationale_text = item["rationale"]
                 if "\n-" in rationale_text:
                     item["rationale"] = [x.strip("-").strip() for x in rationale_text.split("\n") if x.strip()]
                 else:
                     item["rationale"] = [rationale_text]

            # Ensure alternatives are strings (handle LLM returning objects)
            if "alternatives" in item and isinstance(item["alternatives"], list):
                new_alts = []
                for x in item["alternatives"]:
                    if isinstance(x, dict):
                        # Flatten complex object to string
                        name = x.get('name', 'Option')
                        reason = x.get('reason_rejected', x.get('description', ''))
                        new_alts.append(f"{name}: {reason}")
                    else:
                        new_alts.append(str(x))
                item["alternatives"] = new_alts
            
            node = DecisionNode(**item)
            results.append(node)
        return results

    except Exception as e:
        logger.error(f"Failed to parse Groq output: {e}\nRaw content: {content if 'content' in locals() else 'N/A'}")
        return []

def embed_text(text: str) -> List[float]:
    """
    Generates embedding using local SentenceTransformer model.
    Returns a list of floats (size 384 for all-MiniLM-L6-v2).
    """
    return embedding_model.encode(text).tolist()

def ingest_file(file_path: str):
    filename = file_path.split("/")[-1] 
    
    # 1. Extract Text
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # 2. Extract Structure
    decisions = extract_decisions_using_llm(text, filename)

    if not decisions:
        logger.warning(f"No decisions found in {filename}")
        return

    points = []
    for decision in decisions:
        # 3. Create Vector content (Flatten list for embedding)
        rationale_text = " ".join(decision.rationale)
        vector_content = f"{decision.decision_title}: {rationale_text}"
        embedding = embed_text(vector_content)
        
        # 4. Prepare Payload
        payload = decision.model_dump()
        
        # 5. Create Point
        point_id = str(uuid.uuid4())
        points.append(
            models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
        )

    # 6. Upload
    db_client.upsert_points(points)
    logger.info(f"Successfully ingested {len(points)} decisions from {filename}")
