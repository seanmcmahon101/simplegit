# SimpleGit

SimpleGit is a beginner-friendly local version control system designed to help newcomers understand the basics of version control without the complexities of distributed systems. It provides essential functionalities for tracking changes, creating commits, and managing your project's history, all while keeping everything local on your machine.

## Features

- **Easy Initialization**: Quickly set up a new repository with a simple command.
- **Local Commits**: Save snapshots of your project without the need for a remote server.
- **Commit Logs**: View a history of all your commits with timestamps and descriptions.
- **Status Checking**: See what files have been modified since your last commit.
- **Commit Pulling**: Restore your project to any previous commit state.
- **Automatic Backups**: Set up timed automatic commits to safeguard your work.
- **User-Friendly Commands**: Intuitive command structure with short aliases for quick typing.

## Installation

1. Ensure you have Python 3.7 or later installed on your system.
2. Download the `simplegit.py` script to your local machine.
3. Make the script executable:
   ```
   chmod +x simplegit.py
   ```
4. (Optional) Add the script's directory to your PATH for easier access.

## Usage

Here are some common usage examples:

### Initialize a Repository
```
python simplegit.py init
# or
python simplegit.py i
```

### Commit Changes
```
python simplegit.py commit -m "Initial commit" -d "Added project files"
# or
python simplegit.py c -m "Initial commit" -d "Added project files"
```

### View Commit Logs
```
python simplegit.py log
# or
python simplegit.py lg
```

### Check Repository Status
```
python simplegit.py status
# or
python simplegit.py st
```

### Pull from a Specific Commit
```
python simplegit.py pull -c "20231012123456_Initial_commit"
# or
python simplegit.py p -c "Initial_commit"
```

### Set Up Automatic Backups
```
python simplegit.py backup -t 300 -m "Auto backup"
# or
python simplegit.py b -t 300 -m "Auto backup"
```

## Contributing

We welcome contributions to SimpleGit! Here's how you can help:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Submit a pull request with a clear description of your changes.

Please ensure your code adheres to the existing style and includes appropriate comments.

## License

SimpleGit is released under the MIT License. See the LICENSE file for more details.

## Contact

If you have any questions or suggestions, please dont contact :)
