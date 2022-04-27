from calibre.customize import FileTypePlugin

class CalibreKepubify(FileTypePlugin):

    name                = 'Kepubify'
    description         = 'Convert all imported EPUB books to Kobo EPUB'
    supported_platforms = ['linux','osx']
    author              = 'José Luis C.D.'
    version             = (0, 0, 1)   # The version number of this plugin
    file_types          = set(['epub']) # The file types that this plugin will be applied to
    on_postprocess      = True # Run this plugin after conversion is complete
    on_postimport       = True
    on_import           = True
    minimum_calibre_version = (0, 7, 53)

    #def run(self, path_to_ebook):
    def postimport(self, book_id, book_format, db):
        if book_format != "epub":
            return

        path_to_ebook = db.new_api.format(book_id, "epub", as_path=True)

        import subprocess
        kepub_path = self.temporary_file('.kepub.epub')
        subprocess.run(["kepubify", path_to_ebook, "-o", kepub_path.name])

        db.new_api.add_format(book_id, "kepub", kepub_path.name, run_hooks=False)

