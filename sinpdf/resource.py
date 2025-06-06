about_msg = """
    <b>SinPdf версия {version}</b><p>Быстрый поиск по содержимому PDF файлов</p><p>Вы можете скачать последнюю версию 
    здесь:</p><p><a href="https://github.com/Rifgy/sinpdf.git">https://github.com/Rifgy/sinpdf.git</a></p>
    <p>Copyright &copy; 2025-{year}, Rifgy</p><p>Эта программа является свободным программным обеспечением:
    вы можете распространять ее и/или изменять в соответствии с условиями <b>MIT License</b>, опубликованной Open 
    Source Initiative.</p><p>Данная программа распространяется в надежде, что она будет полезна, но БЕЗ КАКИХ-ЛИБО 
    ГАРАНТИЙ; даже без подразумеваемой гарантии ТОРГОВОЙ ПРИГОДНОСТИ или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННОЙ ЦЕЛИ.
"""
help_msg = ""
window_title = 'Search in PDF'
path_to_scan_placeholdertext = 'Path to scan'
text_to_search_placeholdertext= 'Text to search'
get_path_button_text = '...'
get_path_button_tooltip = 'Select path to scan'
get_help_text = '?'
get_help_set_tooltip = 'About...'
results_list_settooltip = 'Double click to open file'
msgbox_about = 'SinPdf about'
open_file_gialog_text = 'Select folder to find PDF files'
scan_file_in_dir = 'Scan all PDF file\'s in '
proc_dlg_text = 'Processing files...'
proc_dlg_bnt_text = 'Cancel'
proc_dlg_win_title = 'File Processing'
msgbox_warning_title = 'Select folder error'
msgbox_warning_text = 'Please select directory with files'
cmb_get_base_settooltip = 'Select base to search'
chk_new_base_text = 'New'
chk_new_base_settooltip = 'Put scan result\'s to NEW base\n default: "results.db"'


class MessA:
    def __init__(self,):
        self.WindowTitle = window_title
        self.About = about_msg
        self.Help = help_msg
        self.PathToScanPlaceholderText = path_to_scan_placeholdertext
        self.TextToSearchPlaceholderText = text_to_search_placeholdertext
        self.GetPathButtonText = get_path_button_text
        self.GetPathButtonToolTip = get_path_button_tooltip
        self.GetHelpText = get_help_text
        self.GetHelpToolTip = get_help_set_tooltip
        self.ResultsListSetToolTip = results_list_settooltip
        self.MsgBoxAbout = msgbox_about
        self.FileDlgText = open_file_gialog_text
        self.StatusScanFileInDir = scan_file_in_dir
        self.ProcDlgText = proc_dlg_text
        self.ProcDlgBtnText = proc_dlg_bnt_text
        self.ProcDlgWinTitle = proc_dlg_win_title
        self.MsgBoxWarnTitle = msgbox_warning_title
        self.MsgBoxWarnText = msgbox_warning_text
        self.NewBaseText = chk_new_base_text
        self.NewBaseSetToolTip = chk_new_base_settooltip
        self.GetBaseToolTip = cmb_get_base_settooltip


if __name__ == "__main__":
    a = MessA()
    print(a.ProcDlgBtnText)
    pass