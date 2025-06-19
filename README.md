# ai_analyics_assistant
## AI Assistant for Self Service Analytics And Insights


## Features

- Natural language query interface for analytics
- Automated insights generation
- Data visualization support
- Integration with popular data sources
- Extensible plugin architecture

## Installation

```bash
git clone https://github.com/yourusername/ai_analyics_assistant.git
cd ai_analyics_assistant
pip install -r requirements.txt
```

## Usage

Start the assistant:

```bash
python main.py
```

Access the web interface at [http://localhost:8000](http://localhost:8000).

## Project Structure

```
app/
├── database/
│   ├── load_data_sources.py
│   └── schema.py
├── llm/
│   └── llm.py
├── tools/
│   ├── __init__.py
│   └── tools.py
├── run.py
├── config/
│   ├── duckdb_sql_llm.mod
│   ├── suggest_viz.mod
│   └── summarize_data.mod
data/
├── app.db
images/
logs/
├── app.log

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License.