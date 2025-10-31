

if __name__ == "__main__":


rows = 5
seats_in_row = 10
cinema_hall = [[0] * seats_in_row for _ in range(rows)]

def show_hall():
    
    print("\n" + "="*50)
    print("КИНОТЕАТР - состояние зала:")
    print("0 - свободно, 1 - занято")
    print("="*50)
    
    print("   " + " ".join(f"{i+1:2}" for i in range(seats_in_row)))
    
    for i, row in enumerate(cinema_hall):
        print(f"Ряд {i+1}: {row}")
    print()

def book_seats():
    
    show_hall()
    
    try:
        row = int(input("Введите номер ряда (1-5): "))
        if row < 1 or row > rows:
            print("Ошибка: такого ряда нет!")
            return
        
        seat = int(input("Введите номер места (1-10): "))
        if seat < 1 or seat > seats_in_row:
            print("Ошибка: такого места нет!")
            return
        
      
        if cinema_hall[row-1][seat-1] == 0:
            cinema_hall[row-1][seat-1] = 1
            print(f"✓ Успешно! Место {seat} в ряду {row} забронировано")
        else:
            print(f"✗ Место {seat} в ряду {row} уже занято!")
            
    except ValueError:
        print("Ошибка: введите числа!")

def book_multiple_seats():
    show_hall()
    
    try:
        row = int(input("Введите номер ряда (1-5): "))
        if row < 1 or row > rows:
            print("Ошибка: такого ряда нет!")
            return
        
        start_seat = int(input("Введите номер первого места (1-10): "))
        num_seats = int(input("Сколько мест забронировать? "))
        
        if start_seat < 1 or (start_seat + num_seats - 1) > seats_in_row:
            print("Ошибка: вышли за границы ряда!")
            return
        
        all_free = True
        for i in range(num_seats):
            if cinema_hall[row-1][start_seat-1 + i] == 1:
                all_free = False
                print(f"✗ Место {start_seat + i} уже занято!")
                break
        
        if all_free:
            for i in range(num_seats):
                cinema_hall[row-1][start_seat-1 + i] = 1
            print(f"✓ Успешно! Забронированы места {start_seat}-{start_seat+num_seats-1} в ряду {row}")
            
    except ValueError:
        print("Ошибка: введите числа!")


while True:
    print("\n=== КИНОТЕАТР ===")
    print("1. Показать зал")
    print("2. Забронировать одно место")
    print("3. Забронировать несколько мест подряд")
    print("4. Выйти")
    
    choice = input("Выберите действие (1-4): ")
    
    if choice == "1":
        show_hall()
    elif choice == "2":
        book_seats()
    elif choice == "3":
        book_multiple_seats()
    elif choice == "4":
        print("До свидания!")
        break
    else:
        print("Неверный выбор! Попробуйте снова.")
