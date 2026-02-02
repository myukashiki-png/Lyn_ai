from memory.vector_store import VectorStore

store = VectorStore()

def retrieve_context(query: str) -> str:
    memories = store.search(query)
    if not memories:
        return ""

    joined = "\n".join(memories)
    return f"Informasi relevan dari ingatan:\n{joined}"

