from __future__ import annotations

import argparse
from pathlib import Path

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.rag_demo_common import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_KNOWLEDGE_PATH,
    DEFAULT_OLLAMA_API_KEY,
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_QDRANT_COLLECTION,
    DEFAULT_QDRANT_HOST,
    DEFAULT_QDRANT_PORT,
    seed_collection,
    setup_logging,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Наполняет Qdrant демо-знаниями по кредитным политикам."
    )
    parser.add_argument(
        "--knowledge-file",
        default=str(DEFAULT_KNOWLEDGE_PATH),
        help="Путь до JSON-файла со знаниями.",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_QDRANT_COLLECTION,
        help="Имя коллекции в Qdrant.",
    )
    parser.add_argument(
        "--qdrant-host",
        default=DEFAULT_QDRANT_HOST,
        help="Хост Qdrant.",
    )
    parser.add_argument(
        "--qdrant-port",
        type=int,
        default=DEFAULT_QDRANT_PORT,
        help="REST-порт Qdrant.",
    )
    parser.add_argument(
        "--ollama-base-url",
        default=DEFAULT_OLLAMA_BASE_URL,
        help="OpenAI-compatible URL локального Ollama.",
    )
    parser.add_argument(
        "--ollama-api-key",
        default=DEFAULT_OLLAMA_API_KEY,
        help="API key для Ollama.",
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Локальная embedding-модель через Ollama.",
    )
    parser.add_argument(
        "--hide-chunks",
        action="store_true",
        help="Не печатать полный каталог чанков перед загрузкой.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    logger = setup_logging()
    knowledge_path = Path(args.knowledge_file).expanduser().resolve()

    logger.info(
        "Старт индексации демо-знаний: file=%s, collection=%s, qdrant=%s:%d, embedding_model=%s",
        knowledge_path,
        args.collection,
        args.qdrant_host,
        args.qdrant_port,
        args.embedding_model,
    )

    seed_collection(
        knowledge_path=knowledge_path,
        qdrant_host=args.qdrant_host,
        qdrant_port=args.qdrant_port,
        collection_name=args.collection,
        ollama_base_url=args.ollama_base_url,
        ollama_api_key=args.ollama_api_key,
        embedding_model=args.embedding_model,
        logger=logger,
        show_chunks=not args.hide_chunks,
    )

    logger.info("Индексация завершена успешно.")


if __name__ == "__main__":
    main()
