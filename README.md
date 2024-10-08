### Installation
1. **Prerequisites:**
- Ensure you have Python 3 installed on your system. You can download it from [python.org]
(https://www.python.org/downloads/).
2. **Setup:**
- Create a directory for your project:
```bash
mkdir my_project
cd my_project
```
- Save the `simplegit.py` script into this directory.
3. **Adding to PATH:**
- To use `simplegit` from anywhere, add the script's directory to your system's PATH:
For Unix-based systems (Linux, macOS), add this line to your `.bashrc` or `.zshrc` file:
```bash
export PATH=$PATH:/path/to/my_project
```
For Windows, you can add the script's directory to the system PATH through the Environment Variables settings.
- Alternatively, create an alias (Unix-based systems):
```bash
alias simplegit='python3 /path/to/my_project/simplegit.py'
```
Add this line to your `.bashrc` or `.zshrc` file.
### Commands
#### `init`
Initializes a new SimpleGit repository in the current directory.
```bash
simplegit init
```
#### `commit`
Commits the current state of the project with a title and an optional description.
```bash
simplegit commit -m "Commit title" -d "Commit description"
```
#### `log`
Displays the history of all commits.
```bash
simplegit log
```
#### `status`
Shows the changes made since the last commit.
```bash
simplegit status
```
### Documentation
