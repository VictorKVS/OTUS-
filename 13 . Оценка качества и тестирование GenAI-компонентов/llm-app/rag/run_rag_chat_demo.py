from __future__ import annotations

import argparse
from pathlib import Path

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.rag_demo_common import (
    DEFAULT_CHAT_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_KNOWLEDGE_PATH,
    DEFAULT_OLLAMA_API_KEY,
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_QDRANT_COLLECTION,
    DEFAULT_QDRANT_HOST,
    DEFAULT_QDRANT_PORT,
    DEFAULT_TOP_K,
    answer_with_rag,
    load_knowledge_chunks,
    parse_optional_float,
    print_chunk_catalog,
    search_chunks,
    seed_collection,
    setup_logging,
)


HELP_TEXT = """Команды:
- `exit`, `quit`, `q`, `выход` — завершить диалог.
- `:help` — показать эту подсказку.
- `:chunks` — повторно распечатать все чанки базы знаний.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Запускает локальный RAG-диалог поверх Qdrant и Ollama."
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
        "--chat-model",
        default=DEFAULT_CHAT_MODEL,
        help="Локальная chat-модель через Ollama.",
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Локальная embedding-модель через Ollama.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Сколько top-k чанков брать из Qdrant.",
    )
    parser.add_argument(
        "--score-threshold",
        default="",
        help="Минимальный score Qdrant. По умолчанию фильтр отключен.",
    )
    parser.add_argument(
        "--question",
        default="",
        help="Если передан, будет выполнен один запрос без интерактивного цикла.",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Перед стартом диалога пересоздать коллекцию и заново залить знания.",
    )
    parser.add_argument(
        "--hide-chunks",
        action="store_true",
        help="Не печатать каталог чанков при старте.",
    )
    return parser


def run_single_turn(
    *,
    question: str,
    history: list[dict[str, str]],
    qdrant_host: str,
    qdrant_port: int,
    collection_name: str,
    ollama_base_url: str,
    ollama_api_key: str,
    embedding_model: str,
    chat_model: str,
    top_k: int,
    score_threshold: float | None,
    logger,
) -> str:
    hits = search_chunks(
        question=question,
        qdrant_host=qdrant_host,
        qdrant_port=qdrant_port,
        collection_name=collection_name,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        embedding_model=embedding_model,
        top_k=top_k,
        score_threshold=score_threshold,
        logger=logger,
    )
    return answer_with_rag(
        question=question,
        history=history,
        hits=hits,
        ollama_base_url=ollama_base_url,
        ollama_api_key=ollama_api_key,
        chat_model=chat_model,
        logger=logger,
    )


def main() -> None:
    args = build_parser().parse_args()
    logger = setup_logging()
    knowledge_path = Path(args.knowledge_file).expanduser().resolve()
    score_threshold = parse_optional_float(args.score_threshold)

    chunks = load_knowledge_chunks(knowledge_path)
    if args.reindex:
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
    elif not args.hide_chunks:
        print_chunk_catalog(chunks, logger)

    logger.info(
        "RAG-чат готов: collection=%s, qdrant=%s:%d, chat_model=%s, embedding_model=%s, top_k=%d",
        args.collection,
        args.qdrant_host,
        args.qdrant_port,
        args.chat_model,
        args.embedding_model,
        args.top_k,
    )

    history: list[dict[str, str]] = []

    if args.question.strip():
        answer = run_single_turn(
            question=args.question.strip(),
            history=history,
            qdrant_host=args.qdrant_host,
            qdrant_port=args.qdrant_port,
            collection_name=args.collection,
            ollama_base_url=args.ollama_base_url,
            ollama_api_key=args.ollama_api_key,
            embedding_model=args.embedding_model,
            chat_model=args.chat_model,
            top_k=args.top_k,
            score_threshold=score_threshold,
            logger=logger,
        )
        print("\nАссистент>\n" + answer)
        return

    print("Интерактивный RAG-диалог запущен.")
    print(HELP_TEXT)

    while True:
        try:
            question = input("Вы> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not question:
            continue

        lowered = question.lower()
        if lowered in {"exit", "quit", "q", "выход"}:
            print("Выход.")
            break
        if question == ":help":
            print(HELP_TEXT)
            continue
        if question == ":chunks":
            print_chunk_catalog(chunks, logger)
            continue

        answer = run_single_turn(
            question=question,
            history=history,
            qdrant_host=args.qdrant_host,
            qdrant_port=args.qdrant_port,
            collection_name=args.collection,
            ollama_base_url=args.ollama_base_url,
            ollama_api_key=args.ollama_api_key,
            embedding_model=args.embedding_model,
            chat_model=args.chat_model,
            top_k=args.top_k,
            score_threshold=score_threshold,
            logger=logger,
        )
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        history = history[-6:]

        print("\nАссистент>\n" + answer + "\n")


if __name__ == "__main__":
    main()
