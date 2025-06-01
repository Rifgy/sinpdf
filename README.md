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

### Clone 
 ```shell
$ git clone https://github.com/Rifgy/sinpdf.git
```

Create a configuration file and save it to *~/.config.ini*: 
```ini
; Configuration for config.ini
[Default]
fontname = {CHOISE THE FONT or EMPY}
fontsize = {CHOISE THE FONT SIZE or EMPY}

[ScanOpt]
basename = {YOUR BASE NAME}
basepath = {YOUR BASE PATH}
limittoscanpages = 1
getmetafrompdf = True
```
### Usage

### Code Structure

- `main.py`     : main interface for the application.
- `functions.py`: Manages the core functionalities of the tool.
- `resource.py` : resources.
- `config.ini`  : configuration file.

### Future Development
- **Integration and Compatibility**:
  - Ensuring compatibility with applications like paperless-ngx.
- Enhancing tag organization and developing hierarchical information through the application of clustering algorithms on a vector database

### License:
#### MIT License

