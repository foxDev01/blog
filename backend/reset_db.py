# cleanup_migrations.py
import os
import shutil
import glob
import sys

def cleanup_migrations():
    """Полная очистка миграций и БД"""
    
    # Удаляем файл БД
    db_files = ['db.sqlite3', 'dev.db', 'test.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✓ Удален файл БД: {db_file}")
    
    # Удаляем __pycache__
    pycache_count = 0
    for pycache in glob.glob('**/__pycache__', recursive=True):
        try:
            shutil.rmtree(pycache, ignore_errors=True)
            pycache_count += 1
        except:
            pass
    
    if pycache_count > 0:
        print(f"✓ Удалено папок __pycache__: {pycache_count}")
    
    # Очищаем папки миграций
    migrations_folders = glob.glob('*/migrations') + glob.glob('*/*/migrations')
    migration_files_removed = 0
    
    for migrations_path in migrations_folders:
        if os.path.exists(migrations_path):
            # Удаляем все .py файлы кроме __init__.py
            for file in os.listdir(migrations_path):
                file_path = os.path.join(migrations_path, file)
                if file.endswith('.py') and file != '__init__.py':
                    try:
                        os.remove(file_path)
                        migration_files_removed += 1
                    except:
                        pass
            
            # Удаляем __pycache__ внутри migrations
            pycache_in_migrations = os.path.join(migrations_path, '__pycache__')
            if os.path.exists(pycache_in_migrations):
                shutil.rmtree(pycache_in_migrations, ignore_errors=True)
    
    print(f"✓ Удалено файлов миграций: {migration_files_removed}")
    
    # Удаляем папки с собранными статическими файлами
    static_dirs = ['staticfiles', 'static', 'media']
    for static_dir in static_dirs:
        if os.path.exists(static_dir) and os.path.isdir(static_dir):
            try:
                shutil.rmtree(static_dir)
                print(f"✓ Удалена папка: {static_dir}")
            except:
                pass
    
    print("\n✅ Очистка завершена!")
    print("\nТеперь выполните:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser (опционально)")

if __name__ == "__main__":
    print("Начинаю очистку миграций и БД...")
    confirm = input("Вы уверены? (y/n): ")
    
    if confirm.lower() == 'y':
        cleanup_migrations()
    else:
        print("Очистка отменена.")