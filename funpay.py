from FunPayAPI import Account, Runner, types, enums
import os
import json
TOKEN = ""

file_path = os.path.join(os.path.dirname(__file__), 'processed_chats.json')

def load_processed_chats(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding= 'utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return set(data)
    return set()

def save_processed_chats(processed_chats, file_path):
    with open(file_path, 'w', encoding= 'utf-8') as file:
        json.dump(list(processed_chats), file, ensure_ascii= False, indent=4)

greeting_sent = False
help_r = 0

acc = Account(TOKEN).get()
runner = Runner(acc)
processed_chats = load_processed_chats(file_path)
print('Бот был запущен...\n')


def help1(chat_id):
    acc.send_message(chat_id, "Позвал продавца!\n Ожидайте его в течение 5 минут")

def help2(chat_id):
    acc.send_message(chat_id, "Я вас внимательно слушаю!\nМаксимально подробно опишите жалобу на товар")

def welcome(chat_id):
    acc.send_message(chat_id, "Здравствуйте! Ожидайте ответа продавца, обычно это происходит в течение 5 минут")

def help(chat_id):
    acc.send_message(
        chat_id, 
        "Нужна помощь? Я всегда рядом!\nЕсли вы хотите задать вопрос по товару:\nНапишите 1 и ожидайте ответ продавца\nЕсли вы хотите описать какую-либо проблему с товаром:\nНапишите 2 и ожидайте моего ответа"
    )


for event in runner.listen(requests_delay=4):
    if event.type is enums.EventTypes.NEW_MESSAGE:
        chat_id = event.message.chat_id
        author_id = event.message.author_id

        if author_id == 0:
            continue

        if author_id != acc.id:
            if chat_id not in processed_chats:
                processed_chats.add(chat_id)
                save_processed_chats(processed_chats, file_path)
                welcome(chat_id)

            elif event.message.text.lower() == 'помощь':
                help(chat_id)
                help_r += 1

            
            elif help_r > 0 and event.message.text == '1':
                help1(chat_id)

            elif help_r > 0 and event.message.text == '2':
                help2(chat_id)
                
            
    elif event.type is enums.EventTypes.NEW_ORDER:
        chat = acc.get_chat_by_name(event.order.buyer_username, True)
        acc.send_message(chat.id, f"Спасибо за покупку, сейчас продавец вам выдаст товар!")
