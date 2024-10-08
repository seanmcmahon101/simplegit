### Welcome to simplegit

### Git for idiots

### Installation

1. **Prerequisites:**

- Ensure you have Python 3 installed on your system. You can download it from [python.org]

(<https://www.python.org/downloads/>).

2. **Setup:**

- Create a directory for your project:

```bash
mkdir my_project
cd my_project
```
- Save the `simplegit.py` script into this directory.
3. **Make the Script Executable (Optional for UNIX-based systems):**
```bash
chmod +x simplegit.py
```
4. **Adding to PATH (Optional):**
- To use `simplegit` from anywhere, you can add it to your system's PATH or create an alias. For example, on UNIXbased
systems:
```bash
alias simplegit='python3 /path/to/simplegit.py'
```
- Add the above line to your `.bashrc` or `.zshrc` file.
### Commands
#### `init`
**Description:** Initializes a new SimpleGit repository in the current directory.
**Usage:**
```bash
python3 simplegit.py init
```
*Or if made executable:*
```bash
./simplegit.py init
```
**Output:**
```
Initialized empty SimpleGit repository in /path/to/my_project/.simplegit
```
#### `commit`
**Description:** Commits the current state of the project with a title and an optional description.
**Usage:**
```bash
python3 simplegit.py commit -m "Initial commit" -d "Set up project structure."
```
*Or if made executable:*
```bash
./simplegit.py commit -m "Initial commit" -d "Set up project structure."
```
**Arguments:**
- `-m, --title` (required): The title of the commit.
- `-d, --description` (optional): A detailed description of the commit.
**Output:**
```
Committed changes as 'Initial commit'.
```
#### `log`
**Description:** Displays the history of all commits.
**Usage:**
```bash
python3 simplegit.py log
```
*Or if made executable:*
```bash
./simplegit.py log
```
**Output:**
```
Commit: Initial commit
Date: 2023-10-05 14:23:45
Description: Set up project structure.
Commit: Add feature X
Date: 2023-10-06 09:15:30
Description: Implemented feature X with functionalities A and B.
```

#### `status`
**Description:** Shows the changes made since the last commit.
**Usage:**

```bash
python3 simplegit.py status

```

*Or if made executable:*

```bash
./simplegit.py status

```

**Output:**


```

Changes since last commit:
Modified: main.py
Added: utils.py

```

**Note:** If no changes are detected:

```

No changes since the last commit.

```

## Documentation

### Initialization (`init`)

The `init` command sets up a new local repository in your current working directory. It creates a hidden `.simplegit`
directory containing a `logs` folder and a `config.json` file to store configurations.
**Example:**

```bash

python3 simplegit.py init
```

### Committing Changes (`commit`)

Use the `commit` command to save the current state of your project. Each commit is saved as a separate folder within
the `logs` directory, containing copies of all project files at the time of the commit. Commit metadata such as title,
timestamp, and description are stored in `commit_info.json`.
**Example:**

```bash
python3 simplegit.py commit -m "Add new feature" -d "Implemented the user authentication feature."
```

### Viewing Logs (`log`)

The `log` command displays a list of all commits in reverse chronological order. Each entry shows the commit title, date,
and description.
**Example:**
```bash

python3 simplegit.py log
```

### Checking Status (`status`)

The `status` command compares the current state of your project with the latest commit, listing any added or modified
files.
**Example:**

```bash
python3 simplegit.py status
```
