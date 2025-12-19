# Graph Code Mapper

**Graph Code Mapper** is an interactive tool designed to help developers visualize and analyze the structure of a codebase. It generates a graph of functions and their dependencies, making it easier to understand how different parts of a project are interconnected. The tool also highlights clusters of tightly coupled functions using community detection algorithms.

---

## Features

- Visualizes code structure and function dependencies.
- Interactive graph with zooming and filtering.
- Detects clusters in the code using **Louvain modularity**.
- Helps identify areas for refactoring or optimization.
- Supports large codebases efficiently.

---

## Technology Stack

- **Backend**: Python 3
  - Parses code to extract functions and dependencies.
  - Generates graph data for visualization.
- **Frontend**: D3.js
  - Renders interactive and dynamic graphs.
- **Algorithm**: Louvain modularity
  - Detects communities within the code graph to identify tightly coupled functions.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vartikaaaa/GraphCodeMapper_.git
```

2. Navigate to the project directory:

```
cd GraphCodeMapper_
```

3. Install required Python packages:
```
pip install -r requirements.txt
```

4. Open index.html in a browser to view the visualization.

## Usage

- Place the code files you want to analyze in the input/ folder.

- Open graphcodemapper.html in a browser to explore the interactive graph.

- Use zooming and filtering features to navigate large graphs.

- Identify clusters of functions using the Louvain modularity visualization.

## Challenges Faced

- Handling large codebases without overwhelming the visualization.

- Accurately parsing dependencies from different types of code structures.

- Optimizing Louvain modularity calculations for performance.

## Future Improvements

- Support for multiple programming languages.

- Enhanced filtering and search options for functions.

- Integration with code editors for real-time visualization.

- Export graphs as images or PDFs for documentation purposes.
