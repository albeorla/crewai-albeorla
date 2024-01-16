from langchain_community.tools import tool, DuckDuckGoSearchRun, WriteFileTool, ReadFileTool


class CrewTools:

    @tool(return_direct=True)
    def duckduckgo_search_run(self, query: str) -> str:
        """
        Run a DuckDuckGo search and return the results as a string.

        Args:
            query (str): The search query string.

        Returns:
            str: The search results.
        """
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(query)

    @tool(return_direct=True)
    def write_file(self, filename: str, data: str) -> None:
        """
        Write data to a file using WriteFileTool.

        Args:
            filename (str): The name of the file to write to.
            data (str): The data to write to the file.
        """
        write_tool = WriteFileTool()
        write_tool.run({"filename": filename, "text": data})

    @tool(return_direct=True)
    def read_file(self, filename: str) -> str:
        """
        Read data from a file using ReadFileTool.

        Args:
            filename (str): The name of the file to read from.

        Returns:
            str: The data read from the file.
        """
        read_tool = ReadFileTool()
        return read_tool.run({"filename": filename})
