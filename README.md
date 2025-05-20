# GitDB – Use Git as a Lightweight Database in Python

## Overview

**GitDB** is a lightweight Python-based database that leverages [Git](https://git-scm.com/) as a versioned storage backend for your JSON data.
Each record is stored in a JSON file, and every change (create, update, delete) is tracked as a Git commit, allowing you to view or revert historical changes easily.

This approach is ideal for:

* Prototyping applications that need versioned data,
* Auditing changes in small to medium datasets,
* Learning about data versioning and Git internals,
* Projects without a heavy database requirement.

## Features

* **Create, Read, Update, Delete (CRUD)** operations on JSON data
* Every operation is saved as a Git commit (full history, auditability)
* Read any record at any past Git commit (time travel!)
* List all record IDs at any Git revision

## Requirements

* Python 3.6+
* [GitPython](https://github.com/gitpython-developers/GitPython) (`pip install gitpython`)

## Quick Start

1. **Install GitPython**

   ```bash
   pip install gitpython
   ```

2. **Copy the `GitDB` class to your project**

3. **Usage Example**

   ```python
   from git_db import GitDB  # Or paste the GitDB class into your code

   db = GitDB('./my_git_db')

   # CREATE
   db.create_record('users.json', 'user1', {"name": "Alice", "age": 30})
   db.create_record('users.json', 'user2', {"name": "Bob", "age": 25})

   # READ
   print("Read user1:", db.read_record('users.json', 'user1'))

   # UPDATE
   db.update_record('users.json', 'user1', {"name": "Alice", "age": 31})

   # DELETE
   db.delete_record('users.json', 'user2')

   # LIST
   print("All users:", db.list_records('users.json'))
   ```

## API

| Method                                     | Description                                            |
| ------------------------------------------ | ------------------------------------------------------ |
| `create_record(filename, record_id, data)` | Create a record; fails if the ID exists                |
| `read_record(filename, record_id, commit)` | Read record by ID at a specific commit (default: HEAD) |
| `update_record(filename, record_id, data)` | Update an existing record; fails if not present        |
| `delete_record(filename, record_id)`       | Delete a record by ID                                  |
| `list_records(filename, commit)`           | List all record IDs at a given commit (default: HEAD)  |

**Arguments:**

* `filename`: Name of the JSON file (e.g., `users.json`)
* `record_id`: Key of the record inside the JSON file
* `data`: Dictionary representing the record's value
* `commit`: Optional Git commit hash or ref

## Data Layout

Each JSON file is a dictionary of records. For example:

```json
{
    "user1": { "name": "Alice", "age": 30 },
    "user2": { "name": "Bob", "age": 25 }
}
```

## Versioning

Every create, update, or delete is committed to Git, making it easy to review or roll back changes using standard Git commands.

---

## Limitations

* Not suitable for large datasets (the entire JSON file is loaded/saved for each change)
* Not concurrent-safe (avoid multi-process writes)
* No indexing or advanced querying (purely key-value)
* Not intended as a replacement for production-grade databases

---

## Optimizations & Suggestions

Sir, here are a few ways you can optimize or improve your implementation:

### 1. **Reduce Full File Loads/Saves**

* **Current:** Every create/update/delete loads and writes the full JSON file.
* **Suggestion:** For very large files, consider breaking up storage into one-file-per-record (e.g., `users/user1.json`), then use a directory as a "table." This is also Git-friendly and avoids large diffs.

### 2. **Add Locking for Safety**

* If your code might run in parallel (multiple processes), use a lock (e.g., file lock) to prevent simultaneous writes.

### 3. **Error Handling & Logging**

* Replace `print` with proper logging and custom exceptions, so that usage in larger apps is safer.

### 4. **Atomic Writes**

* Write to a temp file and then move it into place to reduce risk of data corruption on crashes.

### 5. **Custom Commit Metadata**

* Add author info, timestamps, or tags in commit messages for richer history.

### 6. **Configurable Serialization**

* Allow storing data as YAML, TOML, etc., not just JSON.

### 7. **Optional: Batch Operations**

* Support batch writes (many creates/updates in a single commit).

### 8. **Unit Tests**

* Add automated tests to ensure reliability of CRUD operations.

---

## License

MIT License.
Use at your own risk. Not suitable for high-volume production environments.

