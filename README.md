# SimpleGit

## Git for idiots, for if cloud computing P&!£%S you off

I hate typing repetitive stuff so this was created, all commands have shortened versions for speed. This is designed to be beginner friendly, so if youve never used VCS before this is  good starting point. Also, this doesnt use cloud intergration, I wanted this to be as simple as possible. Enjoy!


## Installation

1. Clone the Repo, or download the zip and place wherever youd like
2. Place the folder path of the repo into your PATH variable
3. Its best to restart your env at this point
4. You should be good to go

## Commands

After adding SimpleGit to your PATH, you can use the following commands:

1. Initialize a repository:
   ```
   simplegit init
   ```
   or
   ```
   simplegit i
   ```

2. Commit changes:
   ```
   simplegit commit -m "Commit message" -d "Optional description"
   ```
   or
   ```
   simplegit c -m "Commit message" -d "Optional description"
   ```

3. View commit logs:
   ```
   simplegit log
   ```
   or
   ```
   simplegit lg
   ```

4. Check repository status:
   ```
   simplegit status
   ```
   or
   ```
   simplegit st
   ```

5. Pull code from a specific commit:
   ```
   simplegit pull -c "CommitIdentifier"
   ```
   or
   ```
   simplegit p -c "CommitIdentifier"
   ```

6. Automatic backup:
   ```
   simplegit backup -t 300 -m "Auto backup"
   ```
   or
   ```
   simplegit b -t 300 -m "Auto backup"
   ```

## Usage Examples

- Initialize a new repository:
  ```
  simplegit init
  ```

- Commit changes:
  ```
  simplegit commit -m "Initial commit" -d "Added project files"
  ```

- View commit history:
  ```
  simplegit log
  ```

- Check current status:
  ```
  simplegit status
  ```

- Pull from a specific commit:
  ```
  simplegit pull -c "20231012123456_Initial_commit"
  ```

- Start automatic backup every 5 minutes:
  ```
  simplegit backup -t 300 -m "Auto backup"
  ```

For more detailed information on each command, use the `-h` or `--help` option:
```
simplegit <command> -h
```

Enjoy using SimpleGit for your local version control needs!
