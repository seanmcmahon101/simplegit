#!/usr/bin/env python3
"""
SimpleGit: A Beginner-Friendly Local Version Control System

This script provides basic version control functionalities such as initializing
a repository, committing changes, viewing logs, and checking the status of the repository.
All changes are stored locally without any cloud integrations.
"""

import os
import sys
import argparse
import shutil
import json
import time
from datetime import datetime
import filecmp

# Constants for repository
REPO_DIR = ".simplegit"
LOGS_DIR = "logs"
CONFIG_FILE = "config.json"


def get_repo_path():
  """Returns the absolute path to the repository directory."""
  return os.path.join(os.getcwd(), REPO_DIR)


def get_logs_path():
  """Returns the absolute path to the logs directory."""
  return os.path.join(get_repo_path(), LOGS_DIR)


def get_config_path():
  """Returns the absolute path to the config file."""
  return os.path.join(get_repo_path(), CONFIG_FILE)


def init_repository(args):
  """Initializes a new local repository."""
  repo_path = get_repo_path()
  if os.path.exists(repo_path):
      print("Repository already initialized.")
      return
  os.makedirs(get_logs_path())
  # Create a default config
  config = {
      "logs_directory": get_logs_path()
  }
  with open(get_config_path(), 'w') as config_file:
      json.dump(config, config_file, indent=4)
  print(f"Initialized empty SimpleGit repository in {repo_path}")


def load_config():
  """Loads the repository configuration."""
  config_path = get_config_path()
  if not os.path.exists(config_path):
      print("Configuration not found. Have you initialized the repository?")
      sys.exit(1)
  with open(config_path, 'r') as config_file:
      return json.load(config_file)


def commit_changes(args):
  """Commits the current state of the repository."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())

  if not os.path.exists(get_repo_path()):
      print("Repository not initialized. Please run 'init' first.")
      sys.exit(1)

  # Create a new commit directory with timestamp
  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  commit_title = args.title.replace(' ', '_')
  commit_dir_name = f"{timestamp}_{commit_title}"
  commit_path = os.path.join(logs_dir, commit_dir_name)
  os.makedirs(commit_path)

  # Copy all files and directories except the .simplegit directory
  for item in os.listdir(os.getcwd()):
      if item == REPO_DIR:
          continue
      s = os.path.join(os.getcwd(), item)
      d = os.path.join(commit_path, item)
      if os.path.isdir(s):
          shutil.copytree(s, d, ignore=shutil.ignore_patterns(REPO_DIR))
      else:
          shutil.copy2(s, d)

  # Save commit message
  commit_info = {
      "title": args.title,
      "timestamp": timestamp,
      "description": args.description if args.description else "",
  }
  with open(os.path.join(commit_path, "commit_info.json"), 'w') as info_file:
      json.dump(commit_info, info_file, indent=4)

  print(f"Committed changes as '{args.title}'.")


def view_logs(args):
  """Displays the commit logs."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())

  if not os.path.exists(logs_dir):
      print("No commits found.")
      return

  commits = sorted(os.listdir(logs_dir), reverse=True)
  if not commits:
      print("No commits found.")
      return

  for commit in commits:
      commit_path = os.path.join(logs_dir, commit)
      info_path = os.path.join(commit_path, "commit_info.json")
      if not os.path.exists(info_path):
          continue
      with open(info_path, 'r') as info_file:
          commit_info = json.load(info_file)
      timestamp = datetime.strptime(commit_info["timestamp"], "%Y%m%d%H%M%S")
      readable_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
      print(f"Commit: {commit_info['title']}")
      print(f"Date: {readable_time}")
      print(f"Description: {commit_info['description']}\n")


def check_status(args):
  """Checks the status of the repository."""
  config = load_config()
  logs_dir = config.get("logs_directory", get_logs_path())

  if not os.path.exists(logs_dir):
      print("No commits to compare with.")
      return

  # Get the latest commit
  commits = sorted(os.listdir(logs_dir), reverse=True)
  if not commits:
      print("No commits to compare with.")
      return
  latest_commit = commits[0]
  latest_commit_path = os.path.join(logs_dir, latest_commit)

  # Compare current files with the latest commit
  changes = []
  for item in os.listdir(os.getcwd()):
      if item == REPO_DIR:
          continue
      current_path = os.path.join(os.getcwd(), item)
      commit_path = os.path.join(latest_commit_path, item)
      if not os.path.exists(commit_path):
          changes.append(f"Added: {item}")
      elif os.path.isdir(current_path):
          # For simplicity, not doing deep comparison for directories
          continue
      else:
          if not filecmp.cmp(current_path, commit_path):
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

  if not os.path.exists(logs_dir):
      print("No commits found.")
      return

  # Find the commit directory
  commits = os.listdir(logs_dir)
  selected_commit = None
  for commit in commits:
      if args.commit in commit:
          selected_commit = commit
          break

  if not selected_commit:
      print(f"No commit found matching '{args.commit}'.")
      return

  commit_path = os.path.join(logs_dir, selected_commit)
  print(f"Pulling code from commit '{selected_commit}'...")

  # Copy files from the commit to the current directory
  # Warning: This will overwrite existing files
  for item in os.listdir(commit_path):
      if item == "commit_info.json":
          continue
      s = os.path.join(commit_path, item)
      d = os.path.join(os.getcwd(), item)
      if os.path.isdir(s):
          if os.path.exists(d):
              shutil.rmtree(d)
          shutil.copytree(s, d)
      else:
          shutil.copy2(s, d)

  print("Pull complete. Your working directory has been updated.")


def backup_changes(args):
  """Automatically commits changes every x amount of time."""
  interval = args.time
  print(f"Starting backup every {interval} seconds. Press Ctrl+C to stop.")
  try:
      while True:
          # Check for changes before committing
          # You can enhance this to commit only if there are changes
          commit_args = argparse.Namespace(
              title=f"{args.title} {datetime.now().strftime('%Y-%m-%d %H_%M_%S')}",
              description="Automatic backup"
          )
          commit_changes(commit_args)
          time.sleep(interval)
  except KeyboardInterrupt:
      print("Backup stopped by user.")


def main():
  parser = argparse.ArgumentParser(
      description="SimpleGit: A Beginner-Friendly Local Version Control System"
  )
  subparsers = parser.add_subparsers(title="Commands", dest="command")

  # Init command
  parser_init = subparsers.add_parser('init', aliases=['i'], help='Initialize a new repository')

  # Commit command
  parser_commit = subparsers.add_parser('commit', aliases=['c'], help='Commit current changes')
  parser_commit.add_argument('-m', '--title', required=True, help='Commit title')
  parser_commit.add_argument('-d', '--description', help='Commit description')

  # Log command
  parser_log = subparsers.add_parser('log', aliases=['lg'], help='Show commit logs')

  # Status command
  parser_status = subparsers.add_parser('status', aliases=['st'], help='Show status of repository')

  # Pull command
  parser_pull = subparsers.add_parser('pull', aliases=['p'], help='Pull code from a specific commit')
  parser_pull.add_argument('-c', '--commit', required=True, help='Commit timestamp or title to pull from')

  # Backup command
  parser_backup = subparsers.add_parser('backup', aliases=['b'], help='Automatically commit changes every x amount of time')
  parser_backup.add_argument('-t', '--time', type=int, required=True, help='Time interval in seconds between backups')
  parser_backup.add_argument('-m', '--title', default="Auto backup", help='Commit title for backups')

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
  elif args.command in ['backup', 'b']:
      backup_changes(args)
  else:
      parser.print_help()


if __name__ == "__main__":
  main()
