import re
import json

class Person:
    def __init__(self, pid, name, mail):
        self.pid = pid
        self.name = name
        self.mail = mail

    def check_mail(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, self.mail))

    def __repr__(self):
        return f"{self.name} {self.mail}"

class ParserCSV:
    @staticmethod
    def parse(text):
        items = text.strip().split(';')
        if len(items) == 3:
            return Person(items[0], items[1], items[2])
        return None

class ParserJSON:
    @staticmethod
    def parse(text):
        try:
            data = json.loads(text)
            uid = data.get('id', data.get('uid', ''))
            
            first = data.get('first_name', '')
            last = data.get('last_name', '')
            if first and last:
                full = f"{first} {last}"
            else:
                full = data.get('name', '')
            
            email_data = data.get('contacts', {})
            if isinstance(email_data, dict):
                email = email_data.get('email', data.get('email', ''))
            else:
                email = data.get('email', '')
            
            return Person(uid, full, email)
        except:
            return None

class ParserRAW:
    @staticmethod
    def parse(text):
        parts = text.strip().split()
        mail = ''
        name_parts = []
        
        for p in parts:
            if '@' in p and '.' in p:
                mail = p
            else:
                name_parts.append(p)
        
        if name_parts and mail:
            uid = str(abs(hash(''.join(name_parts) + mail)))
            return Person(uid, ' '.join(name_parts), mail)
        return None

class Collection:
    def __init__(self):
        self.items = []
    
    def add(self, data):
        if data:
            self.items.append(data)
    
    def process_line(self, line):
        line = line.strip()
        
        if line.startswith('csv '):
            person = ParserCSV.parse(line[4:])
        elif line.startswith('json '):
            person = ParserJSON.parse(line[5:])
        elif line.startswith('raw '):
            person = ParserRAW.parse(line[4:])
        else:
            # Автоопределение
            if '{' in line:
                person = ParserJSON.parse(line)
            elif ';' in line:
                person = ParserCSV.parse(line)
            else:
                person = ParserRAW.parse(line)
        
        if person:
            self.add(person)
            return True
        return False
    
    def get_mails(self):
        return [p.mail for p in self.items if p.mail]
    
    def search_name(self, text):
        return [p for p in self.items if text.lower() in p.name.lower()]
    
    def bad_mails(self):
        return [p for p in self.items if not p.check_mail()]
    
    def show_all(self):
        print("\nВсе записи:")
        for i, p in enumerate(self.items, 1):
            status = "✓" if p.check_mail() else "✗"
            print(f"{i:2}. {p} [{status}]")
    
    def show_info(self):
        total = len(self.items)
        good = sum(1 for p in self.items if p.check_mail())
        bad = total - good
        
        print(f"\nИнформация:")
        print(f"Всего записей: {total}")
        print(f"Правильные email: {good}")
        print(f"Неправильные email: {bad}")
        if total > 0:
            print(f"Процент правильных: {(good/total*100):.1f}%")

def run():
    col = Collection()
    
    print("Введите данные (Enter для завершения):")
    print("Форматы:")
    print("  csv код;имя;почта")
    print("  json {\"uid\": 1, \"name\": \"...\", \"email\": \"...\"}")
    print("  raw имя фамилия почта@домен.ру")
    
    count = 1
    while True:
        line = input(f"\nЗапись {count}: ").strip()
        if not line:
            break
        
        if col.process_line(line):
            print(f"✓ Добавлено")
            count += 1
        else:
            print("✗ Ошибка формата")
    
    if not col.items:
        print("Нет данных для работы")
        return
    
    print("\n" + "="*50)
    print("Доступные действия:")
    print("  mails - все адреса почты")
    print("  search часть_имени - поиск по имени")
    print("  bad - некорректные email")
    print("  list - все записи")
    print("  info - статистика")
    print("  end - выход")
    print("="*50)
    
    while True:
        cmd = input("\nДействие: ").strip().lower()
        
        if cmd == 'end':
            break
        
        elif cmd == 'mails':
            mails = col.get_mails()
            if mails:
                print("\nВсе адреса:")
                for i, m in enumerate(mails, 1):
                    print(f"  {i}. {m}")
            else:
                print("Адресов нет")
        
        elif cmd.startswith('search '):
            search_text = cmd[7:].strip()
            if search_text:
                results = col.search_name(search_text)
                print(f"\nНайдено: {len(results)}")
                for i, r in enumerate(results, 1):
                    print(f"  {i}. {r}")
            else:
                print("Укажите текст для поиска")
        
        elif cmd == 'bad':
            bad = col.bad_mails()
            print(f"\nНекорректные email: {len(bad)}")
            for i, p in enumerate(bad, 1):
                print(f"  {i}. {p}")
        
        elif cmd == 'list':
            col.show_all()
        
        elif cmd == 'info':
            col.show_info()
        
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    run()
