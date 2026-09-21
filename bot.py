import string
import sys

FAQ_FILE = "faq.txt"

def normalize(text: str) -> set[str]:
    """Приводит текст к нижнему регистру, удаляет пунктуацию и разбивает на слова."""
    translator = str.maketrans("", "", string.punctuation)
    cleaned = text.translate(translator).lower()
    return set(cleaned.split())

def load_faq(filepath: str) -> list[dict]:
    """Загружает вопросы и ответы из faq.txt."""
    faq_data = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            blocks = content.split("\n\n") if "\n\n" in content else content.splitlines()
            
            for block in blocks:
                parts = block.split("|")
                if len(parts) == 3:
                    topic, question, answer = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    faq_data.append({
                        "topic": topic,
                        "question": question,
                        "answer": answer,
                        "keywords": normalize(f"{topic} {question}")
                    })
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден. Создайте его рядом со скриптом.")
        sys.exit(1)
    return faq_data

def find_answer(user_query: str, faq_data: list[dict]) -> str:
    """Ищет наиболее подходящий ответ по совпадению ключевых слов."""
    query_words = normalize(user_query)
    if not query_words:
        return "Не знаю"

    best_match = None
    max_score = 0

    for item in faq_data:
        # Считаем количество совпадающих слов
        score = len(query_words.intersection(item["keywords"]))
        if score > max_score:
            max_score = score
            best_match = item["answer"]

    # Если совпало хотя бы 1 ключевое слово
    if max_score > 0 and best_match:
        return best_match
    
    return "Не знаю"

def main():
    faq_data = load_faq(FAQ_FILE)
    print("=== FAQ-бот готов к работе! ===")
    print("Задайте вопрос про репетицию (время, команда, трек, сдача, призы).")
    print("Для выхода введите 'выход' или 'exit'.\n")

    while True:
        try:
            user_input = input("Вы: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("выход", "exit", "quit"):
                print("Бот: До свидания!")
                break

            answer = find_answer(user_input, faq_data)
            print(f"Бот: {answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nБот: До свидания!")
            break

if __name__ == "__main__":
    main()