import os
import sys
import argparse
import shutil
import json
import time
from datetime import datetime
import filecmp
import difflib
from pathlib import Path

try:
  import readline 
except ImportError:
  pass 

REPO_DIR = ".simplegit"
LOGS_DIR = "logs"
CONFIG_FILE = "config.json"
BRANCHES_DIR = "branches"
TAGS_DIR = "tags"
MASTER_BRANCH = "main"

def log(message):
  """Logs messages to a log file within the repository."""
  repo_path = get_repo_path()
  log_file = os.path.join(repo_path, "simplegit.log")
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(log_file, "a") as lf:
      lf.write(f"[{timestamp}] {message}\n")

def get_repo_path():
  """Returns the absolute path to the repository directory."""
  return os.path.join(os.getcwd(), REPO_DIR)

def get_logs_path():
  """Returns the absolute path to the logs directory."""
  return os.path.join(get_repo_path(), LOGS_DIR)

def get_config_path():
  """Returns the absolute path to the config file."""
  return os.path.join(get_repo_path(), CONFIG_FILE)

def get_branches_path():
  """Returns the absolute path to the branches directory."""
  return os.path.join(get_repo_path(), BRANCHES_DIR)

def get_tags_path():
  """Returns the absolute path to the tags directory."""
  return os.path.join(get_repo_path(), TAGS_DIR)

def init_repository(args):
  """Initializes a new local repository."""
  repo_path = get_repo_path()
  if os.path.exists(repo_path):
      print("Repository already initialized.")
      return
  os.makedirs(get_logs_path())
  os.makedirs(get_branches_path())
  os.makedirs(get_tags_path())
  config = {
      "logs_directory": get_logs_path(),
      "backup_locations": [],  
      "current_branch": MASTER_BRANCH,
      "branches": {
          MASTER_BRANCH: []  
      },
      "tags": {} 
  }
  with open(get_config_path(), 'w') as config_file:
      json.dump(config, config_file, indent=4)
  with open(os.path.join(get_branches_path(), MASTER_BRANCH + ".json"), 'w') as branch_file:
      json.dump([], branch_file, indent=4)
  log("Initialized a new SimpleGit repository.")
  print(f"Initialized empty SimpleGit repository in {repo_path}")

def load_config():
  """Loads the repository configuration."""
  config_path = get_config_path()
  if not os.path.exists(config_path):
      print("Configuration not found. Have you initialized the repository?")
      sys.exit(1)
  with open(config_path, 'r') as config_file:
      return json.load(config_file)

def save_config(config):
  """Saves the repository configuration."""
  with open(get_config_path(), 'w') as config_file:
      json.dump(config, config_file, indent=4)

def commit_changes(args):
  """Commits the current state of the repository."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  current_branch = config.get("current_branch", MASTER_BRANCH)
  branches = config.get("branches", {MASTER_BRANCH: []})

  if not os.path.exists(get_repo_path()):
      print("Repository not initialized. Please run 'init' first.")
      sys.exit(1)

  if not has_changes(logs_dir, current_branch):
      print("No changes detected since the last commit.")
      return

  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  unique_id = timestamp  
  commit_title = args.title.replace(' ', '_')
  commit_dir_name = f"{unique_id}_{commit_title}"
  commit_path = os.path.join(logs_dir, commit_dir_name)
  os.makedirs(commit_path)

  for item in os.listdir(os.getcwd()):
      if item == REPO_DIR:
          continue
      s = os.path.join(os.getcwd(), item)
      d = os.path.join(commit_path, item)
      try:
          if os.path.isdir(s):
              shutil.copytree(s, d, symlinks=True)
          else:
              shutil.copy2(s, d)
      except Exception as e:
          print(f"Failed to copy {s} to {d}: {e}")
          log(f"Error copying {s} to {d}: {e}")

  commit_info = {
      "id": unique_id,
      "title": args.title,
      "timestamp": timestamp,
      "description": args.description if args.description else "",
      "branch": current_branch
  }
  with open(os.path.join(commit_path, "commit_info.json"), 'w') as info_file:
      json.dump(commit_info, info_file, indent=4)

  branches[current_branch].append(unique_id)
  config["branches"] = branches
  save_config(config)
  log(f"Committed changes: {commit_dir_name} on branch {current_branch}")
  handle_backups(config, commit_path)
  print(f"Committed changes as '{args.title}' with ID {unique_id} on branch '{current_branch}'.")

def has_changes(logs_dir, current_branch):
  """Checks if there are changes to commit."""
  if not os.path.exists(logs_dir):
      return True 
  branch_commits = get_branch_commits(current_branch)
  if not branch_commits:
      return True  
  latest_commit = os.path.join(logs_dir, f"{branch_commits[-1]}_*")
  commits = sorted([c for c in os.listdir(logs_dir) if c.startswith(branch_commits[-1])], reverse=True)
  if not commits:
      return True
  latest_commit_path = os.path.join(logs_dir, commits[0])
  for item in os.listdir(os.getcwd()):
      if item == REPO_DIR:
          continue
      current_path = os.path.join(os.getcwd(), item)
      commit_path = os.path.join(latest_commit_path, item)
      if not os.path.exists(commit_path):
          return True 
      if os.path.isdir(current_path):
          if not filecmp.dircmp(current_path, commit_path).left_only and not filecmp.dircmp(current_path, commit_path).right_only:
              continue  
          else:
              return True
      else:
          if not filecmp.cmp(current_path, commit_path, shallow=False):
              return True  
  return False 

def handle_backups(config, commit_path):
  """Handles backing up the commit to additional locations."""
  backup_locations = config.get("backup_locations", [])
  if not backup_locations:
      return  
  for backup_dir in backup_locations:
      if not os.path.exists(backup_dir):
          try:
              os.makedirs(backup_dir)
              log(f"Created backup directory: {backup_dir}")
          except Exception as e:
              print(f"Failed to create backup directory {backup_dir}: {e}")
              log(f"Error creating backup directory {backup_dir}: {e}")
              continue
      destination = os.path.join(backup_dir, os.path.basename(commit_path))
      try:
          if os.path.exists(destination):
              shutil.rmtree(destination)
          shutil.copytree(commit_path, destination, symlinks=True)
          log(f"Backed up commit to {destination}")
      except Exception as e:
          print(f"Failed to backup to {backup_dir}: {e}")
          log(f"Error backing up to {backup_dir}: {e}")

def view_logs(args):
  """Displays the commit logs."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  current_branch = config.get("current_branch", MASTER_BRANCH)

  if not os.path.exists(logs_dir):
      print("No commits found.")
      return

  branch_commits = get_branch_commits(current_branch)
  if not branch_commits:
      print("No commits found on the current branch.")
      return

  print(f"--- Commit Logs for Branch '{current_branch}' ---\n")
  for commit_id in reversed(branch_commits):
      commit_dirs = [d for d in os.listdir(logs_dir) if d.startswith(commit_id)]
      if not commit_dirs:
          continue
      commit_dir = commit_dirs[0]
      commit_path = os.path.join(logs_dir, commit_dir)
      info_path = os.path.join(commit_path, "commit_info.json")
      if not os.path.exists(info_path):
          continue
      with open(info_path, 'r') as info_file:
          commit_info = json.load(info_file)
      timestamp = datetime.strptime(commit_info["timestamp"], "%Y%m%d%H%M%S")
      readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
      print(f"Commit ID : {commit_info['id']}")
      print(f"Title     : {commit_info['title']}")
      print(f"Date      : {readable_time}")
      print(f"Description: {commit_info['description']}\n")

def get_branch_commits(branch):
  """Retrieves the list of commit IDs for a given branch."""
  config = load_config()
  branches = config.get("branches", {})
  return branches.get(branch, [])

def check_status(args):
  """Checks the status of the repository."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  current_branch = config.get("current_branch", MASTER_BRANCH)

  if not os.path.exists(logs_dir):
      print("No commits to compare with.")
      return

  branch_commits = get_branch_commits(current_branch)
  if not branch_commits:
      print("No commits on the current branch.")
      return
  latest_commit_id = branch_commits[-1]
  commit_dirs = [d for d in os.listdir(logs_dir) if d.startswith(latest_commit_id)]
  if not commit_dirs:
      print("Latest commit data missing.")
      return
  latest_commit_path = os.path.join(logs_dir, commit_dirs[0])

  changes = []
  for item in os.listdir(os.getcwd()):
      if item == REPO_DIR:
          continue
      current_path = os.path.join(os.getcwd(), item)
      commit_path = os.path.join(latest_commit_path, item)
      if not os.path.exists(commit_path):
          changes.append(f"Added: {item}")
      elif os.path.isdir(current_path):
          if len(os.listdir(current_path)) != len(os.listdir(commit_path)):
              changes.append(f"Modified: {item}/")
      else:
          if not filecmp.cmp(current_path, commit_path, shallow=False):
              changes.append(f"Modified: {item}")

  if changes:
      print("Changes since last commit:")
      for change in changes:
          print(f"  {change}")
  else:
      print("No changes since the last commit.")

def pull_commit(args):
  """Pulls code from a specific commit."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  current_branch = config.get("current_branch", MASTER_BRANCH)

  if not os.path.exists(logs_dir):
      print("No commits found.")
      return

  commits = get_branch_commits(current_branch)
  if args.commit not in commits:
      print(f"No commit found with ID '{args.commit}' on branch '{current_branch}'.")
      return

  commit_id = args.commit
  commit_dirs = [d for d in os.listdir(logs_dir) if d.startswith(commit_id)]
  if not commit_dirs:
      print(f"Commit data missing for ID '{commit_id}'.")
      return

  commit_path = os.path.join(logs_dir, commit_dirs[0])
  print(f"Pulling code from commit '{commit_id}'...")
  
  confirmation = input("This will overwrite existing files in the working directory. Proceed? (y/n): ")
  if confirmation.lower() != 'y':
      print("Pull aborted.")
      return

  for item in os.listdir(commit_path):
      if item == "commit_info.json":
          continue
      s = os.path.join(commit_path, item)
      d = os.path.join(os.getcwd(), item)
      try:
          if os.path.isdir(s):
              if os.path.exists(d):
                  shutil.rmtree(d)
              shutil.copytree(s, d, symlinks=True)
          else:
              shutil.copy2(s, d)
      except Exception as e:
          print(f"Failed to copy {s} to {d}: {e}")
          log(f"Error copying {s} to {d}: {e}")

  log(f"Pulled commit '{commit_id}' to working directory.")
  print("Pull complete. Your working directory has been updated.")

def backup_changes(args):
  """Automatically commits changes every x amount of time."""
  interval = args.time
  print(f"Starting automatic backup every {interval} seconds. Press Ctrl+C to stop.")
  try:
      while True:
          if has_changes(load_config()['logs_directory'], load_config()['current_branch']):
              commit_args = argparse.Namespace(
                  title=f"{args.title} {datetime.now().strftime('%Y-%m-%d %H_%M_%S')}",
                  description="Automatic backup"
              )
              commit_changes(commit_args)
          else:
              print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No changes detected. Skipping backup.")
          time.sleep(interval)
  except KeyboardInterrupt:
      print("\nBackup stopped by user.")
      log("Automatic backup process terminated by user.")

def add_backup_location(args):
  """Adds a new backup location."""
  config = load_config()
  backup_dir = os.path.abspath(args.location)
  if not os.path.exists(backup_dir):
      try:
          os.makedirs(backup_dir)
          print(f"Created backup directory at {backup_dir}")
          log(f"Created backup directory at {backup_dir}")
      except Exception as e:
          print(f"Failed to create backup directory {backup_dir}: {e}")
          log(f"Error creating backup directory {backup_dir}: {e}")
          return
  if backup_dir in config.get("backup_locations", []):
      print("Backup location already exists.")
      return
  config.setdefault("backup_locations", []).append(backup_dir)
  save_config(config)
  print(f"Added backup location: {backup_dir}")
  log(f"Added backup location: {backup_dir}")

def remove_backup_location(args):
  """Removes an existing backup location."""
  config = load_config()
  backup_dir = os.path.abspath(args.location)
  if backup_dir not in config.get("backup_locations", []):
      print("Backup location not found in configuration.")
      return
  config["backup_locations"].remove(backup_dir)
  save_config(config)
  print(f"Removed backup location: {backup_dir}")
  log(f"Removed backup location: {backup_dir}")

def list_backup_locations(args):
  """Lists all configured backup locations."""
  config = load_config()
  backup_locations = config.get("backup_locations", [])
  if not backup_locations:
      print("No backup locations configured.")
      return
  print("--- Backup Locations ---")
  for idx, loc in enumerate(backup_locations, start=1):
      print(f"{idx}. {loc}")

def branch_init(args):
  """Creates a new branch."""
  config = load_config()
  branch_name = args.name
  branches = config.get("branches", {})
  if branch_name in branches:
      print(f"Branch '{branch_name}' already exists.")
      return
  branches[branch_name] = []
  config["branches"] = branches
  with open(os.path.join(get_branches_path(), branch_name + ".json"), 'w') as branch_file:
      json.dump([], branch_file, indent=4)
  save_config(config)
  print(f"Created new branch '{branch_name}'.")
  log(f"Created new branch '{branch_name}'.")

def branch_switch(args):
  """Switches to an existing branch."""
  config = load_config()
  branch_name = args.name
  branches = config.get("branches", {})
  if branch_name not in branches:
      print(f"Branch '{branch_name}' does not exist.")
      return
  config["current_branch"] = branch_name
  save_config(config)
  print(f"Switched to branch '{branch_name}'.")
  log(f"Switched to branch '{branch_name}'.")

def view_branches(args):
  """Lists all branches."""
  config = load_config()
  current_branch = config.get("current_branch", MASTER_BRANCH)
  branches = config.get("branches", {})
  print("--- Branches ---")
  for branch in branches:
      if branch == current_branch:
          print(f"* {branch}")
      else:
          print(f"  {branch}")

def diff_commits(args):
  """Shows differences between two commits."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  commit1 = args.commit1
  commit2 = args.commit2

  commit_dirs1 = [d for d in os.listdir(logs_dir) if d.startswith(commit1)]
  commit_dirs2 = [d for d in os.listdir(logs_dir) if d.startswith(commit2)]
  if not commit_dirs1:
      print(f"No commit found with ID '{commit1}'.")
      return
  if not commit_dirs2:
      print(f"No commit found with ID '{commit2}'.")
      return

  path1 = os.path.join(logs_dir, commit_dirs1[0])
  path2 = os.path.join(logs_dir, commit_dirs2[0])

  for root, dirs, files in os.walk(path1):
      rel_path = os.path.relpath(root, path1)
      path2_root = os.path.join(path2, rel_path)
      for file in files:
          file1 = os.path.join(root, file)
          file2 = os.path.join(path2_root, file)
          if os.path.exists(file2):
              with open(file1, 'r', errors='ignore') as f1, open(file2, 'r', errors='ignore') as f2:
                  diff = difflib.unified_diff(
                      f1.readlines(),
                      f2.readlines(),
                      fromfile=f"{commit1}/{rel_path}/{file}",
                      tofile=f"{commit2}/{rel_path}/{file}",
                      lineterm=''
                  )
                  for line in diff:
                      print(line)
          else:
              print(f"File '{file}' removed in commit '{commit2}'.")

def tag_commit(args):
  """Tags a specific commit."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())
  commit_id = args.commit
  tag_name = args.tag

  commit_dirs = [d for d in os.listdir(logs_dir) if d.startswith(commit_id)]
  if not commit_dirs:
      print(f"No commit found with ID '{commit_id}'.")
      return

  tags = config.get("tags", {})
  if tag_name in tags:
      print(f"Tag '{tag_name}' already exists.")
      return

  tags[tag_name] = commit_id
  config["tags"] = tags
  save_config(config)

  with open(os.path.join(get_tags_path(), f"{tag_name}.json"), 'w') as tag_file:
      json.dump({"commit_id": commit_id}, tag_file, indent=4)

  print(f"Tagged commit '{commit_id}' as '{tag_name}'.")
  log(f"Tagged commit '{commit_id}' as '{tag_name}'.")

def list_tags(args):
  """Lists all tags."""
  config = load_config()
  tags = config.get("tags", {})
  if not tags:
      print("No tags have been created.")
      return
  print("--- Tags ---")
  for tag, commit in tags.items():
      print(f"{tag}: {commit}")

def branch_merge(args):
  """Merges a specified branch into the current branch."""
  config = load_config()
  current_branch = config.get("current_branch", MASTER_BRANCH)
  target_branch = args.name
  branches = config.get("branches", {})

  if target_branch not in branches:
      print(f"Branch '{target_branch}' does not exist.")
      return
  if target_branch == current_branch:
      print("Cannot merge a branch into itself.")
      return

  current_commits = branches[current_branch]
  target_commits = branches[target_branch]
  if not target_commits:
      print(f"Branch '{target_branch}' has no commits to merge.")
      return
  latest_target_commit_id = target_commits[-1]
  logs_dir = config.get("logs_directory", get_logs_path())
  commit_dirs = [d for d in os.listdir(logs_dir) if d.startswith(latest_target_commit_id)]
  if not commit_dirs:
      print(f"Commit data missing for ID '{latest_target_commit_id}'.")
      return
  target_commit_path = os.path.join(logs_dir, commit_dirs[0])

  print(f"Merging branch '{target_branch}' into '{current_branch}'...")
  for item in os.listdir(target_commit_path):
      if item == "commit_info.json":
          continue
      s = os.path.join(target_commit_path, item)
      d = os.path.join(os.getcwd(), item)
      try:
          if os.path.isdir(s):
              if os.path.exists(d):
                  shutil.rmtree(d)
              shutil.copytree(s, d, symlinks=True)
          else:
              shutil.copy2(s, d)
      except Exception as e:
          print(f"Failed to merge {s} to {d}: {e}")
          log(f"Error merging {s} to {d}: {e}")

  merge_commit_title = f"Merge branch '{target_branch}' into '{current_branch}'"
  merge_commit_args = argparse.Namespace(
      title=merge_commit_title,
      description=f"Merged branch '{target_branch}' into '{current_branch}'"
  )
  commit_changes(merge_commit_args)
  print(f"Successfully merged '{target_branch}' into '{current_branch}'.")
  log(f"Merged branch '{target_branch}' into '{current_branch}'.")

def main():
  parser = argparse.ArgumentParser(
      description="SimpleGit: An Advanced Beginner-Friendly Local Version Control System",
      formatter_class=argparse.RawTextHelpFormatter
  )
  """
  The below is just evil, i dont apologise
  """
  subparsers = parser.add_subparsers(title="Commands", dest="command")
  parser_init = subparsers.add_parser('init', aliases=['i'], help='Initialize a new repository')
  parser_commit = subparsers.add_parser('commit', aliases=['c'], help='Commit current changes')
  parser_commit.add_argument('-m', '--title', required=True, help='Commit title')
  parser_commit.add_argument('-d', '--description', help='Commit description')
  parser_log = subparsers.add_parser('log', aliases=['lg'], help='Show commit logs')
  parser_status = subparsers.add_parser('status', aliases=['st'], help='Show status of repository')
  parser_pull = subparsers.add_parser('pull', aliases=['p'], help='Pull code from a specific commit')
  parser_pull.add_argument('-c', '--commit', required=True, help='Commit ID to pull from')
  parser_backup = subparsers.add_parser('backup', aliases=['b'], help='Automatically commit changes every x seconds')
  parser_backup.add_argument('-t', '--time', type=int, required=True, help='Time interval in seconds between backups')
  parser_backup.add_argument('-m', '--title', default="Auto backup", help='Commit title for backups')
  backup_loc = subparsers.add_parser('backup-loc', help='Manage backup locations')
  backup_loc_sub = backup_loc.add_subparsers(title="Backup Location Commands", dest="backup_command")
  backup_add = backup_loc_sub.add_parser('add', help='Add a new backup location')
  backup_add.add_argument('location', help='Path to the backup directory')
  backup_remove = backup_loc_sub.add_parser('remove', help='Remove an existing backup location')
  backup_remove.add_argument('location', help='Path to the backup directory to remove')
  backup_list = backup_loc_sub.add_parser('list', help='List all backup locations')
  branch = subparsers.add_parser('branch', help='Manage branches')
  branch_sub = branch.add_subparsers(title="Branch Commands", dest="branch_command")
  branch_create = branch_sub.add_parser('create', help='Create a new branch')
  branch_create.add_argument('name', help='Name of the new branch')
  branch_switch_cmd = branch_sub.add_parser('switch', help='Switch to an existing branch')
  branch_switch_cmd.add_argument('name', help='Name of the branch to switch to')
  branch_list = branch_sub.add_parser('list', help='List all branches')
  branch_merge_cmd = branch_sub.add_parser('merge', help='Merge a branch into the current branch')
  branch_merge_cmd.add_argument('name', help='Name of the branch to merge into the current branch')
  parser_diff = subparsers.add_parser('diff', help='Show differences between two commits')
  parser_diff.add_argument('commit1', help='First commit ID')
  parser_diff.add_argument('commit2', help='Second commit ID')
  tag = subparsers.add_parser('tag', help='Manage tags')
  tag_sub = tag.add_subparsers(title="Tag Commands", dest="tag_command")
  tag_add = tag_sub.add_parser('add', help='Tag a specific commit')
  tag_add.add_argument('commit', help='Commit ID to tag')
  tag_add.add_argument('tag', help='Tag name')
  tag_list = tag_sub.add_parser('list', help='List all tags')
  parser_merge = subparsers.add_parser('merge', help='Merge a branch into the current branch')
  parser_merge.add_argument('name', help='Name of the branch to merge into the current branch')
  args = parser.parse_args()

  if args.command in ['init', 'i']:
      init_repository(args)
  elif args.command in ['commit', 'c']:
      commit_changes(args)
  elif args.command in ['log', 'lg']:
      view_logs(args)
  elif args.command in ['status', 'st']:
      check_status(args)
  elif args.command in ['pull', 'p']:
      pull_commit(args)
  elif args.command == 'backup':
      backup_changes(args)
  elif args.command == 'backup-loc':
      if args.backup_command == 'add':
          add_backup_location(args)
      elif args.backup_command == 'remove':
          remove_backup_location(args)
      elif args.backup_command == 'list':
          list_backup_locations(args)
      else:
          print_help_backup_loc()
  elif args.command == 'branch':
      if args.branch_command == 'create':
          branch_init(args)
      elif args.branch_command == 'switch':
          branch_switch(args)
      elif args.branch_command == 'list':
          view_branches(args)
      elif args.branch_command == 'merge':
          branch_merge(args)
      else:
          print_help_branch()
  elif args.command == 'diff':
      diff_commits(args)
  elif args.command == 'tag':
      if args.tag_command == 'add':
          tag_commit(args)
      elif args.tag_command == 'list':
          list_tags(args)
      else:
          print_help_tag()
  else:
      parser.print_help()

def print_help_backup_loc():
  """Prints help for backup location management."""
  help_text = """
Backup Location Management Commands:

backup-loc add <location>        Add a new backup location.
backup-loc remove <location>     Remove an existing backup location.
backup-loc list                  List all configured backup locations.
"""
  print(help_text)

def print_help_branch():
  """Prints help for branch management."""
  help_text = """
Branch Management Commands:

branch create <name>             Create a new branch.
branch switch <name>             Switch to an existing branch.
branch list                      List all branches.
branch merge <name>              Merge a branch into the current branch.
"""
  print(help_text)

def print_help_tag():
  """Prints help for tag management."""
  help_text = """
Tag Management Commands:

tag add <commit> <tag>           Tag a specific commit.
tag list                         List all tags.
"""
  print(help_text)

if __name__ == "__main__":
  main()
