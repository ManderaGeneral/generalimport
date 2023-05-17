from generalimport.helper import generate_import_messages

print(generate_import_messages(path="generalimport/pyprojectexample.toml", name="farm-haystack", include=(
    # "pydantic", # Required for all dataclasses
    # "tenacity",  # Probably needed because it's a decorator, to be evaluated
    # "pandas",
    "aiorwlock",
    "azure",
    "beautifulsoup4",
    "beir",
    "boilerpy3",
    "canals",
    "dill",
    "docx",
    "elasticsearch",
    "events",
    "faiss",
    "fitz",
    "frontmatter",
    "huggingface_hub",
    "jsonschema",
    "langdetect",
    "magic",
    "markdown",
    "mlflow",
    "mmh3",
    "more_itertools",
    "networkx",
    "nltk",
    "numpy",
    "onnxruntime",
    "onnxruntime_tools",
    "opensearchpy",
    "pdf2image",
    "PIL",
    "pinecone",
    "posthog",
    "protobuf",
    "psycopg2",
    "pymilvus",
    "pytesseract",
    "quantulum3",
    "rank_bm25",
    "rapidfuzz",
    "ray",
    "rdflib",
    "requests",
    "scipy",
    "selenium",
    "sentence_transformers",
    "seqeval",
    "sklearn",
    "SPARQLWrapper",
    "sqlalchemy",
    "sseclient",
    "tenacity",
    "tika",
    "tiktoken",
    "tokenizers",
    "torch",
    "tqdm",
    "transformers",
    "weaviate",
    "webdriver_manager",
    "whisper",
    "yaml")))


from generalimport import generalimport

from generalimport import generalimport
generalimport(
    "PIL",
    "azure",
    "boilerpy3",
    "canals",
    "dill",
    "docx",
    "events",
    "faiss",
    "fitz",
    "frontmatter",
    "huggingface_hub",
    "jsonschema",
    "magic",
    "mmh3",
    "more_itertools",
    "networkx",
    "numpy",
    "opensearchpy",
    "pinecone",
    "posthog",
    "protobuf",
    "psycopg2",
    "quantulum3",
    "rank_bm25",
    "requests",
    "sentence_transformers",
    "sklearn",
    "sseclient",
    "tenacity",
    "tiktoken",
    "tokenizers",
    "torch",
    "tqdm",
    "transformers",
    "weaviate",
    "webdriver_manager",
    "whisper",
    "yaml",
    # ("PyMuPDF", "pdf"),
    ("SPARQLWrapper", ("graphdb", "inmemorygraph")),
    ("aiorwlock", "ray"),
    ("beautifulsoup4", "file-conversion"),
    ("beir", "beir"),
    # ("black", "formatting"),
    # ("coverage", "dev"),
    ("elasticsearch", "elasticsearch"),
    # ("faiss-cpu", "only-faiss"),
    # ("faiss-gpu", "only-faiss-gpu"),
    # ("jupytercontrib", "dev"),
    ("langdetect", "preprocessing"),
    ("markdown", "file-conversion"),
    # ("mkdocs", "dev"),
    ("mlflow", "metrics"),
    # ("mypy", "dev"),
    ("nltk", "preprocessing"),
    ("onnxruntime", "onnx"),
    # ("onnxruntime-gpu", "onnx-gpu"),
    ("onnxruntime_tools", ("onnx", "onnx-gpu")),
    # ("openai-whisper", "audio"),
    # ("opensearch-py", "opensearch"),
    ("pdf2image", "ocr"),
    # ("pillow", "colab"),
    # ("pinecone-client", "only-pinecone"),
    # ("pre-commit", "dev"),
    # ("psutil", "dev"),
    # ("psycopg2-binary", "sql"),
    # ("pydoc-markdown", "dev"),
    # ("pylint", "dev"),
    ("pymilvus", "only-milvus"),
    ("pytesseract", "ocr"),
    # ("pytest", "dev"),
    # ("pytest-asyncio", "dev"),
    # ("pytest-cov", "dev"),
    # ("pytest-custom_exit_code", "dev"),
    # ("python-docx", "file-conversion"),
    # ("python-frontmatter", "file-conversion"),
    # ("python-magic", "file-conversion"),
    # ("python-magic-bin", "file-conversion"),
    # ("python-multipart", "dev"),
    ("rapidfuzz", "metrics"),
    ("ray", "ray"),
    ("rdflib", ("inmemorygraph", "graphdb")),
    # ("responses", "dev"),
    ("scipy", "metrics"),
    ("selenium", "crawler"),
    ("seqeval", "metrics"),
    ("sqlalchemy", "sql"),
    # ("sqlalchemy_utils", "sql"),
    ("tika", "file-conversion"),
    # ("toml", "dev"),
    # ("tox", "dev"),
    # ("typing_extensions", "dev"),
    # ("watchdog", "dev"),
    # ("weaviate-client", "weaviate"),
    # ("webdriver-manager", "crawler"),
)

