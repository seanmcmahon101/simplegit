# SimpleGit: A Beginner-Friendly Local Version Control System

SimpleGit is designed for beginners and small projects (though it works well for larger projects too). It's a local version
control system that's easy to use and doesn't require cloud integration. Perfect for those new to version control!

## Features

- Easy to use with short command aliases
- Local storage (no cloud integration required)
- Multiple backup locations
- Branching support
- Commit tagging
- Diff viewing between commits
- Automatic backups
- 
## Detailed Installation Guide

### Step 1: Obtain SimpleGit

#### Option A: Cloning the Repository, works if you ironically have Git installed, if not refer to option B
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to store SimpleGit.
3. Run the following command:
   
   ```
   git clone https://github.com/yourusername/SimpleGit.git
   ```

#### Option B: Downloading the ZIP file

1. Go to the SimpleGit GitHub repository.
2. Click on the "Code" button and select "Download ZIP".
3. Once downloaded, extract the ZIP file to your desired location.

### Step 2: Add SimpleGit to System PATH

Adding SimpleGit to your system PATH allows you to run it from any directory in the terminal.

#### For Windows:

1. Right-click on "This PC" or "My Computer" and select "Properties".
2. Click on "Advanced system settings".
3. Click the "Environment Variables" button.
4. Under "System variables", find and select the "Path" variable, then click "Edit".
5. Click "New" and add the full path to the SimpleGit folder (e.g., C:\Users\YourUsername\SimpleGit).
6. Click "OK" to close all dialog boxes.

#### For macOS and Linux:

1. Open your terminal.
2. Open your shell configuration file (e.g., ~/.bash_profile, ~/.zshrc) in a text editor:
   
   ```
   nano ~/.bash_profile
   ```
   
4. Add the following line at the end of the file, replacing the path with your SimpleGit folder location:
   
   ```
   export PATH=$PATH:/path/to/SimpleGit
   ```
   
6. Save the file and exit the editor.
   
8. Reload your shell configuration:
   
   ```
   source ~/.bash_profile
   ```

### Note: Why Use a Batch File on Windows?

Windows doesn't have a built-in way to associate file extensions with command-line interpreters. When you type a command in the terminal, Windows looks for executable files (.exe, .com, .bat, etc.) in the directories listed in the PATH environment variable.

Python files (.py) are not directly executable on Windows. By creating a batch file with the same name as our Python script, we provide Windows with an executable file it can find and run. The batch file then calls Python to execute our actual script. Essentially, its a work around.

### Step 2: Verify Installation

1. Open a new terminal or command prompt (this is important to load the updated PATH).
2. Type `simplegit -h` and press Enter.
3. If everything is set up correctly, you should see the help message for SimpleGit.
## Basic Commands
Here are some basic commands to get you started:
### Initialize a Repository
```
simplegit init
```
or
```
simplegit i
```
This creates a new SimpleGit repository in your current folder.
### Commit Changes
```
simplegit commit -m "Your commit message" -d "Optional description"
```
or
```
simplegit c -m "Your commit message" -d "Optional description"
```
This saves your current changes with a message and optional description.
### View Commit History
```
simplegit log
```
or
```
simplegit lg
```
This shows you a list of all your commits.
### Check Repository Status
```
simplegit status
```
or
```
simplegit st
```
This tells you what files have changed since your last commit.
### Pull from a Specific Commit
```
simplegit pull -c "CommitID"
```
or
```
simplegit p -c "CommitID"
```
This retrieves the state of your project from a specific commit.
### Automatic Backup
```
simplegit backup -t 300 -m "Auto backup"
```
or
```
simplegit b -t 300 -m "Auto backup"
```
This starts an automatic backup every 5 minutes (300 seconds).
## Advanced Features AKA The really fun stuff
### Managing Backup Locations
Add a backup location:
```
simplegit backup-loc add /path/to/backup
```
Remove a backup location:
```
simplegit backup-loc remove /path/to/backup
```
List all backup locations:
```
simplegit backup-loc list
```
### Working with Branches
Create a new branch:
```
simplegit branch create feature-name
```
Switch to a branch:
```
simplegit branch switch feature-name
```
List all branches:
```
simplegit branch list
```
Merge a branch:
```
simplegit branch merge feature-name
```
### Tagging Commits
Add a tag to a commit:
```
simplegit tag add CommitID tag-name
```
List all tags:
```
simplegit tag list
```
### Viewing Differences Between Commits
```
simplegit diff CommitID1 CommitID2
```
## Getting Help
For more information on any command, use the -h or --help option:
```
simplegit -h
```
## Tips for Beginners
1. Start by initializing a repository in your project folder.
2. Commit often! Every time you make a significant change or finish a feature, make a commit.
3. Use meaningful commit messages to describe what you've changed.
4. Check the status regularly to see what files have been modified.
5. Use branches when you're working on new features or experiments.
6. Don't be afraid to make mistakes becasue I do and I made the thing!

