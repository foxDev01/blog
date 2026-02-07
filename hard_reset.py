# hard_reset.py
import os
import shutil
import glob
import sys

def hard_reset():
    """Жесткий сброс всего проекта"""
    
    print("=" * 60)
    print("HARD RESET DJANGO PROJECT")
    print("=" * 60)
    
    # 1. Удаляем ВСЕ файлы БД
    db_patterns = ['*.sqlite3', '*.db', '*.sqlite']
    removed_dbs = []
    
    for pattern in db_patterns:
        for db_file in glob.glob(pattern):
            try:
                os.remove(db_file)
                removed_dbs.append(db_file)
                print(f"✓ Удален файл БД: {db_file}")
            except:
                pass
    
    # 2. Удаляем папки __pycache__
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"✓ Удален: {pycache_path}")
            except:
                pass
    
    # 3. Удаляем файлы .pyc
    for pyc_file in glob.glob('**/*.pyc', recursive=True):
        try:
            os.remove(pyc_file)
        except:
            pass
    
    # 4. Очищаем миграции
    migrations_found = False
    for root, dirs, files in os.walk('.'):
        if 'migrations' in dirs:
            migrations_path = os.path.join(root, 'migrations')
            init_file = os.path.join(migrations_path, '__init__.py')
            
            # Сохраняем __init__.py
            if os.path.exists(init_file):
                with open(init_file, 'r') as f:
                    init_content = f.read()
                
                # Удаляем все файлы в migrations
                for item in os.listdir(migrations_path):
                    item_path = os.path.join(migrations_path, item)
                    if item != '__init__.py':
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            else:
                                os.remove(item_path)
                            migrations_found = True
                        except:
                            pass
                
                # Восстанавливаем __init__.py
                with open(init_file, 'w') as f:
                    f.write(init_content)
    
    if migrations_found:
        print("✓ Очищены все папки migrations")
    
    # 5. Проверяем структуру проекта
    print("\n" + "=" * 60)
    print("СТРУКТУРА ПРОЕКТА:")
    
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"📁 {item}/")
            if item in ['venv', 'env', '.git', '.vscode']:
                print(f"   (системная папка)")
            elif os.path.exists(os.path.join(item, 'migrations')):
                print(f"   содержит папку migrations")
    
    print("\n" + "=" * 60)
    print("✅ Жесткий сброс завершен!")
    print("\nСледующие шаги:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py runserver")

if __name__ == "__main__":
    print("\n⚠️  ВНИМАНИЕ: Этот скрипт удалит ВСЕ файлы базы данных!")
    print("   Используйте только в разработке!\n")
    
    confirm = input("Продолжить? (y/N): ")
    if confirm.lower() == 'y':
        hard_reset()
    else:
        print("Отменено.")
        sys.exit(0)