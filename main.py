import json
import os.path
from datetime import datetime


class Note:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def update(self, title, body):
        self.title = title
        self.body = body
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class NotesManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.notes = []

        if os.path.isfile(self.filepath):
            with open(self.filepath, 'r') as f:
                notes_data = json.load(f)
                for note_data in notes_data:
                    note = Note(
                        note_data['id'],
                        note_data['title'],
                        note_data['body']
                    )
                    note.created_at = datetime.fromisoformat(note_data['created_at'])
                    note.updated_at = datetime.fromisoformat(note_data['updated_at'])
                    self.notes.append(note)

    def save(self):
        with open(self.filepath, 'w') as f:
            notes_data = [note.to_dict() for note in self.notes]
            json.dump(notes_data, f, indent=4)

    def add(self, title, body):
        id = len(self.notes) + 1
        note = Note(id, title, body)
        self.notes.append(note)
        self.save()

    def delete(self, id):
        for note in self.notes:
            if note.id == id:
                self.notes.remove(note)
                self.save()
                return True
        return False

    def update(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.update(title, body)
                self.save()
                return True
        return False

    def get_by_id(self, id):
        for note in self.notes:
            if note.id == id:
                return note
        return None


class NotesCLI:
    def __init__(self):
        self.manager = NotesManager('notes.json')

    def start(self):
        print('Добро пожаловать в NoteOne!')
        while True:
            command = input('В ведите команду: (добавить, список, просмотреть, обновить, удалить, выход): ')
            if command == 'добавить':
                title = input('Введите название Заметки: ')
                body = input('Введите текст Заметки: ')
                self.manager.add(title, body)
                print('Заметка добавлена.')
            elif command == 'список':
                for note in self.manager.notes:
                    print(f'{note.id}. {note.title} ({note.created_at.strftime("%Y-%m-%d %H:%M:%S")})')
            elif command == 'просмотреть':
                id = input('Введите id Заметки: ')
                note = self.manager.get_by_id(int(id))
                if note:
                    print(f'{note.title}\n{note.body}\n{note.updated_at.strftime("%Y-%m-%d %H:%M:%S")}')
                else:
                    print(f'Заметка с id {id} не найдена.')
            elif command == 'обновить':
                id = input('Введите id Заметки: ')
                title = input('Введите название Заметки: ')
                body = input('Введите текст Заметки: ')
                if self.manager.update(int(id), title, body):
                    print('Заметка добавлена.')
                else:
                    print(f'Заметка с id {id} не найдена.')
            elif command == 'удалить':
                id = input('Введите id Заметки: ')
                if self.manager.delete(int(id)):
                    print('Заметка удалена.')
                else:
                    print(f'Заметка с id {id} не найдена.')
            elif command == 'выход':
                print('Возвращайтесь!')
                break
            else:
                print('Введена не правильная команда, попробуйте еще раз.')


if __name__ == '__main__':
    cli = NotesCLI()
    cli.start()
