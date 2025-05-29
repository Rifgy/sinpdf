# SinPdf 
____
Search in PDF-files

Small program for scan PDF files massive and fast search 
text in result.
____
### Overview
The Python utility to optimize the search for the desired 
document among the large array of PDF files

### Requirements to run this program
- Python
- **Future**: OS only (Linux, Windows, MacOS)

### Installation
 ```shell
$ pip install git+https://github.com/Uli-Z/autoPDFtagger
```

Create configuration file and save it to *~/.autoPDFtagger.conf*: 
```ini
; Configuration for autoPDFtagger

[DEFAULT]
language = {YOUR LANGUAGE}

[OPENAI-API]
API-Key = {INSERT YOUR API-KEY}
```
### Usage

### Code Structure

- `main.py`: main interface for the application.
- `functions.py`: Manages the core functionalities of the tool.
- `resource.py`: resources.
- `Future: config.ini`: An example configuration file outlining API key setup and other settings.

## Future Development
- **Integration and Compatibility**:
  - Ensuring compatibility with applications like paperless-ngx.
- Enhancing tag organization and developing hierarchical information through the application of clustering algorithms on a vector database

### License:
#### MIT License

