import json
import os
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def load_config(file_path):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def create_agents(agent_configs):
    """Create agent objects based on configuration."""
    agents = []
    for config in agent_configs:
        agent = Agent(
            role=config["role"].replace(" ", "_").lower(),
            goal=config["goal"],
            backstory=config["backstory"],
            memory=bool(config["memory"]),
            verbose=bool(config["verbose"]),
            allow_delegation=bool(config["allow_delegation"])
        )
        agents.append(agent)
    return agents


def create_tasks(task_configs, agents):
    """Create task objects based on configuration."""
    tasks = []
    agent_map = {agent.role: agent for agent in agents}

    for config in task_configs:
        task = Task(
            description=config["description"],
            agent=agent_map[config["agentRole"].replace(" ", "_").lower()],
            output=TaskOutput(
                description=config["output"]["description"],
                result=config["output"]["result"]
            )
        )
        tasks.append(task)
    return tasks


class FileOperations:
    def __init__(self, base_directory="."):
        self.base_directory = base_directory

    def create_directory(self, path):
        """Create a directory if it doesn't exist."""
        try:
            os.makedirs(os.path.join(self.base_directory, path), exist_ok=True)
        except OSError as error:
            logger.error(f"Error creating directory {path}: {error}")
            raise

    def write_file(self, directory, filename, data):
        """Write data to a file."""
        full_path = os.path.join(self.base_directory, directory, filename)
        try:
            with open(full_path, "w") as file:
                file.write(data)
        except OSError as error:
            logger.error(f"Error writing file {filename}: {error}")
            raise

    def write_result_file(self, crew, result):
        directory = "crew_output"
        filename = f"{crew.id}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
        self.create_directory(directory)
        self.write_file(directory, filename, result)


def main():
    config = load_config('config/crew.json')

    agents = create_agents(config["agents"])
    tasks = create_tasks(config["tasks"], agents)
    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=True)
    result = crew.kickoff()

    file_ops = FileOperations()
    file_ops.write_result_file(crew, result)


if __name__ == '__main__':
    main()
