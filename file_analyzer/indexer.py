import os
from pathlib import Path
from typing import Optional, List
import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class FileIndexer:
    def __init__(
        self,
        index_path: Optional[str] = None,
        verbose: bool = False
    ):
        self.index_path = index_path or "./index"
        self.verbose = verbose
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def _load_files(self, directory: Path) -> List[str]:
        """Carrega todos os arquivos de texto do diretório."""
        loader = DirectoryLoader(
            str(directory),
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def index_directory(self, directory: Path) -> None:
        """Indexa todos os arquivos em um diretório."""
        if self.verbose:
            print(f"Indexando arquivos em {directory}...")

        # Carrega e divide os documentos
        documents = self._load_files(directory)

        # Cria o índice FAISS
        vectorstore = FAISS.from_documents(documents, self.embeddings)

        # Salva o índice
        vectorstore.save_local(self.index_path)

        if self.verbose:
            print(f"Índice salvo em {self.index_path}")

    def load_index(self) -> FAISS:
        """Carrega um índice existente."""
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"Índice não encontrado em {self.index_path}")
        
        return FAISS.load_local(self.index_path, self.embeddings) 