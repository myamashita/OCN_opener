# encoding: cp1252

import gzip
import zlib
# import bz2  # FIXME: spits out an error when imported?!?

import sublime
import sublime_plugin


compression_formats = {
    '.gz': gzip.open,
    '.adc_gz': zlib.decompress,
    '.fsi_gz': zlib.decompress,
    '.hadc_gz': zlib.decompress,
    '.mir_gz': zlib.decompress,
    '.yng_gz': zlib.decompress,

    # '.bz2': bz2.open,
}


def get_decompressor_by_filename(filename):
    for suffix, decompressor in compression_formats.items():
        if filename.endswith(suffix):
            return suffix, decompressor
    return None, None


class DecompressFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, filename=None, suffix=None, decompressor=None):
        if filename is None:
            filename = self.view.file_name()
            if not filename:
                print("can't find filename for decompression")
                return
        if not suffix:
            suffix, decompressor = get_decompressor_by_filename(filename)
            if not suffix or not decompressor:
                print("trying to decompress unknown file format")
                return
        if not decompressor:
            decompressor = compression_formats[suffix]

        view = self.view
        view.set_name(filename[:-len(suffix)])

        pos = 0
        if suffix != '.gz':
            filegz = open(filename, 'rb')
            filegz = filegz.read()
            file = zlib.decompress(filegz).decode('cp1252')
            file = file.replace('\r\n','\n')
            for line in file:
                pos += view.insert(edit, pos, line)
        else:
            with decompressor(filename) as f:
                for line in f:
                    # print(type(line), line)
                    pos += view.insert(edit, pos, line.decode('utf-8'))

        #view.set_read_only(True)


class OpenCompressedFile(sublime_plugin.EventListener):
    def on_load(self, view):
        filename = view.file_name()
        suffix, decompressor = get_decompressor_by_filename(filename)
        if suffix and decompressor:
            sublime.status_message("opening compressed file: " + filename)
            print("opening compressed file: " + filename)

            decomp_view = view.window().new_file()
            view.close()
            decomp_view.run_command(
                'decompress_file', {'filename': filename, 'suffix': suffix}
            )
