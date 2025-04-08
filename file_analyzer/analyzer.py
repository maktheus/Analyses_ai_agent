import os
from pathlib import Path
from typing import Optional, List, Dict
import ollama
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from .indexer import FileIndexer

class FileAnalyzer:
    def __init__(
        self,
        model_name: str = "mistral",
        index_path: Optional[str] = None,
        verbose: bool = False
    ):
        self.model_name = model_name
        self.index_path = index_path or "./index"
        self.verbose = verbose
        self.indexer = FileIndexer(index_path=index_path, verbose=verbose)

    def _setup_qa_chain(self, vectorstore: FAISS) -> RetrievalQA:
        """Configura a cadeia de QA usando o modelo local."""
        return RetrievalQA.from_chain_type(
            llm=ollama.chat,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

    def analyze_file(self, file_path: Path, qa_chain: RetrievalQA) -> Dict:
        """Analisa um arquivo específico."""
        if self.verbose:
            print(f"Analisando arquivo: {file_path}")

        # Lê o conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Prepara o prompt para análise
        prompt = f"""
        Analise o seguinte conteúdo do arquivo {file_path.name}:
        
        {content[:1000]}  # Limita o tamanho para não sobrecarregar o modelo
        
        Por favor, forneça:
        1. Um resumo do conteúdo
        2. Principais pontos ou padrões identificados
        3. Possíveis problemas ou áreas de atenção
        """

        # Obtém a análise do modelo
        response = qa_chain.run(prompt)

        return {
            'file': str(file_path),
            'analysis': response
        }

    def analyze_directory(self, directory: Path) -> List[Dict]:
        """Analisa todos os arquivos em um diretório."""
        if self.verbose:
            print(f"Iniciando análise do diretório: {directory}")

        # Carrega ou cria o índice
        try:
            vectorstore = self.indexer.load_index()
        except FileNotFoundError:
            if self.verbose:
                print("Índice não encontrado. Criando novo índice...")
            self.indexer.index_directory(directory)
            vectorstore = self.indexer.load_index()

        # Configura a cadeia de QA
        qa_chain = self._setup_qa_chain(vectorstore)

        # Analisa cada arquivo
        results = []
        for file_path in directory.glob("**/*.txt"):
            if file_path.is_file():
                try:
                    result = self.analyze_file(file_path, qa_chain)
                    results.append(result)
                except Exception as e:
                    if self.verbose:
                        print(f"Erro ao analisar {file_path}: {str(e)}")

        return results 