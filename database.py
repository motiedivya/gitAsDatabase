import os
import json
from git import Repo, GitCommandError

class GitDB:
    def __init__(self, repo_path):
        # Initialize or open existing repo
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
            self.repo = Repo.init(repo_path)
        else:
            self.repo = Repo(repo_path)
        self.repo_path = repo_path

    def _load_file(self, filename, commit='HEAD'):
        try:
            commit_obj = self.repo.commit(commit)
            file_data = (commit_obj.tree / filename).data_stream.read()
            return json.loads(file_data)
        except (KeyError, GitCommandError, FileNotFoundError):
            # File doesn't exist in that commit or repo
            return {}
        except Exception as e:
            print(f"Error loading file '{filename}' at commit '{commit}': {e}")
            return {}

    def _save_file(self, filename, data, commit_message):
        file_path = os.path.join(self.repo_path, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        self.repo.index.add([filename])
        self.repo.index.commit(commit_message)

    def create_record(self, filename, record_id, record_data):
        """
        Create a new record. Fail if ID already exists.
        """
        data = self._load_file(filename)
        if record_id in data:
            print(f"Record {record_id} already exists. Use update_record to modify.")
            return False
        data[record_id] = record_data
        self._save_file(filename, data, f"Create record {record_id}")
        print(f"Record {record_id} created.")
        return True

    def read_record(self, filename, record_id, commit='HEAD'):
        """
        Read a record by ID at a specific commit (default HEAD).
        """
        data = self._load_file(filename, commit)
        record = data.get(record_id)
        if record is None:
            print(f"Record {record_id} not found at commit {commit}.")
        return record

    def update_record(self, filename, record_id, record_data):
        """
        Update an existing record. Fail if ID does not exist.
        """
        data = self._load_file(filename)
        if record_id not in data:
            print(f"Record {record_id} does not exist. Use create_record to add new records.")
            return False
        data[record_id] = record_data
        self._save_file(filename, data, f"Update record {record_id}")
        print(f"Record {record_id} updated.")
        return True

    def delete_record(self, filename, record_id):
        """
        Delete a record by ID. Fail if ID does not exist.
        """
        data = self._load_file(filename)
        if record_id not in data:
            print(f"Record {record_id} does not exist.")
            return False
        del data[record_id]
        self._save_file(filename, data, f"Delete record {record_id}")
        print(f"Record {record_id} deleted.")
        return True

    def list_records(self, filename, commit='HEAD'):
        """
        List all record IDs in a file at a specific commit.
        """
        data = self._load_file(filename, commit)
        return list(data.keys())

# Example usage
if __name__ == "__main__":
    db = GitDB('./my_git_db')

    # CREATE
    db.create_record('users.json', 'user1', {"name": "Alice", "age": 30})
    db.create_record('users.json', 'user2', {"name": "Bob", "age": 25})
    db.create_record('users.json', 'user3', {"name": "John", "age": 22})

    # READ
    print("Read user1:", db.read_record('users.json', 'user1'))

    # UPDATE

    db.update_record('users.json', 'user1', {"name": "Alice", "age": 31, "skills": ["python", "git"]})

    # DELETE
    db.delete_record('users.json', 'user2')

    # LIST
    print("All users:", db.list_records('users.json'))
