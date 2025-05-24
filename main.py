from pathlib import Path
import click

SAMPLE_PATH="~/"
OUT_FILE="out.txt"

def get_pdf_from_path(path_to_scan, recursive, filename):
    pth=path_to_scan
    if recursive:
        print("Scan WITH recursive...")
    else:
        print("Scan WITHOUY recursive...")

    return pth

@click.command(help="Scan *.pdf file in LOCATION and output result in file.")
@click.argument("location",type=click.Path(exists=True, file_okay=False,readable=True, path_type=Path, ), )
@click.option('--recursive', '-r', is_flag=True, help = 'Scan subfolder in LOCATION',)
@click.option('--filename', '-f', prompt='Output filename', default=OUT_FILE, help='Filename for output scan result.', )
@click.version_option("0.1.0", prog_name="sinpdf")
def main(location, recursive, filename):
    """
        Search in PDF.
        Scan *.pdf file in LOCATION and output result in file
    """
    target_dir = Path(location)
    if not target_dir.exists():
        click.echo("The target directory doesn't exist")
        raise SystemExit(1)

    for entry in target_dir.iterdir():
        if entry.suffix.lower() == '.pdf':
            click.echo(f"{entry.stem}", nl=True)

    click.echo()

    find_count=get_pdf_from_path(location, recursive, filename)
    #print(f"Search {find_count} PDF file in {location}.")
    click.echo(f"Search {find_count} PDF file in {location}.", nl=True)
    #print(f"Ouptput result in {filename}")
    click.echo(f"Ouptput result in {filename}", nl=True)

if __name__ == '__main__':
    main()