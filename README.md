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
## Installation
1. Make sure you have python installed
2. Make sure the requirements is installed, currently just argsparse
3. Clone the repo or download the zip file
4. Place the SimpleGit folder wherever you'd like on your computer
5. Add the folder path to your system's PATH variable
6. Restart your terminal or command prompt
7. You're ready to go!
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
6. Don't be afraid to make mistakes - you can always go back to a previous commit!
Enjoy using SimpleGit for your projects! Remember, practice makes perfect. The more you use version control, the
more natural it will become.
```
