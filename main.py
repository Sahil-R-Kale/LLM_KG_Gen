import os, argparse
import json
from typing import List
from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel
from core.llm_interface import Prompt, create_and_send_prompt  
from core.prompts import EXTRACTION_PROMPT

class Triple(BaseModel):
    subject: str
    relation: str
    object: str

class TripleExtractionResult(BaseModel):
    triples: List[Triple]

@dataclass
class TripleExtractor:
    model_name: str = "gpt-4o"

    def _build_prompt(self, input_text: str, format_instructions: str) -> Prompt:
        prompt_text = EXTRACTION_PROMPT.format(
            input_text=input_text,
            format_instructions=format_instructions
        )
        return Prompt(
            user_prompt=prompt_text,
            model=self.model_name
        )

    def extract_triples(self, input_text: str) -> TripleExtractionResult:
        llm_response = self.send_prompt(input_text)
        raw_response = llm_response.content
        if not raw_response or not raw_response.strip():
            raise ValueError("LLM response is empty. Ensure prompt is being sent correctly and the model returned valid output.")
        
        try:
            # Strip triple backticks if present
            raw_response = raw_response.strip()
            if raw_response.startswith("```json"):
                raw_response = raw_response[len("```json"):].strip()
            if raw_response.startswith("```"):
                raw_response = raw_response[3:].strip()
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3].strip()

            triples = json.loads(raw_response)
            parsed = TripleExtractionResult(triples=[Triple(**t) for t in triples])
        except Exception as e:
            raise ValueError(f"Failed to parse LLM output: {e}\nRaw response:\n{raw_response}")
        return parsed

    @create_and_send_prompt
    def send_prompt(self, input_text: str) -> Prompt:
        return self._build_prompt(input_text, format_instructions="Output only and only a JSON array of triples: [{\"subject\": ..., \"relation\": ..., \"object\": ...}]. Do not include any additional text or explanations. Ensure the output is valid JSON and does not contain any comments or extra formatting.")

    def process_file(self, input_path: str, output_path: str):
        with open(input_path, "r", encoding="utf-8") as infile:
            full_text = infile.read()

        result = self.extract_triples(full_text)
        triples_data = [[t.subject, t.relation, t.object] for t in result.triples]

        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(triples_data, outfile, indent=2)

        print(f"Extracted {len(triples_data)} triples. Saved to {output_path}")
        return triples_data

    def visualize(self, triple_file: str):
        with open(triple_file, "r", encoding="utf-8") as f:
            triples = json.load(f)

        G = nx.DiGraph()
        for subj, rel, obj in triples:
            G.add_edge(subj, obj, label=rel)

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
                node_size=2000, font_size=10)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        plt.title("Knowledge Graph")
        plt.show()

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and visualize triples from a text file.")
    parser.add_argument("--input_path", required=True, help="Path to the input text file")
    parser.add_argument("--output_dir", default="outputs", help="Directory to save the output JSON file (default: outputs/)")
    parser.add_argument("--model", default="gpt-4o", help="LLM model name (default: gpt-4o)")
    parser.add_argument("--visualize", action="store_true", help="Visualize the extracted triples")

    args = parser.parse_args()

    extractor = TripleExtractor(model_name=args.model)
    input_path = args.input_path
    output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(input_path)
    filename_wo_ext = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"triples_{filename_wo_ext}_{args.model}.json")

    extractor.process_file(input_path, output_path)

    if args.visualize:
        extractor.visualize(output_path)